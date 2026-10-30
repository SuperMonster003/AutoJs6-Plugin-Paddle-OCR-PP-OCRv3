استخدم Paddle OCR للتعرف على المحتوى النصي في لقطة الشاشة:

```js
/* الصيغة الكاملة. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* الصيغة المختصرة. */

ocr.paddle.recognizeText();

/* الصيغة الابسط. */

ocr.paddle();
```

استخدم Paddle OCR للتعرف على المحتوى النصي في ملف صورة محلي (باستخدام `test.png` كمثال):

```js
/* الصيغة الكاملة. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* الصيغة المختصرة. */

ocr.paddle.recognizeText("test.png");

/* الصيغة الابسط. */

ocr.paddle("test.png");
```

اختيار حزمة لغة وضبط خيارات التعرف (يتطلب `profile` و `useCls` الإصدار AutoJs6 6.8.0 أو أحدث):

```js
let img = images.read("test.png");

/* استخدام حزمة اليابانية. */

ocr.paddle(img, { profile: "ja" });

/* تحديد اتجاه النص أولا لقراءة النص المدار بمقدار 180 درجة أيضا (معطل افتراضيا). */

ocr.paddle(img, { useCls: true });

/* useOpenCL يقابل NNAPI في إصدار ONNX Runtime ويعود إلى CPU عند عدم توفر NNAPI. */

ocr.paddle(img, { useOpenCL: true });
```

لمزيد من طرق الاستخدام, راجع قسم [التعرف الضوئي على الحروف (OCR)](https://docs.autojs6.com/#/ocr)
في وثائق AutoJs6.
