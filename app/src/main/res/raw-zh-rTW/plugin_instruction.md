使用 Paddle OCR 識別螢幕截圖中的文字內容:

```js
/* 完整寫法. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* 簡寫. */

ocr.paddle.recognizeText();

/* 極簡. */

ocr.paddle();
```

使用 Paddle OCR 識別本地影像檔案中的文字內容 (以 `test.png` 為例):

```js
/* 完整寫法. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* 簡寫. */

ocr.paddle.recognizeText("test.png");

/* 極簡. */

ocr.paddle("test.png");
```

選擇語種包並設定辨識選項 (`profile` 與 `useCls` 需要 AutoJs6 6.8.0 或更新版本):

```js
let img = images.read("test.png");

/* 使用日文語種包. */

ocr.paddle(img, { profile: "ja" });

/* 辨識前判斷文字方向, 可辨識旋轉 180 度的文字 (預設關閉). */

ocr.paddle(img, { useCls: true });

/* useOpenCL 在 ONNX Runtime 版映射為 NNAPI, 無法使用時退回 CPU. */

ocr.paddle(img, { useOpenCL: true });
```

更多使用方式, 可參閱 AutoJs6 應用文件的 [光學字元識別 (OCR)](https://docs.autojs6.com/#/ocr) 章節.