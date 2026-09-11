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

# v1.0.1

###### 2026/09/11

* `改善` 64 ビットのネイティブライブラリの 16 KB ページアラインメントをビルド時に検証, manifest 契約の検査と JSON レポートに対応

# v1.0.0

###### 2026/09/01

* `追加` Paddle OCR (PP-OCRv3) プラグインサービス, プラグイン ID `paddle-ocr-pp-ocrv3`, エンジン `paddle-ocr`, バリアント `v3`
* `追加` `org.autojs.plugin.PADDLE_OCR` によるプラグインの検出と呼び出しをサポート
* `追加` スクリーンショット, ローカル画像ファイル, RAW ARGB_8888 画像入力に対する `ocr.paddle.recognizeText(image)` テキスト認識と `ocr.paddle.detect(image)` テキスト検出をサポート
* `追加` PaddleOCR PP-OCRv3 CPU モデルを同梱し, Paddle Lite と OpenCV 4.8.0 で実行
* `追加` プラグイン情報, 使用手順, README, CHANGELOG の多言語リソース: スペイン語/フランス語/ロシア語/アラビア語/日本語/韓国語/英語/簡体中国語/香港繁体中国語/台湾繁体中国語
* `改善` `arm64-v8a`/`armeabi-v7a` と `universal` パッケージを含む ABI 別 APK ビルドをサポート
* `改善` リリース APK ファイル名にプロジェクト名, バージョン番号, ABI バリアントを含める
* `改善` README のレイアウトと Gradle プラットフォームのバージョン管理方式を統一

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
