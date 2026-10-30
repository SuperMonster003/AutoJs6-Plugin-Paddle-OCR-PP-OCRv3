使用 Paddle OCR 識別屏幕截圖中的文本內容:

```js
/* 完整寫法. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* 簡寫. */

ocr.paddle.recognizeText();

/* 極簡. */

ocr.paddle();
```

使用 Paddle OCR 識別本地圖像文件中的文本內容 (以 `test.png` 為例):

```js
/* 完整寫法. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* 簡寫. */

ocr.paddle.recognizeText("test.png");

/* 極簡. */

ocr.paddle("test.png");
```

選擇語種包並設置識別選項 (`profile` 與 `useCls` 需要 AutoJs6 6.8.0 或更高版本):

```js
let img = images.read("test.png");

/* 使用日文語種包. */

ocr.paddle(img, { profile: "ja" });

/* 識別前判斷文字方向, 可識別旋轉 180 度的文字 (默認關閉). */

ocr.paddle(img, { useCls: true });

/* useOpenCL 在 ONNX Runtime 版映射為 NNAPI, 不可用時回退 CPU. */

ocr.paddle(img, { useOpenCL: true });
```

更多使用方式, 可參閲 AutoJs6 應用文檔的 [光學字符識別 (OCR)](https://docs.autojs6.com/#/ocr) 章節.