"""Render the P4.2 / P4.3 benchmark image set (roadmap D34) with headless Microsoft Edge.

Two phone-sized screens per language flavor (a light settings list and a dark notes page) are
rendered from HTML with the Windows fonts of that script, plus the host's paddle_ocr_test.png.
The images are not committed: they go to .bak/visual/benchmark/ together with images.json, which
records each file's flavor, ground-truth lines (null for the host image) and SHA-256 for
docs/benchmark.md. tools/device/benchmark.py reads that directory.
"""

import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / '.bak' / 'visual' / 'benchmark'
DEFAULT_HOST_IMAGE = ROOT.parent / 'AutoJs6' / 'plugin-api' / 'paddle-ocr-engine' / 'src' / 'main' / 'res' / 'drawable' / 'paddle_ocr_test.png'
EDGE = Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
WIDTH, HEIGHT, SCALE = 720, 1000, 1.5

# flavor -> (html lang, font stack, settings title, settings rows, notes lines)
SCREENS = {
    'zh': ('zh-CN', "'Microsoft YaHei'", '设置', [
        ('无线网络', '已连接到 Home-5G'),
        ('蓝牙', '已关闭'),
        ('显示与亮度', '自动调节亮度, 深色模式'),
        ('声音与振动', '铃声音量 80%'),
        ('通知', '允许 12 个应用发送通知'),
        ('电池', '剩余 67%, 预计可用 9 小时'),
        ('存储空间', '已使用 48.6 GB, 共 128 GB'),
        ('应用管理', '默认应用, 权限管理'),
        ('关于手机', 'Android 14, 版本号 2026.10'),
    ], [
        '周三下午的会议记录',
        '1. 下周一上午 10:30 发布新版本',
        '2. 文字识别插件需要在五台设备上测试',
        '3. 安装包体积控制在 35 MB 以内',
        '张工: 模拟器的测试结果已经上传',
        '李工: 好的, 我晚上再核对一遍',
        '明天的天气: 多云转晴, 气温 18 - 26 度',
        '提醒: 记得备份手机里的照片和联系人',
        '已读 21:45',
    ]),
    'en': ('en', "'Segoe UI'", 'Settings', [
        ('Network and internet', 'Connected to Home-5G'),
        ('Bluetooth', 'Off'),
        ('Display and brightness', 'Adaptive brightness, Dark theme'),
        ('Sound and vibration', 'Ring volume 80%'),
        ('Notifications', '12 apps can send notifications'),
        ('Battery', '67% remaining, about 9 hours left'),
        ('Storage', '48.6 GB used of 128 GB'),
        ('Apps', 'Default apps, Permission manager'),
        ('About phone', 'Android 14, build 2026.10'),
    ], [
        'Meeting notes, Wednesday afternoon',
        '1. Release the new version on Monday at 10:30',
        '2. Test the text recognition plugin on five devices',
        '3. Keep the package size under 35 MB',
        'Alex: The emulator results are uploaded',
        'Sam: Thanks, I will check them again tonight',
        'Weather tomorrow: cloudy, 18 to 26 degrees',
        'Reminder: back up your photos and contacts',
        'Read 21:45',
    ]),
    'zhHant': ('zh-TW', "'Microsoft JhengHei'", '設定', [
        ('無線網路', '已連線到 Home-5G'),
        ('藍牙', '已關閉'),
        ('顯示與亮度', '自動調整亮度, 深色模式'),
        ('音效與震動', '鈴聲音量 80%'),
        ('通知', '允許 12 個應用程式傳送通知'),
        ('電池', '剩餘 67%, 預計可用 9 小時'),
        ('儲存空間', '已使用 48.6 GB, 共 128 GB'),
        ('應用程式', '預設應用程式, 權限管理'),
        ('關於手機', 'Android 14, 版本號碼 2026.10'),
    ], [
        '週三下午的會議紀錄',
        '1. 下週一上午 10:30 發佈新版本',
        '2. 文字辨識外掛需要在五台裝置上測試',
        '3. 安裝檔大小控制在 35 MB 以內',
        '陳先生: 模擬器的測試結果已經上傳',
        '林小姐: 好的, 我晚上再核對一遍',
        '明天的天氣: 多雲轉晴, 氣溫 18 - 26 度',
        '提醒: 記得備份手機裡的照片和聯絡人',
        '已讀 21:45',
    ]),
    'ja': ('ja', "'Yu Gothic UI', 'Meiryo'", '設定', [
        ('ネットワークとインターネット', 'Home-5G に接続済み'),
        ('Bluetooth', 'オフ'),
        ('ディスプレイと明るさ', '明るさの自動調節, ダークモード'),
        ('音とバイブレーション', '着信音の音量 80%'),
        ('通知', '12 個のアプリが通知を送信できます'),
        ('電池', '残り 67%, あと約 9 時間'),
        ('ストレージ', '128 GB 中 48.6 GB を使用'),
        ('アプリ', 'デフォルトのアプリ, 権限マネージャ'),
        ('デバイス情報', 'Android 14, ビルド番号 2026.10'),
    ], [
        '水曜日の午後の会議メモ',
        '1. 月曜日の午前 10:30 に新しいバージョンを公開',
        '2. 文字認識プラグインを五台の端末でテスト',
        '3. パッケージのサイズは 35 MB 以内にする',
        '田中: エミュレータの結果をアップロードしました',
        '佐藤: ありがとう, 今夜もう一度確認します',
        '明日の天気: 曇りのち晴れ, 気温 18 - 26 度',
        'リマインダー: 写真と連絡先をバックアップ',
        '既読 21:45',
    ]),
    'ko': ('ko', "'Malgun Gothic'", '설정', [
        ('네트워크 및 인터넷', 'Home-5G에 연결됨'),
        ('블루투스', '꺼짐'),
        ('디스플레이 및 밝기', '자동 밝기, 다크 모드'),
        ('소리 및 진동', '벨소리 음량 80%'),
        ('알림', '앱 12개가 알림을 보낼 수 있음'),
        ('배터리', '67% 남음, 약 9시간 사용 가능'),
        ('저장용량', '128 GB 중 48.6 GB 사용'),
        ('애플리케이션', '기본 앱, 권한 관리자'),
        ('휴대전화 정보', 'Android 14, 빌드 번호 2026.10'),
    ], [
        '수요일 오후 회의 메모',
        '1. 월요일 오전 10:30에 새 버전 출시',
        '2. 문자 인식 플러그인을 기기 다섯 대에서 테스트',
        '3. 패키지 크기는 35 MB 이하로 유지',
        '민수: 에뮬레이터 결과를 업로드했어요',
        '지영: 고마워요, 오늘 밤에 다시 확인할게요',
        '내일 날씨: 흐린 뒤 맑음, 기온 18 - 26도',
        '알림: 사진과 연락처를 백업하세요',
        '읽음 21:45',
    ]),
}

SETTINGS_STYLE = '''
body { margin: 0; background: #f6f7f9; color: #1b1c1f; font-family: __FONT__, sans-serif; }
h1 { font-size: 30px; font-weight: 600; margin: 36px 28px 20px; }
.row { background: #ffffff; padding: 14px 28px; border-bottom: 1px solid #e3e5e8; }
.t { font-size: 19px; white-space: nowrap; }
.s { font-size: 15px; color: #6b6f76; margin-top: 5px; white-space: nowrap; }
'''
NOTES_STYLE = '''
body { margin: 0; background: #1e1f22; color: #e8e8ea; font-family: __FONT__, sans-serif; }
.head { font-size: 24px; font-weight: 600; margin: 36px 28px 22px; white-space: nowrap; }
.p { font-size: 18px; margin: 14px 28px; white-space: nowrap; }
.bubble { display: inline-block; padding: 10px 16px; border-radius: 14px; }
.left { background: #2f3136; }
.right { background: #2b6cb0; color: #ffffff; }
.meta { font-size: 14px; color: #9a9ca3; margin: 18px 28px; white-space: nowrap; }
'''


def settings_html(lang, font, title, rows):
    body = [f'<h1>{html.escape(title)}</h1>']
    for name, summary in rows:
        body.append(f'<div class="row"><div class="t">{html.escape(name)}</div>'
                    f'<div class="s">{html.escape(summary)}</div></div>')
    lines = [title] + [line for row in rows for line in row]
    return page(lang, SETTINGS_STYLE.replace('__FONT__', font), body), lines


def notes_html(lang, font, lines):
    head, items, chat, meta = lines[0], lines[1:4], lines[4:6], lines[6:]
    body = [f'<div class="head">{html.escape(head)}</div>']
    body += [f'<div class="p">{html.escape(line)}</div>' for line in items]
    body.append(f'<div class="p"><span class="bubble left">{html.escape(chat[0])}</span></div>')
    body.append(f'<div class="p" style="text-align: right"><span class="bubble right">{html.escape(chat[1])}</span></div>')
    body += [f'<div class="p">{html.escape(line)}</div>' for line in meta[:-1]]
    body.append(f'<div class="meta">{html.escape(meta[-1])}</div>')
    return page(lang, NOTES_STYLE.replace('__FONT__', font), body), list(lines)


def page(lang, style, body):
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{style}</style></head>'
            f'<body>{"".join(body)}</body></html>')


def render(edge, source, target, profile_dir):
    subprocess.run([str(edge), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
                    '--no-default-browser-check', f'--user-data-dir={profile_dir}',
                    f'--force-device-scale-factor={SCALE}', f'--window-size={WIDTH},{HEIGHT}',
                    f'--screenshot={target}', source.as_uri()],
                   check=True, capture_output=True, timeout=120)


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--edge', type=Path, default=EDGE)
    parser.add_argument('--host-image', type=Path, default=DEFAULT_HOST_IMAGE)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    images = []
    target = args.out / 'host-paddle_ocr_test.png'
    shutil.copyfile(args.host_image, target)
    images.append({'file': target.name, 'flavor': 'zh', 'lines': None})
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        for flavor, (lang, font, title, rows, notes) in SCREENS.items():
            for kind, (document, lines) in (('settings', settings_html(lang, font, title, rows)),
                                            ('notes', notes_html(lang, font, notes))):
                source = temp / f'{flavor}-{kind}.html'
                source.write_text(document, encoding='utf-8')
                target = args.out / f'{flavor}-{kind}.png'
                render(args.edge, source, target, temp / 'edge-profile')
                images.append({'file': target.name, 'flavor': flavor, 'lines': lines})
    for image in images:
        image['sha256'] = hashlib.sha256((args.out / image['file']).read_bytes()).hexdigest()
        print(f"{image['file']}: {image['flavor']}, {len(image['lines'] or [])} lines, sha256 {image['sha256'][:16]}")
    (args.out / 'images.json').write_text(json.dumps({'images': images}, ensure_ascii=False, indent=2) + '\n',
                                          encoding='utf-8')
    print(f'{len(images)} images in {args.out}')


if __name__ == '__main__':
    main()
