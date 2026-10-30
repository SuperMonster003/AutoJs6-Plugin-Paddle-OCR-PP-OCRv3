Используйте Paddle OCR для распознавания текстового содержимого на снимке экрана:

```js
/* Полная форма. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* Краткая форма. */

ocr.paddle.recognizeText();

/* Минимальная форма. */

ocr.paddle();
```

Используйте Paddle OCR для распознавания текстового содержимого в локальном файле изображения (на примере `test.png`):

```js
/* Полная форма. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* Краткая форма. */

ocr.paddle.recognizeText("test.png");

/* Минимальная форма. */

ocr.paddle("test.png");
```

Выбор языкового пакета и параметров распознавания (`profile` и `useCls` требуют AutoJs6 6.8.0 или новее):

```js
let img = images.read("test.png");

/* Использовать японский пакет. */

ocr.paddle(img, { profile: "ja" });

/* Сначала определить направление текста, чтобы читать и текст, повёрнутый на 180 градусов (по умолчанию выключено). */

ocr.paddle(img, { useCls: true });

/* useOpenCL в версии ONNX Runtime сопоставлен с NNAPI и возвращается на CPU, если NNAPI недоступен. */

ocr.paddle(img, { useOpenCL: true });
```

Другие способы использования см. в разделе [Оптическое распознавание символов (OCR)](https://docs.autojs6.com/#/ocr)
документации AutoJs6.