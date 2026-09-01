******

### リリース履歴

******

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
