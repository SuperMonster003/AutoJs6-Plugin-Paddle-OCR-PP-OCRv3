"""Install language packages of this plugin on a device and check them through the AutoJs6 host.

Each check prints PASS or FAIL with its key values (recognized text is not printed):
  install    every flavor's APK for the device ABI installs over any earlier build (a build signed
             by the other key, debug vs release, is uninstalled first)
  identity   each installed package has the versionName and versionCode of version.properties
  discovery  every installed flavor answers the org.autojs.plugin.PADDLE_OCR action (coexistence)
  label      the host reads each flavor's application label
  recognize  ocr.paddle.recognizeText(img, { engineId }) reads the flavor's androidTest sample;
             the first flavor also runs useSlim x useOpenCL (fp32 / slim, CPU / NNAPI), reporting
             the cold and warm host-side times, the execution provider from the plugin log and
             whether the text equals the fp32 / CPU result

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
# flavor -> (package suffix, plugin id suffix, application label)
FLAVORS = {
    'zh': ('', '', 'Paddle OCR (PP-OCRv3)'),
    'en': ('.en', '-en', 'Paddle OCR (PP-OCRv3 EN)'),
    'zhHant': ('.zhhant', '-zh-hant', 'Paddle OCR (PP-OCRv3 ZH-Hant)'),
    'ja': ('.ja', '-ja', 'Paddle OCR (PP-OCRv3 JA)'),
    'ko': ('.ko', '-ko', 'Paddle OCR (PP-OCRv3 KO)'),
}
MATRIX = [('fp32/cpu', False, False), ('fp32/nnapi', False, True), ('slim/cpu', True, False), ('slim/nnapi', True, True)]
ACTION = 'org.autojs.plugin.PADDLE_OCR'
SAMPLES = ROOT / 'app' / 'src' / 'androidTest' / 'assets' / 'samples'
RUN_ACTIVITY = 'org.autojs.autojs.external.open.RunIntentActivity'
PLUGIN_CENTER = 'org.autojs.autojs.core.plugin.center.PluginCenterActivity'
NAME = 'ppocrv3-device-check'
READY = re.compile(r'Sessions ready on (\w+) in (\d+) ms \(cls (on|off)\)')

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
    let entry = { id: run.id, times: [] };
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
    """Lowest best-match similarity over the expected lines, spaces ignored."""
    recognized = [text.replace(' ', '') for text in texts]
    scores = []
    for line in expected:
        target = line.replace(' ', '')
        scores.append(max((difflib.SequenceMatcher(None, target, text).ratio() for text in recognized), default=0.0))
    return scores


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--flavor', action='append', choices=sorted(FLAVORS), help='repeatable; defaults to zh and en')
    parser.add_argument('--build', choices=('debug', 'release'), default='release',
                        help='debug reads app/build/outputs/apk, release reads releases/v<VERSION_NAME>')
    parser.add_argument('--host', default='org.autojs.autojs6', help='AutoJs6 host package')
    parser.add_argument('--repeat', type=int, default=4, help='calls per run; the first one includes the cold load')
    parser.add_argument('--min-similarity', type=float, default=0.8)
    parser.add_argument('--cls', action='store_true', help='also run the rotated Chinese sample with useCls true')
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

    abi = adb('shell', 'getprop', 'ro.product.cpu.abilist').stdout.strip().split(',')[0]
    model = adb('shell', 'getprop', 'ro.product.model').stdout.strip()
    api = adb('shell', 'getprop', 'ro.build.version.sdk').stdout.strip()
    host = re.search(r'versionCode=(\d+)', adb('shell', 'dumpsys', 'package', args.host).stdout)
    print(f'Device: {model}, API {api}, {abi}, host {host.group(1) if host else "missing"}, {args.build} build', flush=True)

    packages = {}
    for flavor in flavors:
        suffix, _, _ = FLAVORS[flavor]
        package = BASE_PACKAGE + suffix
        packages[flavor] = package
        if args.build == 'debug':
            candidates = sorted((ROOT / 'app' / 'build' / 'outputs' / 'apk' / flavor / 'debug').glob(f'*-{abi}.apk'))
        else:
            candidates = sorted((ROOT / 'releases' / f'v{version_name}').glob(f'*-{flavor.lower()}-{abi}-*.apk'))
        if len(candidates) != 1:
            report(f'{flavor} install', False, f'expected one {abi} APK, found {len(candidates)}')
            continue
        installed = adb('install', '-r', str(candidates[0]), timeout=300)
        replaced = 'INSTALL_FAILED_UPDATE_INCOMPATIBLE' in installed.stdout + installed.stderr
        if replaced:
            # The installed build is signed by the other key (debug vs release): replace it.
            adb('uninstall', package, timeout=120)
            installed = adb('install', str(candidates[0]), timeout=300)
        report(f'{flavor} install', installed.returncode == 0 and 'Success' in installed.stdout,
               (candidates[0].name + (' (replaced a build with another signature)' if replaced else ''))
               if installed.returncode == 0 else installed.stderr.strip()[-200:])
        dump = adb('shell', 'dumpsys', 'package', package).stdout
        code = re.search(r'versionCode=(\d+)', dump)
        name = re.search(r'versionName=(\S+)', dump)
        actual = (name.group(1) if name else None, int(code.group(1)) if code else None)
        report(f'{flavor} identity', actual == (version_name, version_code), f'{package} {actual[0]} ({actual[1]})')

    services = adb('shell', 'cmd', 'package', 'query-services', '--brief', '-a', ACTION).stdout.split()
    ours = sorted(service.split('/')[0] for service in services if service.startswith(BASE_PACKAGE))
    report('discovery', all(package in ours for package in packages.values()),
           f'{len(ours)} {BASE_PACKAGE}* services among {sum("/" in s for s in services)} {ACTION} services')

    runs = []
    for index, flavor in enumerate(flavors):
        _, id_suffix, _ = FLAVORS[flavor]
        engine_id = BASE_PLUGIN_ID + id_suffix
        variants = MATRIX if index == 0 else MATRIX[:1]
        for label, slim, nnapi in variants:
            runs.append({'id': f'{flavor} {label}', 'flavor': flavor, 'sample': flavor, 'file': samples[flavor]['file'],
                         'repeat': args.repeat, 'options': {'engineId': engine_id, 'useSlim': slim, 'useOpenCL': nnapi}})
        if args.cls and flavor == 'zh':
            runs.append({'id': 'zh rotated useCls', 'flavor': flavor, 'sample': 'zh-rotated', 'info': True,
                         'file': samples['zh-rotated']['file'], 'repeat': 2,
                         'options': {'engineId': engine_id, 'useCls': True}})

    remote_dir = f'/sdcard/Android/data/{args.host}/files'
    files = sorted({run['file'] for run in runs})
    remote = [f'{remote_dir}/{NAME}{suffix}' for suffix in ('.js', '.json', '.json.part')]
    remote += [f'{remote_dir}/{name}' for name in files]
    config = {'name': NAME, 'packages': list(packages.values()), 'pluginCenter': PLUGIN_CENTER,
              'runs': [{key: run[key] for key in ('id', 'file', 'repeat', 'options')} for run in runs]}
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
        adb('shell', 'am', 'start', '-n', f'{args.host}/{RUN_ACTIVITY}', '-e', 'path', f'{remote_dir}/{NAME}.js')
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

        # Each engine (re)creation logs one line, in the order of that flavor's runs.
        ready = {}
        for flavor, package in packages.items():
            pid = adb('shell', 'pidof', package).stdout.strip()
            lines = adb('logcat', '-d', '-T', since, '--pid', pid, '-s', 'ORTSessionManager:*').stdout if pid else ''
            ready[flavor] = [match.groups() for match in READY.finditer(lines)]

        for flavor, package in packages.items():
            label = result['labels'].get(package)
            report(f'{flavor} label', label == FLAVORS[flavor][2], label)
        baseline = None
        for run, entry in zip(runs, result['runs']):
            provider = ready[run['flavor']].pop(0) if ready[run['flavor']] else None
            if 'error' in entry or not entry.get('times'):
                report(run['id'], False, entry.get('error', 'no result'))
                continue
            scores = line_similarity(samples[run['sample']]['lines'], entry['texts'])
            matched = sum(score >= args.min_similarity for score in scores)
            warm = entry['times'][1:] or entry['times']
            value = (f'lines {matched}/{len(scores)} (min similarity {min(scores):.2f}), '
                     f'cold {entry["times"][0]} ms, warm median {statistics.median(warm):.0f} ms, '
                     f'provider {provider[0] if provider else "?"}' +
                     (f' (cls {provider[2]}, load {provider[1]} ms)' if provider else ''))
            if run['id'] == 'zh fp32/cpu':
                baseline = entry['texts']
            elif run['flavor'] == 'zh' and baseline is not None and not run.get('info'):
                value += f', same text as fp32/cpu: {"yes" if entry["texts"] == baseline else "no"}'
            passed = matched == len(scores)
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
