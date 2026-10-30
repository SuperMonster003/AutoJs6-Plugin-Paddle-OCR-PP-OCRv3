Utilisez Paddle OCR pour reconnaitre le contenu texte d'une capture d'ecran:

```js
/* Forme complete. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* Forme abregee. */

ocr.paddle.recognizeText();

/* Forme minimale. */

ocr.paddle();
```

Utilisez Paddle OCR pour reconnaitre le contenu texte d'un fichier image local (en prenant `test.png` comme exemple):

```js
/* Forme complete. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* Forme abregee. */

ocr.paddle.recognizeText("test.png");

/* Forme minimale. */

ocr.paddle("test.png");
```

Choisir un paquet de langue et régler les options de reconnaissance (`profile` et `useCls` nécessitent AutoJs6 6.8.0 ou ultérieur):

```js
let img = images.read("test.png");

/* Utiliser le paquet japonais. */

ocr.paddle(img, { profile: "ja" });

/* Déterminer d'abord l'orientation du texte pour lire aussi un texte tourné de 180 degrés (désactivé par défaut). */

ocr.paddle(img, { useCls: true });

/* useOpenCL est associé à NNAPI dans l'édition ONNX Runtime et repasse sur le CPU si NNAPI n'est pas disponible. */

ocr.paddle(img, { useOpenCL: true });
```

Pour plus de modes d'utilisation, consultez la section [Reconnaissance optique de caracteres (OCR)](https://docs.autojs6.com/#/ocr)
de la documentation AutoJs6.