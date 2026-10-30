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

AutoJs6 Paddle OCR (PP-OCRv3) プラグインは PaddleOCR PP-OCRv3 と ONNX Runtime を利用した光学文字認識を AutoJs6 に追加し, スクリーンショット, ローカル画像ファイル, RAW 画像入力をサポートします. 2.0.0 から推論エンジンを Paddle Lite から ONNX Runtime に切り替え, 4 つの ABI に対応し, 認識する言語ごとに 5 つの言語パッケージに分かれています.

> **Paddle Lite 版**: 1.0.x の Paddle Lite 実装は [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) に改名して別途公開されています (プラグイン ID `paddle-ocr-pp-ocrv3-paddle-lite`, バリアント `v3-paddle-lite`). arm64-v8a と armeabi-v7a のみに対応し, このプラグインと同時にインストールできます.

******

### 機能

******

- 簡体字中国語, 英語, 繁体字中国語, 日本語, 韓国語の 5 つの言語パッケージを提供します. 簡体字中国語パッケージは 1.0.x のパッケージ名とプラグイン ID `paddle-ocr-pp-ocrv3` を引き継ぎ, すべてのパッケージのエンジンは `paddle-ocr`, バリアントは `v3` です.
- AutoJs6 の `ocr.paddle.recognizeText(image)` と `ocr.paddle.detect(image)` をサポートします.
- スクリーンショット, ローカル画像ファイル, RAW ARGB_8888 画像入力をサポートします.
- プラグイン情報, 使用手順, README, CHANGELOG はスペイン語/フランス語/ロシア語/アラビア語/日本語/韓国語/英語/簡体中国語/香港繁体中国語/台湾繁体中国語をサポートします.
- PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1, OpenCV 4.8.0 に基づき, arm64-v8a, armeabi-v7a, x86_64, x86 の 4 つの ABI に対応します.
- `useSlim: true` は ONNX Runtime の動的量子化 (int8) で生成した検出モデルと認識モデルを使います.
- `useCls: true` は認識の前に文字の向きを判定し, 180 度回転した文字も認識できます. 既定では無効で, 1.0.x と同じです.
- `useOpenCL` は ONNX Runtime 版では NNAPI に対応付けられます. Android 8.1 (API 27) 以降では NNAPI 実行プロバイダーを使い, それより前のバージョンや NNAPI の初期化に失敗した場合は CPU に戻ります. 速くなるかどうかは端末によって異なります.
- 画像は最大 16777216 ピクセルまで, 生画像バッファーは 64 MiB まで対応
- エンコード済み画像は 64 MiB まで対応し ファイル記述子とパイプを使用できます

******

### 言語パッケージ

******

言語パッケージはそれぞれ独立した APK で, 複数を同時にインストールできます:

| 言語 | `profile` | プラグイン ID | パッケージ名 | APK ファイル名 |
| --- | --- | --- | --- | --- |
| 簡体字中国語 | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| 英語 | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| 繁体字中国語 | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| 日本語 | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| 韓国語 | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

認識したい文字に合わせて言語パッケージを選んでください. 簡体字中国語パッケージは英字と数字も認識でき, 既定のおすすめです. 繁体字中国語, 日本語, 韓国語の文字には対応する言語パッケージを, 英語だけなら英語パッケージもインストールできます. 各言語パッケージには ABI ごとに `arm64-v8a` (ほとんどのスマートフォン), `armeabi-v7a`, `x86_64`, `x86`, `universal` (4 つの ABI をすべて含み, 最も大きい) の 5 つの APK があり, 端末に合うものを 1 つだけインストールします.

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

言語パッケージとオプションを指定します:

```js
let img = images.read("test.png");
/* 日本語パッケージを使います. */
ocr.paddle(img, { profile: "ja" });
/* プラグイン ID で韓国語パッケージを指定します. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* 量子化モデルを使い, 文字の向きの分類を有効にします. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL は ONNX Runtime 版では NNAPI に対応付けられます. */
ocr.paddle(img, { useOpenCL: true });
/* Paddle Lite 版プラグインを使います. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

`profile` による言語パッケージの選択と `useCls` オプションには AutoJs6 6.8.0 以降が必要です. それより前のホストは `profile` で選択せず, `useCls` も渡しません. 複数の言語パッケージをインストールしている場合は `engineId` で指定してください.

******

### API メソッド

******

よく使う OCR API は次のとおりです:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` はデフォルトで現在のスクリーンショットを認識し, `ocr.paddle(path)` はローカル画像ファイルを認識します.

******

### リリース履歴

******

# v2.0.0

###### 2026/10/30

* `注意` 認識エンジンを Paddle Lite から ONNX Runtime に切り替え, 開発者を SuperMonster003 に変更しました. 従来の Paddle Lite 実装は Paddle OCR (PP-OCRv3 Paddle Lite) として別途公開され (プラグイン ID `paddle-ocr-pp-ocrv3-paddle-lite`, バリアント `v3-paddle-lite`), このプラグインと同時にインストールできます
* `注意` 認識する言語ごとに簡体字中国語, 英語, 繁体字中国語, 日本語, 韓国語の 5 つの言語パッケージに分かれ, それぞれ独立した APK です. 簡体字中国語パッケージは従来のパッケージ名とプラグイン ID を引き継ぎます
* `注意` `profile` による言語パッケージの選択と `useCls` オプションには AutoJs6 6.8.0 以降が必要です. それより前のホストは `profile` で選択せず, `useCls` も渡しません
* `追加` x86_64 と x86 の端末 (エミュレータを含む) に対応し, 合計 4 つの ABI になりました
* `追加` `useCls` オプションを追加しました. 認識の前に文字の向きを判定し, 180 度回転した文字も認識できます. 既定では無効です
* `追加` `useOpenCL` は ONNX Runtime 版では NNAPI に対応付けられます. Android 8.1 以降は NNAPI を使い, それより前のバージョンや NNAPI が使えない場合は CPU に戻ります
* `改善` `useSlim` は ONNX Runtime の動的量子化 (int8) で生成した検出モデルと認識モデルを使うようになりました
* `依存関係` ONNX Runtime Android 1.21.1 を追加し, Paddle Lite を削除
* `依存関係` PaddleOCR PP-OCRv3 モデルを ONNX 形式に変更 (公式推論モデルから変換) し, 英語, 繁体字中国語, 日本語, 韓国語の認識モデルと文字の向きの分類モデルを追加
* `依存関係` OpenCV 4.8.0 を共有ライブラリ libopencv_java4.so で提供するように変更 (PP-OCRv4 プラグインと同じ)

# v1.0.6

###### 2026/10/10

* `注意` 本バージョンをパッケージ化されたアプリで使用するには, ホストに AutoJs6 6.8.0 以降が必要 (古いホストでは OpenCV も同時に選択した場合のみパッケージ化可能)
* `修正` モデルの読み込みや推論でネイティブ例外が発生するとプラグインプロセスが異常終了する問題 (ホストにエラーとして返すように変更)
* `改善` libNative.so が OpenCV のシンボルをエクスポートしなくなり, APK に libopencv_java4.so を同梱しなくなってサイズが縮小し, パッケージ化されたアプリで別バージョンの OpenCV と併用可能
* `依存関係` OpenCV Android AAR 4.8.0 を削除し, 静的リンクする OpenCV Android SDK 4.8.0 のみを使用 (ダウンロード時に SHA-256 を検証)

# v1.0.5

###### 2026/10/05

* `修正` 共有ビルドプラグイン 1.8.3 により, AGP 9.1 での SDK XML v4 解析警告と, JVM 単体テストの組み立て時に APK ネイティブライブラリのアラインメント検証が誤って実行される問題
* `改善` compileSdk と targetSdk を 37 (Android 17) に引き上げ, プラグインの動作は新しいターゲットの影響を受けない
* `改善` Android のアプリ情報アイコンに Icon Studio と共通の図案と明暗の背景色を使用し, プラグインセンターの透明な図案と既存のランチャー設定を維持

##### その他のリリース履歴は次を参照してください

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ja.md)

******

### ビルド

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release ビルド:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

ビルドパラメータは `version.properties` から取得され, 現在の最小 SDK は 24, ターゲット SDK は 37 です. ONNX モデルはリポジトリに含まれません. ビルドの前に上記の `prepare_ppocrv3_assets.py` を実行すると, PaddleOCR 公式モデルをダウンロードして ONNX に変換し, `libs/ppocr-android-sdk/models.provenance.json` と照合します. `--profile` には `zh`, `en`, `zhHant`, `ja`, `ko`, `all` を指定できます. サードパーティのコンポーネントとライセンスは [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md) を参照してください.

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
- ONNX Runtime 公式プロジェクト: https://github.com/microsoft/onnxruntime
- OpenCV 公式サイト: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) プラグイン: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
