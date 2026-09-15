<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>AutoJs6 用 Paddle OCR PP-OCRv3 テキスト認識プラグイン</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### 言語

******

現在の README.md は次の言語をサポートします:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- 日本語 [ja] # 現在
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### 概要

******

AutoJs6 Paddle OCR (PP-OCRv3) プラグインは PaddleOCR PP-OCRv3 を利用した光学文字認識を AutoJs6 に追加し, スクリーンショット, ローカル画像ファイル, RAW 画像入力をサポートします.

******

### 機能

******

- `paddle-ocr-pp-ocrv3` プラグインサービスを提供し, プラグイン ID は `paddle-ocr-pp-ocrv3` です.
- AutoJs6 の `ocr.paddle.recognizeText(image)` と `ocr.paddle.detect(image)` をサポートします.
- スクリーンショット, ローカル画像ファイル, RAW ARGB_8888 画像入力をサポートします.
- プラグイン情報, 使用手順, README, CHANGELOG はスペイン語/フランス語/ロシア語/アラビア語/日本語/韓国語/英語/簡体中国語/香港繁体中国語/台湾繁体中国語をサポートします.
- PaddleOCR PP-OCRv3, Paddle Lite, OpenCV 4.8.0 に基づきます.
- 画像は最大 16777216 ピクセルまで, 生画像バッファーは 64 MiB まで対応
- エンコード済み画像は 64 MiB まで対応し ファイル記述子とパイプを使用できます

******

### 使用例

******

スクリーンショット内のテキスト内容を認識します:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

ローカル画像ファイル内のテキスト内容を認識します. `test.png` を例にします:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

ショートカット形式も使用できます:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

******

### API メソッド

******

よく使う OCR API は次のとおりです:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` はデフォルトで現在のスクリーンショットを認識し, `ocr.paddle(path)` はローカル画像ファイルを認識します.

******

### リリース履歴

******

# v1.0.4

###### 2026/09/13

* `修正` 初期化時の文字列変換で JNI 一時参照の解放が不完全になる問題, および JNI 例外発生時に初期化を速やかに中止する処理 _[`issue #575`](http://issues.autojs6.com/575)_
* `修正` プラグインセンターのバージョンと ABI 情報がインストール済み APK と一致
* `修正` エンコード済み画像は 64 MiB まで対応し ファイル記述子とパイプを使用できます
* `修正` バージョン日付は英語の統一形式で表示されます
* `改善` ダウンロード用ファイルの作成前に, リリース APK のバージョン, 署名, バリアントの完全性を検証
* `改善` 画像は最大 16777216 ピクセルまで, 生画像バッファーは 64 MiB まで対応

# v1.0.3

###### 2026/09/12

* `修正` プロセス初回の文字検出で 1000 x 320 のような高さの小さい画像を使うと Paddle Lite がクラッシュ (SIGSEGV) していた問題を修正; 初回の実検出前に 960 x 960 の空白画像で検出器を一度ウォームアップするようにした

# v1.0.2

###### 2026/09/12

* `修正` Paddle OCR のネイティブ依存関係のクリーンアップ設定が初期化されていない場合に `clean` タスクが失敗する問題
* `改善` OpenCV 4.8.0 ネイティブライブラリを NDK r28c (Clang 19.0.1) 再ビルド版に同期 (donor: AutoJs6-Plugin-OpenCV); 4 つの ABI の `libopencv_java4.so` は 16 KB `PT_LOAD` アラインメントを維持し provenance マニフェストを同梱

##### その他のリリース履歴は次を参照してください

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ja.md)

******

### ビルド

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Release ビルド:

```powershell
.\gradlew.bat :app:assembleRelease
```

ビルドパラメータは `version.properties` から取得され, 現在の最小 SDK は 24, ターゲット SDK は 36 です.

******

### リソース構成

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` はローカライズされたプラグイン説明を提供します; `plugin_instruction.md` はホスト側に表示されるプラグイン使用手順を提供します. README と CHANGELOG は `.python/generate_markdown.py` により JSON ソースファイルから生成されます.

******

### 関連リンク

******

- AutoJs6 OCR ドキュメント: https://docs.autojs6.com/#/ocr
- PaddleOCR 公式プロジェクト: https://github.com/PaddlePaddle/PaddleOCR
- Paddle Lite 公式プロジェクト: https://github.com/PaddlePaddle/Paddle-Lite
- OpenCV 公式サイト: https://opencv.org/


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
