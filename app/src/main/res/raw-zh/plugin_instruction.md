使用 Paddle OCR 识别屏幕截图中的文本内容:

```js
/* 完整写法. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* 简写. */

ocr.paddle.recognizeText();

/* 极简. */

ocr.paddle();
```

使用 Paddle OCR 识别本地图像文件中的文本内容 (以 `test.png` 为例):

```js
/* 完整写法. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* 简写. */

ocr.paddle.recognizeText("test.png");

/* 极简. */

ocr.paddle("test.png");
```

选择语种包并设置识别选项 (`profile` 与 `useCls` 需要 AutoJs6 6.8.0 或更高版本):

```js
let img = images.read("test.png");

/* 使用日文语种包. */

ocr.paddle(img, { profile: "ja" });

/* 识别前判断文字方向, 可识别旋转 180 度的文字 (默认关闭). */

ocr.paddle(img, { useCls: true });

/* useOpenCL 在 ONNX Runtime 版映射为 NNAPI, 不可用时回退 CPU. */

ocr.paddle(img, { useOpenCL: true });
```

更多使用方式, 可参阅 AutoJs6 应用文档的 [光学字符识别 (OCR)](https://docs.autojs6.com/#/ocr) 章节.