Paddle OCR を使って, スクリーンショット内のテキスト内容を認識します:

```js
/* 完全な書き方. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* 簡略形. */

ocr.paddle.recognizeText();

/* 最小形. */

ocr.paddle();
```

Paddle OCR を使って, ローカル画像ファイル内のテキスト内容を認識します (`test.png` を例とします):

```js
/* 完全な書き方. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* 簡略形. */

ocr.paddle.recognizeText("test.png");

/* 最小形. */

ocr.paddle("test.png");
```

言語パッケージと認識オプションを指定します (`profile` と `useCls` には AutoJs6 6.8.0 以降が必要です):

```js
let img = images.read("test.png");

/* 日本語パッケージを使います. */

ocr.paddle(img, { profile: "ja" });

/* 認識の前に文字の向きを判定し, 180 度回転した文字も認識します (既定では無効). */

ocr.paddle(img, { useCls: true });

/* useOpenCL は ONNX Runtime 版では NNAPI に対応付けられ, 使えない場合は CPU に戻ります. */

ocr.paddle(img, { useOpenCL: true });
```

その他の使用方法については, AutoJs6 アプリドキュメントの [光学文字認識 (OCR)](https://docs.autojs6.com/#/ocr)
セクションを参照してください.
