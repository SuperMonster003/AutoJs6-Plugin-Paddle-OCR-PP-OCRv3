"""Install language packages of this plugin on a device and check them through the AutoJs6 host.

Each check prints PASS or FAIL with its key values (recognized text is not printed):
  install    every flavor's APK for the device ABI installs over any earlier build (a build signed
             by the other key, debug vs release, is uninstalled first)
  identity   each installed package has the versionName and versionCode of version.properties
  discovery  every installed flavor answers the org.autojs.plugin.PADDLE_OCR action (coexistence)
  label      the host reads each flavor's application label
  routing    with zh first, ocr.paddle.recognizeText(img) without any condition reads the Chinese
             sample and the plugin that served it is reported (the zh package unless a Paddle OCR
             plugin with a higher variant number is installed and enabled, roadmap D22); every other flavor is
             reached by { profile } alone (D23)
  recognize  ocr.paddle.recognizeText(img, { engineId }) reads the flavor's androidTest sample;
             the first flavor also runs useSlim x useOpenCL (fp32 / slim, CPU / NNAPI), reporting
             the cold and warm host-side times, the execution provider from the plugin log and
             whether the text equals the fp32 / CPU result
  raw image  the first flavor's fp32 / CPU run is repeated with useRaw false (encoded PNG); the
             default runs pass the bitmap through the host's SharedMemory (RAW_IMAGE, API 27+), so
             the texts must be equal and the host must not log a raw transfer fallback
  lite       --lite also installs Paddle Lite 1.1.0 (the sibling repository's release) and reads
             the Chinese sample through it (fp32 and slim)

A line matches when its similarity to some recognized line is at least --min-similarity (PP-OCRv3
reads a few characters differently). `--cls` adds an informational run of the rotated Chinese
sample with useCls true; hosts before the USE_CLS contract do not forward the option.
The host script then opens Plugin Center; --screenshot saves a screenshot of it. Temporary files on
the device are removed afterwards; the plugins stay installed.
"""

import argparse
import difflib
import json
from pathlib import Path
import re
import statistics
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
BASE_PACKAGE = 'io.github.supermonster003.autojs6.plugin.paddleocr.v3'
BASE_PLUGIN_ID = 'paddle-ocr-pp-ocrv3'
# flavor -> (package suffix, plugin id suffix, application label, model profile)
FLAVORS = {
    'zh': ('', '', 'Paddle OCR (PP-OCRv3)', 'zh'),
    'en': ('.en', '-en', 'Paddle OCR (PP-OCRv3 EN)', 'en'),
    'zhHant': ('.zhhant', '-zh-hant', 'Paddle OCR (PP-OCRv3 ZH-Hant)', 'zh-hant'),
    'ja': ('.ja', '-ja', 'Paddle OCR (PP-OCRv3 JA)', 'ja'),
    'ko': ('.ko', '-ko', 'Paddle OCR (PP-OCRv3 KO)', 'ko'),
}
LITE_PACKAGE = BASE_PACKAGE + '.paddlelite'
LITE_PLUGIN_ID = 'paddle-ocr-pp-ocrv3-paddle-lite'
LITE_RELEASES = ROOT.parent / 'AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite' / 'releases'
# Paddle OCR plugins whose variant number beats v3 in the host's default choice (D22).
HIGHER_VARIANT = re.compile(r'\.paddleocr\.v([4-9])(?:\.|$)')
MATRIX = [('fp32/cpu', False, False), ('fp32/nnapi', False, True), ('slim/cpu', True, False), ('slim/nnapi', True, True)]
ACTION = 'org.autojs.plugin.PADDLE_OCR'
SAMPLES = ROOT / 'app' / 'src' / 'androidTest' / 'assets' / 'samples'
RUN_ACTIVITY = 'org.autojs.autojs.external.open.RunIntentActivity'
PLUGIN_CENTER = 'org.autojs.autojs.core.plugin.center.PluginCenterActivity'
NAME = 'ppocrv3-device-check'
READY = re.compile(r'^\s*(\d+)\.(\d+)\s.*Sessions ready on (\w+) in (\d+) ms \(cls (on|off)\)', re.M)
RAW_FALLBACK = 'raw image transfer failed|shared memory unavailable'
RAW_MIN_API = 27

HOST_SCRIPT = '''\
'use strict';
let CONFIG = __CONFIG__;
let dir = context.getExternalFilesDir(null).getAbsolutePath();
let result = { labels: {}, runs: [] };
let pm = context.getPackageManager();
CONFIG.packages.forEach(function (name) {
    try {
        result.labels[name] = String(pm.getApplicationLabel(pm.getApplicationInfo(name, 0)));
    } catch (e) {
        result.labels[name] = 'error: ' + e;
    }
});
CONFIG.runs.forEach(function (run) {
    let entry = { id: run.id, times: [], start: Date.now() };
    try {
        let img = images.read(files.join(dir, run.file));
        try {
            for (let i = 0; i < run.repeat; i += 1) {
                let start = Date.now();
                let texts = ocr.paddle.recognizeText(img, run.options);
                entry.times.push(Date.now() - start);
                let size = typeof texts.size === 'function' ? texts.size() : texts.length;
                entry.texts = [];
                for (let j = 0; j < size; j += 1) {
                    entry.texts.push(String(typeof texts.get === 'function' ? texts.get(j) : texts[j]));
                }
            }
        } finally {
            img.recycle();
        }
    } catch (e) {
        entry.error = String(e);
    }
    entry.end = Date.now();
    result.runs.push(entry);
});
try {
    let intent = new android.content.Intent();
    intent.setClassName(context.getPackageName(), CONFIG.pluginCenter);
    intent.addFlags(android.content.Intent.FLAG_ACTIVITY_NEW_TASK);
    context.startActivity(intent);
} catch (e) {
    result.pluginCenterError = String(e);
}
let out = files.join(dir, CONFIG.name + '.json');
files.write(out + '.part', JSON.stringify(result));
new java.io.File(out + '.part').renameTo(new java.io.File(out));
'''


def line_similarity(expected, texts):
    """Best-match similarity of each expected line, spaces ignored.

    The ko detector boxes words rather than lines, so up to 4 consecutive recognized texts joined
    together also count as a candidate.
    """
    parts = [text.replace(' ', '') for text in texts]
    recognized = [''.join(parts[start:start + size]) for size in range(1, 5) for start in range(len(parts) - size + 1)]
    scores = []
    for line in expected:
        target = line.replace(' ', '')
        scores.append(max((difflib.SequenceMatcher(None, target, text).ratio() for text in recognized), default=0.0))
    return scores


def start_host_script(adb, host, code):
    """Runs JavaScript code in the host through the script extra of RunIntentActivity.

    The path extra needs all-files access on Android 11+, which a host freshly installed on an
    emulator does not have; inline code does not, and the host reads its own external files.
    """
    adb('shell', f"am start -n {host}/{RUN_ACTIVITY} -e script '{code}'")


def bring_host_to_front(adb, host):
    """Starts the launcher activity of the host from adb.

    A host without a foreground service is a cached process once RunIntentActivity finishes, and
    Android 12+ freezes cached processes, which stops a running script in the middle. Launching the
    host from the script itself is not enough: the freezer won before the activity started.
    """
    query = adb('shell', 'cmd', 'package', 'query-activities', '--brief',
                '-a', 'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', host)
    components = [line.strip() for line in query.stdout.splitlines() if line.strip().startswith(f'{host}/')]
    # A debug host also has the launcher of LeakCanary, so resolve-activity returns the chooser.
    components.sort(key=lambda component: 'leakcanary' in component)
    if query.returncode == 0 and components:
        adb('shell', 'am', 'start', '-W', '-n', components[0])
    else:
        adb('shell', 'monkey', '-p', host, '-c', 'android.intent.category.LAUNCHER', '1')


def disabled_plugins(adb, host):
    """Packages switched off in the Plugin Center of the host, read with run-as (debug hosts only).

    The host skips them when it picks a plugin, and a package without an entry counts as enabled.
    """
    prefs = adb('shell', 'run-as', host, 'cat', 'shared_prefs/plugin_center_enable_state.xml').stdout
    return set(re.findall(r'name="key_\$_enabled_plugin_\$_([^"]+)" value="false"', prefs))


def run_host_file(adb, host, name):
    """Runs a script pushed to the external files directory of the host, with the host in front."""
    bring_host_to_front(adb, host)
    start_host_script(adb, host, f'engines.execScriptFile(context.getExternalFilesDir(null).getAbsolutePath() + "/{name}")')


def prepare_host_files(adb, host, remote_dir, timeout=30):
    """Returns None when remote_dir is the host's own directory, otherwise why it is not.

    adb push creates a missing directory with shell as its owner and the host cannot read it, so a
    host that never ran creates the directory itself first.
    """
    if adb('shell', 'ls', '-d', remote_dir).returncode != 0:
        start_host_script(adb, host, 'context.getExternalFilesDir(null)')
        deadline = time.monotonic() + timeout
        while adb('shell', 'ls', '-d', remote_dir).returncode != 0:
            if time.monotonic() > deadline:
                return f'the host did not create {remote_dir} within {timeout} s'
            time.sleep(1)
    owner = adb('shell', 'stat', '-c', '%U', remote_dir).stdout.strip()
    if owner in ('shell', 'root'):
        return f'{remote_dir} belongs to {owner} (adb push created it before the host ran); remove it and run again'
    return None


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--flavor', action='append', choices=sorted(FLAVORS), help='repeatable; defaults to zh and en')
    parser.add_argument('--build', choices=('debug', 'release'), default='release',
                        help='debug reads app/build/outputs/apk, release reads releases/v<VERSION_NAME>')
    parser.add_argument('--host', default='org.autojs.autojs6', help='AutoJs6 host package')
    parser.add_argument('--abi', help='install the APKs of this ABI (e.g. armeabi-v7a on a 64-bit device that also '
                                      'runs 32-bit code); defaults to the primary ABI of the device')
    parser.add_argument('--repeat', type=int, default=4, help='calls per run; the first one includes the cold load')
    parser.add_argument('--min-similarity', type=float, default=0.8)
    parser.add_argument('--cls', action='store_true', help='also run the rotated Chinese sample with useCls true')
    parser.add_argument('--lite', metavar='VERSION', help='also install and run Paddle Lite VERSION (e.g. 1.1.0)')
    parser.add_argument('--no-install', action='store_true',
                        help='test the installed packages (their version and ABI are still checked); ColorOS asks '
                             'to confirm every adb install')
    parser.add_argument('--timeout', type=int, default=600, help='seconds to wait for the host script')
    parser.add_argument('--screenshot', type=Path, help='save a Plugin Center screenshot here')
    parser.add_argument('--json', type=Path, help='save the raw host result (including recognized text) here')
    args = parser.parse_args()
    flavors = args.flavor or ['zh', 'en']

    properties = dict(line.split('=', 1) for line in
                      (ROOT / 'version.properties').read_text().splitlines()
                      if '=' in line and not line.startswith('#'))
    version_name = properties['VERSION_NAME']
    version_code = int(properties['VERSION_BUILD']) + int(properties['VERSION_CODE_OFFSET'])
    samples = json.loads((SAMPLES / 'samples.json').read_text(encoding='utf-8'))

    def adb(*command, timeout=120):
        return subprocess.run([args.adb, '-s', args.serial, *command], capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=timeout)

    results = []

    def report(name, passed, value):
        print(f"{'PASS' if passed else 'FAIL'} {name}: {value}", flush=True)
        results.append(passed)

    abis = adb('shell', 'getprop', 'ro.product.cpu.abilist').stdout.strip().split(',')
    if args.abi and args.abi not in abis:
        parser.error(f'{args.abi} is not among the device ABIs {",".join(abis)}')
    abi = args.abi or abis[0]
    abi_option = ['--abi', abi] if args.abi else []
    model = adb('shell', 'getprop', 'ro.product.model').stdout.strip()
    api = adb('shell', 'getprop', 'ro.build.version.sdk').stdout.strip()
    host = re.search(r'versionCode=(\d+)', adb('shell', 'dumpsys', 'package', args.host).stdout)
    print(f'Device: {model}, API {api}, {abi}, host {host.group(1) if host else "missing"}, {args.build} build', flush=True)

    packages = {}
    for flavor in flavors:
        suffix = FLAVORS[flavor][0]
        package = BASE_PACKAGE + suffix
        packages[flavor] = package
        if not args.no_install:
            if args.build == 'debug':
                candidates = sorted((ROOT / 'app' / 'build' / 'outputs' / 'apk' / flavor / 'debug').glob(f'*-{abi}.apk'))
            else:
                token = FLAVORS[flavor][3]
                candidates = sorted((ROOT / 'releases' / f'v{version_name}').glob(f'*-{token}-{abi}-*.apk'))
            if len(candidates) != 1:
                report(f'{flavor} install', False, f'expected one {abi} APK, found {len(candidates)}')
                continue
            installed = adb('install', '-r', *abi_option, str(candidates[0]), timeout=300)
            replaced = 'INSTALL_FAILED_UPDATE_INCOMPATIBLE' in installed.stdout + installed.stderr
            if replaced:
                # The installed build is signed by the other key (debug vs release): replace it.
                adb('uninstall', package, timeout=120)
                installed = adb('install', *abi_option, str(candidates[0]), timeout=300)
            report(f'{flavor} install', installed.returncode == 0 and 'Success' in installed.stdout,
                   (candidates[0].name + (' (replaced a build with another signature)' if replaced else ''))
                   if installed.returncode == 0 else installed.stderr.strip()[-200:])
        dump = adb('shell', 'dumpsys', 'package', package).stdout
        code = re.search(r'versionCode=(\d+)', dump)
        name = re.search(r'versionName=(\S+)', dump)
        actual = (name.group(1) if name else None, int(code.group(1)) if code else None)
        # The ABI the package manager chose for the native libraries (the process runs 32-bit for armeabi-v7a).
        primary = re.search(r'primaryCpuAbi=(\S+)', dump)
        primary = primary.group(1) if primary else None
        report(f'{flavor} identity', actual == (version_name, version_code) and primary == abi,
               f'{package} {actual[0]} ({actual[1]}), {primary}')
    if args.lite and not args.no_install:
        candidates = sorted((LITE_RELEASES / f'v{args.lite}').glob(f'*-v{args.lite}-{abi}-*.apk'))
        if len(candidates) == 1:
            installed = adb('install', '-r', *abi_option, str(candidates[0]), timeout=300)
            report('lite install', installed.returncode == 0 and 'Success' in installed.stdout,
                   candidates[0].name if installed.returncode == 0 else installed.stderr.strip()[-200:])
        else:
            report('lite install', False, f'expected one {abi} APK of Paddle Lite {args.lite}, found {len(candidates)}')

    services = adb('shell', 'cmd', 'package', 'query-services', '--brief', '-a', ACTION).stdout.split()
    service_packages = sorted({service.split('/')[0] for service in services if '/' in service})
    ours = [package for package in service_packages if package.startswith(BASE_PACKAGE)]
    expected = list(packages.values()) + ([LITE_PACKAGE] if args.lite else [])
    report('discovery', all(package in ours for package in expected),
           f'{len(ours)} {BASE_PACKAGE}* services among {len(service_packages)} {ACTION} services')
    disabled = disabled_plugins(adb, args.host)
    higher = sorted(package for package in service_packages
                    if HIGHER_VARIANT.search(package) and package not in disabled)

    runs = []
    if flavors[0] == 'zh':
        # Defaults apply here: useSlim true, and RAW_IMAGE from API 27.
        runs.append({'id': 'zh routing (no condition)', 'flavor': 'zh', 'sample': 'zh', 'file': samples['zh']['file'],
                     'repeat': args.repeat, 'options': {}, 'routing': None if higher else packages['zh']})
    for flavor in flavors[1:]:
        profile = FLAVORS[flavor][3]
        runs.append({'id': f'{flavor} routing (profile {profile})', 'flavor': flavor, 'sample': flavor,
                     'file': samples[flavor]['file'], 'repeat': args.repeat, 'options': {'profile': profile},
                     'routing': packages[flavor]})
    for index, flavor in enumerate(flavors):
        id_suffix = FLAVORS[flavor][1]
        engine_id = BASE_PLUGIN_ID + id_suffix
        variants = MATRIX if index == 0 else MATRIX[:1]
        for label, slim, nnapi in variants:
            runs.append({'id': f'{flavor} {label}', 'flavor': flavor, 'sample': flavor, 'file': samples[flavor]['file'],
                         'repeat': args.repeat, 'options': {'engineId': engine_id, 'useSlim': slim, 'useOpenCL': nnapi}})
        if index == 0:
            runs.append({'id': f'{flavor} fp32/cpu encoded', 'flavor': flavor, 'sample': flavor, 'encoded': True,
                         'file': samples[flavor]['file'], 'repeat': args.repeat,
                         'options': {'engineId': engine_id, 'useSlim': False, 'useOpenCL': False, 'useRaw': False}})
        if args.cls and flavor == 'zh':
            runs.append({'id': 'zh rotated useCls', 'flavor': flavor, 'sample': 'zh-rotated', 'info': True,
                         'file': samples['zh-rotated']['file'], 'repeat': 2,
                         'options': {'engineId': engine_id, 'useCls': True}})
    if args.lite:
        for label, slim in (('fp32', False), ('slim', True)):
            runs.append({'id': f'lite {label}', 'flavor': None, 'sample': 'zh', 'file': samples['zh']['file'],
                         'repeat': args.repeat, 'options': {'engineId': LITE_PLUGIN_ID, 'useSlim': slim}})

    remote_dir = f'/sdcard/Android/data/{args.host}/files'
    files = sorted({run['file'] for run in runs})
    remote = [f'{remote_dir}/{NAME}{suffix}' for suffix in ('.js', '.json', '.json.part')]
    remote += [f'{remote_dir}/{name}' for name in files]
    config = {'name': NAME, 'packages': list(packages.values()), 'pluginCenter': PLUGIN_CENTER,
              'runs': [{key: run[key] for key in ('id', 'file', 'repeat', 'options')} for run in runs]}
    unusable = prepare_host_files(adb, args.host, remote_dir)
    if unusable:
        report('host script', False, unusable)
        return 1
    try:
        adb('shell', 'rm', '-f', *remote)
        for name in files:
            adb('push', str(SAMPLES / name), f'{remote_dir}/{name}')
        with tempfile.TemporaryDirectory() as temp:
            script = Path(temp) / f'{NAME}.js'
            script.write_text(HOST_SCRIPT.replace('__CONFIG__', json.dumps(config)), encoding='utf-8')
            pushed = adb('push', str(script), f'{remote_dir}/{NAME}.js')
        if pushed.returncode != 0:
            report('host script', False, f'push failed: {pushed.stderr.strip()}')
            return 1
        # adb shell joins its arguments with spaces (adb logcat quotes them itself).
        since = adb('shell', "date '+%m-%d %H:%M:%S.000'").stdout.strip()
        run_host_file(adb, args.host, f'{NAME}.js')
        result = None
        deadline = time.monotonic() + args.timeout
        while result is None and time.monotonic() < deadline:
            time.sleep(3)
            text = adb('shell', 'cat', f'{remote_dir}/{NAME}.json')
            if text.returncode == 0 and text.stdout.strip():
                result = json.loads(text.stdout)
        if result is None:
            report('host script', False, f'no host result within {args.timeout} s')
            return 1
        if args.json:
            args.json.parent.mkdir(parents=True, exist_ok=True)
            args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

        # Each engine (re)creation logs one line; the run whose host-side time window holds the
        # line's timestamp is the run that created it (and so the plugin that served that run).
        ready = []
        for package in packages.values():
            pid = adb('shell', 'pidof', package).stdout.strip()
            lines = adb('logcat', '-d', '-v', 'epoch', '-T', since, '--pid', pid,
                        '-s', 'ORTSessionManager:*').stdout if pid else ''
            for match in READY.finditer(lines):
                seconds, fraction, provider, load, cls = match.groups()
                ready.append((int(seconds) * 1000 + int(fraction[:3].ljust(3, '0')), package, provider, load, cls))
        host_pid = adb('shell', 'pidof', args.host).stdout.strip()
        # Older logcat versions also print "--------- beginning of <buffer>" lines here.
        raw_fallbacks = sum(bool(re.search(RAW_FALLBACK, line)) for line in
                            adb('logcat', '-d', '-T', since, '--pid', host_pid, '-e', RAW_FALLBACK)
                            .stdout.splitlines()) if host_pid else 0

        for flavor, package in packages.items():
            label = result['labels'].get(package)
            report(f'{flavor} label', label == FLAVORS[flavor][2], label)
        entries = dict(zip((run['id'] for run in runs), result['runs']))
        baseline = entries.get(f'{flavors[0]} fp32/cpu', {}).get('texts')
        for run, entry in zip(runs, result['runs']):
            if 'error' in entry or not entry.get('times'):
                report(run['id'], False, entry.get('error', 'no result'))
                continue
            created = [line for line in ready if entry['start'] - 50 <= line[0] <= entry['end'] + 50]
            provider = created[0] if created else None
            scores = line_similarity(samples[run['sample']]['lines'], entry['texts'])
            matched = sum(score >= args.min_similarity for score in scores)
            warm = entry['times'][1:] or entry['times']
            value = (f'lines {matched}/{len(scores)} (min similarity {min(scores):.2f}), '
                     f'cold {entry["times"][0]} ms, warm median {statistics.median(warm):.0f} ms')
            if run['flavor'] is not None:
                value += (f', provider {provider[2] if provider else "?"}' +
                          (f' (cls {provider[4]}, load {provider[3]} ms)' if provider else ''))
            passed = matched == len(scores)
            if 'routing' in run:
                served = provider[1] if provider else None
                if run['routing'] is None:
                    # A higher variant wins the default choice (D22): the run must not reach this plugin.
                    passed = passed and served is None
                    value += f', served by {served or "another plugin"} (enabled: {", ".join(higher)})'
                else:
                    passed = passed and served == run['routing']
                    value += f', served by {served or "another plugin"}'
            elif run['flavor'] == flavors[0] and baseline is not None and not run.get('info') \
                    and run['id'] != f'{flavors[0]} fp32/cpu':
                value += f', same text as fp32/cpu: {"yes" if entry["texts"] == baseline else "no"}'
            if run.get('encoded'):
                passed = passed and entry['texts'] == baseline
                if int(api) < RAW_MIN_API:
                    value += f', raw image n/a below API {RAW_MIN_API} (both runs encoded)'
                else:
                    passed = passed and raw_fallbacks == 0
                    value += (f', raw fp32/cpu warm median {statistics.median(entries[f"{flavors[0]} fp32/cpu"]["times"][1:]):.0f} ms'
                              f', host raw fallbacks {raw_fallbacks}')
            if run.get('info'):
                print(f"INFO {run['id']}: {value}", flush=True)
            else:
                report(run['id'], passed, value)
        if 'pluginCenterError' in result:
            print(f'Plugin Center did not open: {result["pluginCenterError"]}', flush=True)
        elif args.screenshot:
            time.sleep(3)
            image = subprocess.run([args.adb, '-s', args.serial, 'exec-out', 'screencap', '-p'],
                                   capture_output=True, timeout=60).stdout
            args.screenshot.parent.mkdir(parents=True, exist_ok=True)
            args.screenshot.write_bytes(image)
            print(f'Plugin Center screenshot: {args.screenshot}', flush=True)
    finally:
        adb('shell', 'rm', '-f', *remote)

    print(f'{sum(results)}/{len(results)} checks passed', flush=True)
    return 0 if all(results) else 1


if __name__ == '__main__':
    sys.exit(main())
