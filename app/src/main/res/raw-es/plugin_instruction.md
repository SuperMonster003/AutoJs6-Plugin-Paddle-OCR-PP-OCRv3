Usa Paddle OCR para reconocer el contenido de texto en una captura de pantalla:

```js
/* Forma completa. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* Forma abreviada. */

ocr.paddle.recognizeText();

/* Forma minima. */

ocr.paddle();
```

Usa Paddle OCR para reconocer el contenido de texto en un archivo de imagen local (tomando `test.png` como ejemplo):

```js
/* Forma completa. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* Forma abreviada. */

ocr.paddle.recognizeText("test.png");

/* Forma minima. */

ocr.paddle("test.png");
```

Elegir un paquete de idioma y ajustar opciones de reconocimiento (`profile` y `useCls` requieren AutoJs6 6.8.0 o posterior):

```js
let img = images.read("test.png");

/* Usar el paquete de japonés. */

ocr.paddle(img, { profile: "ja" });

/* Determinar primero la orientación del texto para leer también el texto girado 180 grados (desactivado de forma predeterminada). */

ocr.paddle(img, { useCls: true });

/* useOpenCL se asigna a NNAPI en la edición ONNX Runtime y vuelve a la CPU si NNAPI no está disponible. */

ocr.paddle(img, { useOpenCL: true });
```

Para mas formas de uso, consulta la seccion [Reconocimiento optico de caracteres (OCR)](https://docs.autojs6.com/#/ocr)
de la documentacion de AutoJs6.