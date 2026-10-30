Use Paddle OCR to recognize text content in a screenshot:

```js
/* Full form. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* Short form. */

ocr.paddle.recognizeText();

/* Minimal form. */

ocr.paddle();
```

Use Paddle OCR to recognize text content in a local image file (using `test.png` as an example):

```js
/* Full form. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* Short form. */

ocr.paddle.recognizeText("test.png");

/* Minimal form. */

ocr.paddle("test.png");
```

Choose a language package and set recognition options (`profile` and `useCls` need AutoJs6 6.8.0 or later):

```js
let img = images.read("test.png");

/* Use the Japanese package. */

ocr.paddle(img, { profile: "ja" });

/* Check the text direction first so text rotated by 180 degrees can be read (off by default). */

ocr.paddle(img, { useCls: true });

/* useOpenCL maps to NNAPI in the ONNX Runtime edition and falls back to the CPU when NNAPI is unavailable. */

ocr.paddle(img, { useOpenCL: true });
```

For more usage examples, refer to the [Optical Character Recognition (OCR)](https://docs.autojs6.com/#/ocr)
section in the AutoJs6 documentation.