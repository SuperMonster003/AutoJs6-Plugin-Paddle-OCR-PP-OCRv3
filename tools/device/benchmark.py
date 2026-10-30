"""Benchmark this plugin (and Paddle Lite 1.1.0) on a device with the image set of roadmap D34.

The images come from tools/device/make_benchmark_images.py (.bak/visual/benchmark/). A script run by
the AutoJs6 host binds each plugin service directly (org.autojs.plugin.PADDLE_OCR) and calls
IOcrPlugin.detect with an encoded PNG, so the times exclude the host's plugin selection; each run
makes --warmup calls (the first one includes any engine load) and then --repeat timed calls.

Runs, all on the CPU execution provider with --threads threads unless noted:
  <flavor> fp32 / slim   every image of that flavor (the host's paddle_ocr_test.png counts as zh)
  zh fp32 / lite fp32 / lite slim
                         with --lite, every zh and en image (Paddle Lite 1.1.0 is the Chinese
                         PP-OCRv3 model, which also reads Latin text); the plugins must be installed
                         already (tools/device/check_device.py --lite 1.1.0)
  <first flavor> fp32/nnapi
                         with --nnapi, the first flavor's images with useOpenCL true

Printed per run: lines matched against the ground truth (similarity >= --min-similarity), result
boxes, median wall time of the binder call and the plugin's own det / rec / total times. Printed per
pair: the line consistency, i.e. boxes matched by IoU >= 0.5 whose texts are equal (spaces ignored)
over the larger box count, and the rec time change. The summaries apply the pass lines of P4.2
(Paddle Lite vs ONNX Runtime fp32 consistency >= 95%) and P4.3 (slim vs fp32 consistency >= 95% and
a lower total rec time). Recognized text is only written to --json.
"""

import argparse
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_device import (ACTION, BASE_PACKAGE, FLAVORS, LITE_PACKAGE, line_similarity, prepare_host_files,  # noqa: E402
                          run_host_file)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IMAGES = ROOT / '.bak' / 'visual' / 'benchmark'
NAME = 'ppocrv3-benchmark'
MIN_CONSISTENCY = 0.95

HOST_SCRIPT = '''\
'use strict';
let CONFIG = __CONFIG__;
let dir = context.getExternalFilesDir(null).getAbsolutePath();
let api = Packages.org.autojs.plugin.paddle.ocr.api;
let result = { runs: [] };
let bound = {};

function bind(name) {
    if (bound[name]) {
        return bound[name].plugin;
    }
    let latch = new java.util.concurrent.CountDownLatch(1);
    let holder = {};
    let connection = new android.content.ServiceConnection({
        onServiceConnected: function (component, binder) {
            holder.binder = binder;
            latch.countDown();
        },
        onServiceDisconnected: function (component) {
        },
    });
    let intent = new android.content.Intent(CONFIG.action).setPackage(name);
    if (!context.bindService(intent, connection, android.content.Context.BIND_AUTO_CREATE)) {
        throw new Error('bindService returned false for ' + name);
    }
    if (!latch.await(30, java.util.concurrent.TimeUnit.SECONDS)) {
        throw new Error('no service connection from ' + name + ' within 30 s');
    }
    bound[name] = { connection: connection, plugin: api.IOcrPlugin.Stub.asInterface(holder.binder) };
    return bound[name].plugin;
}

function extraTime(extras, key) {
    return extras !== null && extras.containsKey(key) ? Number(extras.getLong(key)) : null;
}

CONFIG.runs.forEach(function (run) {
    let entry = { id: run.id, calls: [] };
    try {
        let plugin = bind(run.package);
        let file = new java.io.File(files.join(dir, run.file));
        let total = CONFIG.warmup + CONFIG.repeat;
        for (let i = 0; i < total; i += 1) {
            let options = new api.OcrOptions();
            options.cpuThreadNum = CONFIG.threads;
            options.useSlim = run.slim;
            options.useOpenCL = run.nnapi;
            options.detLongSize = 0;
            options.scoreThreshold = -1;
            options.extras = new android.os.Bundle();
            let fd = android.os.ParcelFileDescriptor.open(file, android.os.ParcelFileDescriptor.MODE_READ_ONLY);
            let list;
            let start = java.lang.System.nanoTime();
            try {
                list = plugin.detect(fd, options);
            } finally {
                fd.close();
            }
            let call = { wall: (java.lang.System.nanoTime() - start) / 1e6, boxes: Number(list.size()) };
            if (list.size() > 0) {
                let extras = list.get(0).extras;
                call.det = extraTime(extras, 'detectionTimeMs');
                call.cls = extraTime(extras, 'classificationTimeMs');
                call.rec = extraTime(extras, 'recognitionTimeMs');
                call.total = extraTime(extras, 'totalTimeMs');
                call.load = extraTime(extras, 'coldLoadTimeMs');
                call.provider = extras !== null && extras.containsKey('executionProvider')
                    ? String(extras.getString('executionProvider')) : null;
            }
            entry.calls.push(call);
            if (i === total - 1) {
                entry.results = [];
                for (let j = 0; j < list.size(); j += 1) {
                    let item = list.get(j);
                    let bounds = item.bounds;
                    entry.results.push({
                        text: String(item.text),
                        confidence: Number(item.confidence),
                        bounds: [Number(bounds.left), Number(bounds.top), Number(bounds.right), Number(bounds.bottom)],
                    });
                }
            }
        }
    } catch (e) {
        entry.error = String(e);
    }
    result.runs.push(entry);
    if (CONFIG.pause > 0) {
        sleep(CONFIG.pause * 1000);
    }
});
Object.keys(bound).forEach(function (name) {
    try {
        context.unbindService(bound[name].connection);
    } catch (e) {
        // The service may already be gone.
    }
});
let out = files.join(dir, CONFIG.name + '.json');
files.write(out + '.part', JSON.stringify(result));
new java.io.File(out + '.part').renameTo(new java.io.File(out));
'''


def normalize(text):
    return ''.join(text.split())


def iou(a, b):
    width = min(a[2], b[2]) - max(a[0], b[0])
    height = min(a[3], b[3]) - max(a[1], b[1])
    if width <= 0 or height <= 0:
        return 0.0
    inter = width * height
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def consistency(reference, candidate):
    """(equal boxes, larger box count, differences) of two result lists, boxes matched greedily by IoU."""
    pairs = sorted(((iou(a['bounds'], b['bounds']), i, j) for i, a in enumerate(reference)
                    for j, b in enumerate(candidate)), reverse=True)
    used_reference, used_candidate, differences = set(), set(), []
    equal = 0
    for score, i, j in pairs:
        if score < 0.5:
            break
        if i in used_reference or j in used_candidate:
            continue
        used_reference.add(i)
        used_candidate.add(j)
        if normalize(reference[i]['text']) == normalize(candidate[j]['text']):
            equal += 1
        else:
            differences.append([reference[i]['text'], candidate[j]['text']])
    differences += [[reference[i]['text'], None] for i in range(len(reference)) if i not in used_reference]
    differences += [[None, candidate[j]['text']] for j in range(len(candidate)) if j not in used_candidate]
    return equal, max(len(reference), len(candidate)), differences


def median(values):
    values = [value for value in values if value is not None]
    return statistics.median(values) if values else None


def ms(value):
    return '?' if value is None else f'{value:.0f}'


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--host', default='org.autojs.autojs6', help='AutoJs6 host package')
    parser.add_argument('--images', type=Path, default=DEFAULT_IMAGES, help='directory with images.json')
    parser.add_argument('--flavor', action='append', choices=sorted(FLAVORS), help='repeatable; defaults to all')
    parser.add_argument('--image', action='append', help='repeatable file name from images.json; defaults to all '
                                                        '(Paddle Lite 1.1.0 crashes on a mix of small and large images)')
    parser.add_argument('--lite', action='store_true', help='also compare Paddle Lite 1.1.0 with zh fp32')
    parser.add_argument('--nnapi', action='store_true', help='also run the first flavor fp32 with useOpenCL true')
    parser.add_argument('--threads', type=int, default=4)
    parser.add_argument('--warmup', type=int, default=1)
    parser.add_argument('--repeat', type=int, default=10)
    parser.add_argument('--pause', type=float, default=2, help='seconds between runs')
    parser.add_argument('--min-similarity', type=float, default=0.8)
    parser.add_argument('--timeout', type=int, default=3600, help='seconds to wait for the host script')
    parser.add_argument('--json', type=Path, help='save the runs (including recognized text) and pairs here')
    args = parser.parse_args()

    images = json.loads((args.images / 'images.json').read_text(encoding='utf-8'))['images']
    if args.image:
        unknown = set(args.image) - {image['file'] for image in images}
        if unknown:
            parser.error(f'not in images.json: {", ".join(sorted(unknown))}')
        images = [image for image in images if image['file'] in args.image]
    flavors = args.flavor or [flavor for flavor in FLAVORS if any(image['flavor'] == flavor for image in images)]

    def adb(*command, timeout=120):
        return subprocess.run([args.adb, '-s', args.serial, *command], capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=timeout)

    def temperature():
        for line in adb('shell', 'dumpsys', 'battery').stdout.splitlines():
            if line.strip().startswith('temperature:'):
                return f"{int(line.split(':')[1]) / 10:.1f} C"
        return '?'

    abi = adb('shell', 'getprop', 'ro.product.cpu.abilist').stdout.strip().split(',')[0]
    model = adb('shell', 'getprop', 'ro.product.model').stdout.strip()
    api = adb('shell', 'getprop', 'ro.build.version.sdk').stdout.strip()
    print(f'Device: {model}, API {api}, {abi}, {args.threads} threads, '
          f'{args.warmup} warm-up + {args.repeat} timed calls per run, battery {temperature()}', flush=True)

    packages = {flavor: BASE_PACKAGE + FLAVORS[flavor][0] for flavor in flavors}
    if args.lite:
        packages['lite'] = LITE_PACKAGE
    missing = [package for package in packages.values() if not adb('shell', 'pm', 'path', package).stdout.strip()]
    if missing:
        print(f'FAIL packages: not installed: {", ".join(missing)}', flush=True)
        return 1

    # Runs are grouped by package and model so each engine loads once per group.
    runs = []

    def add(engine, model_name, image, slim, nnapi):
        runs.append({'id': f'{engine} {model_name} {image["file"][:-4]}', 'engine': engine, 'model': model_name,
                     'image': image, 'package': packages[engine], 'file': image['file'], 'slim': slim, 'nnapi': nnapi})

    lite_images = [image for image in images if image['flavor'] in ('zh', 'en')]
    for flavor in flavors:
        own = [image for image in images if image['flavor'] == flavor]
        extra = [image for image in lite_images if image['flavor'] != 'zh'] if args.lite and flavor == 'zh' else []
        for image in own + extra:
            add(flavor, 'fp32', image, False, False)
        for image in own:
            add(flavor, 'slim', image, True, False)
        if args.nnapi and flavor == flavors[0]:
            for image in own:
                add(flavor, 'fp32/nnapi', image, False, True)
    if args.lite:
        for model_name, slim in (('fp32', False), ('slim', True)):
            for image in lite_images:
                add('lite', model_name, image, slim, False)

    remote_dir = f'/sdcard/Android/data/{args.host}/files'
    files = sorted({run['file'] for run in runs})
    remote = [f'{remote_dir}/{NAME}{suffix}' for suffix in ('.js', '.json', '.json.part')]
    remote += [f'{remote_dir}/{name}' for name in files]
    config = {'name': NAME, 'action': ACTION, 'threads': args.threads, 'warmup': args.warmup, 'repeat': args.repeat,
              'pause': args.pause,
              'runs': [{key: run[key] for key in ('id', 'package', 'file', 'slim', 'nnapi')} for run in runs]}
    unusable = prepare_host_files(adb, args.host, remote_dir)
    if unusable:
        print(f'FAIL host script: {unusable}', flush=True)
        return 1
    try:
        adb('shell', 'rm', '-f', *remote)
        for name in files:
            adb('push', str(args.images / name), f'{remote_dir}/{name}')
        with tempfile.TemporaryDirectory() as temp:
            script = Path(temp) / f'{NAME}.js'
            script.write_text(HOST_SCRIPT.replace('__CONFIG__', json.dumps(config)), encoding='utf-8')
            pushed = adb('push', str(script), f'{remote_dir}/{NAME}.js')
        if pushed.returncode != 0:
            print(f'FAIL host script: push failed: {pushed.stderr.strip()}', flush=True)
            return 1
        started = time.monotonic()
        run_host_file(adb, args.host, f'{NAME}.js')
        result = None
        while result is None and time.monotonic() < started + args.timeout:
            time.sleep(5)
            text = adb('shell', 'cat', f'{remote_dir}/{NAME}.json')
            if text.returncode == 0 and text.stdout.strip():
                result = json.loads(text.stdout)
        if result is None:
            print(f'FAIL host script: no result within {args.timeout} s', flush=True)
            return 1
    finally:
        adb('shell', 'rm', '-f', *remote)
    print(f'Host script finished in {time.monotonic() - started:.0f} s, battery {temperature()}', flush=True)

    entries = {}
    failures = 0
    for run, entry in zip(runs, result['runs']):
        if 'error' in entry:
            print(f"FAIL {run['id']}: {entry['error']}", flush=True)
            failures += 1
            continue
        timed = entry['calls'][args.warmup:] or entry['calls']
        texts = [item['text'] for item in entry['results']]
        lines = run['image']['lines']
        summary = {key: median(call.get(key) for call in timed) for key in ('wall', 'det', 'cls', 'rec', 'total')}
        summary['load'] = entry['calls'][0].get('load')
        summary['provider'] = next((call['provider'] for call in timed if call.get('provider')), None)
        if lines:
            scores = line_similarity(lines, texts)
            summary['matched'] = sum(score >= args.min_similarity for score in scores)
            summary['exact'] = sum(score == 1.0 for score in scores)
            summary['lines'] = len(lines)
        entries[run['id']] = {**run, 'image': run['image']['file'], 'summary': summary, 'results': entry['results'],
                              'calls': entry['calls']}
        accuracy = f"lines {summary['matched']}/{summary['lines']} (exact {summary['exact']}), " if lines else ''
        print(f"RUN {run['id']}: {accuracy}{len(texts)} boxes, wall {ms(summary['wall'])} ms, "
              f"det {ms(summary['det'])}, rec {ms(summary['rec'])}, total {ms(summary['total'])} ms, "
              f"load {ms(summary['load'])} ms, provider {summary['provider'] or '?'}", flush=True)

    pairs = []

    def pair(kind, reference_id, candidate_id):
        reference, candidate = entries.get(reference_id), entries.get(candidate_id)
        if reference is None or candidate is None:
            return
        equal, count, differences = consistency(reference['results'], candidate['results'])
        rec = (reference['summary']['rec'], candidate['summary']['rec'])
        wall = (reference['summary']['wall'], candidate['summary']['wall'])
        pairs.append({'kind': kind, 'reference': reference_id, 'candidate': candidate_id, 'image': reference['image'],
                      'equal': equal, 'count': count, 'rec': rec, 'wall': wall, 'differences': differences})
        change = (f', rec {ms(rec[0])} -> {ms(rec[1])} ms' if None not in rec else '') + \
                 f', wall {ms(wall[0])} -> {ms(wall[1])} ms'
        print(f"PAIR {kind} {reference['image'][:-4]}: equal {equal}/{count} "
              f"({equal / count * 100 if count else 100:.1f}%){change}", flush=True)

    for run in runs:
        if run['model'] == 'slim' and run['engine'] != 'lite':
            pair('slim vs fp32', run['id'].replace(' slim ', ' fp32 '), run['id'])
    for run in runs:
        if run['engine'] == 'lite':
            pair(f"lite {run['model']} vs ort fp32", f"zh fp32 {run['file'][:-4]}", run['id'])
        if run['model'] == 'fp32/nnapi':
            pair('nnapi vs cpu', run['id'].replace(' fp32/nnapi ', ' fp32 '), run['id'])

    results = []

    def judge(kind, need_faster):
        selected = [item for item in pairs if item['kind'] == kind]
        if not selected:
            return
        equal = sum(item['equal'] for item in selected)
        count = sum(item['count'] for item in selected)
        rate = equal / count if count else 1.0
        rec = [sum(item['rec'][side] for item in selected if None not in item['rec']) for side in (0, 1)]
        wall = [sum(item['wall'][side] for item in selected) for side in (0, 1)]
        passed = rate >= MIN_CONSISTENCY and (not need_faster or rec[1] < rec[0])
        results.append(passed)
        print(f"{'PASS' if passed else 'FAIL'} {kind}: equal {equal}/{count} ({rate * 100:.1f}%, line >= "
              f"{MIN_CONSISTENCY * 100:.0f}%), rec sum {rec[0]:.0f} -> {rec[1]:.0f} ms "
              f"({(rec[1] - rec[0]) / rec[0] * 100 if rec[0] else 0:+.1f}%), wall sum {wall[0]:.0f} -> {wall[1]:.0f} ms "
              f"({(wall[1] - wall[0]) / wall[0] * 100 if wall[0] else 0:+.1f}%)", flush=True)

    judge('slim vs fp32', True)
    judge('lite fp32 vs ort fp32', False)
    for kind in ('lite slim vs ort fp32', 'nnapi vs cpu'):
        selected = [item for item in pairs if item['kind'] == kind]
        if selected:
            equal = sum(item['equal'] for item in selected)
            count = sum(item['count'] for item in selected)
            wall = [sum(item['wall'][side] for item in selected) for side in (0, 1)]
            print(f'INFO {kind}: equal {equal}/{count} ({equal / count * 100 if count else 100:.1f}%), '
                  f'wall sum {wall[0]:.0f} -> {wall[1]:.0f} ms', flush=True)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({'device': {'model': model, 'api': api, 'abi': abi}, 'runs': entries,
                                         'pairs': pairs}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{len(entries)}/{len(runs)} runs finished, {sum(results)}/{len(results)} pass lines met', flush=True)
    return 0 if not failures and all(results) else 1


if __name__ == '__main__':
    sys.exit(main())
