<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>Complemento Paddle OCR PP-OCRv3 de reconocimiento de texto para AutoJs6</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### Idiomas

******

El README.md actual admite los siguientes idiomas:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- Español [es] # actual
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### Introduccion

******

El complemento AutoJs6 Paddle OCR (PP-OCRv3) agrega reconocimiento optico de caracteres basado en PaddleOCR PP-OCRv3, con soporte para capturas de pantalla, archivos de imagen locales y entrada de imagen sin procesar.

******

### Funciones

******

- Proporciona el servicio de complemento `paddle-ocr-pp-ocrv3`, con ID de complemento `paddle-ocr-pp-ocrv3`.
- Admite `ocr.paddle.recognizeText(image)` y `ocr.paddle.detect(image)` en AutoJs6.
- Admite capturas de pantalla, archivos de imagen locales y entrada de imagen ARGB_8888 sin procesar.
- La informacion del complemento, las instrucciones, README y CHANGELOG admiten espanol/frances/ruso/arabe/japones/coreano/ingles/chino simplificado/chino tradicional de Hong Kong/chino tradicional de Taiwan.
- Basado en PaddleOCR PP-OCRv3, Paddle Lite y OpenCV 4.8.0.
- Las imágenes admiten hasta 16777216 píxeles; los búferes de imagen sin procesar se limitan a 64 MiB
- La imagen codificada admite hasta 64 MiB mediante descriptores de archivo y tuberías

******

### Uso

******

Reconocer el contenido de texto en una captura de pantalla:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

Reconocer el contenido de texto en un archivo de imagen local, usando `test.png` como ejemplo:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

Tambien hay formas abreviadas disponibles:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

******

### Metodos API

******

Las API OCR comunes incluyen:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` reconoce la captura de pantalla actual de forma predeterminada, y `ocr.paddle(path)` reconoce un archivo de imagen local.

******

### Historial de versiones

******

# v1.0.5

###### 2026/09/15

* `Mejora` compileSdk y targetSdk suben a 37 (Android 17); el comportamiento del plugin no depende del nuevo objetivo

# v1.0.4

###### 2026/09/13

* `Correccion` Limpieza incompleta de referencias JNI temporales al convertir cadenas durante la inicialización; esta ahora se detiene de inmediato ante excepciones JNI _[`issue #575`](http://issues.autojs6.com/575)_
* `Correccion` La versión y las ABI del centro de complementos coinciden con el APK instalado
* `Correccion` La imagen codificada admite hasta 64 MiB mediante descriptores de archivo y tuberías
* `Correccion` Las fechas de versión mantienen un formato uniforme en inglés
* `Mejora` Validación de las versiones, firmas y variantes completas de los APK antes de crear los archivos de descarga
* `Mejora` Las imágenes admiten hasta 16777216 píxeles; los búferes de imagen sin procesar se limitan a 64 MiB

# v1.0.3

###### 2026/09/12

* `Correccion` Paddle Lite fallaba (SIGSEGV) cuando la primera detección de texto de un proceso usaba una imagen baja como 1000 x 320; ahora el detector se precalienta una vez con una imagen en blanco de 960 x 960 antes de la primera detección real

##### Para mas historial de versiones, consulta

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-es.md)

******

### Compilacion

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Compilacion Release:

```powershell
.\gradlew.bat :app:assembleRelease
```

Los parametros de compilacion vienen de `version.properties`, con SDK minimo actual 24 y SDK objetivo 37.

******

### Estructura de recursos

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` proporciona descripciones localizadas del complemento; `plugin_instruction.md` proporciona instrucciones del complemento mostradas por el host. README y CHANGELOG son generados por `.python/generate_markdown.py` desde archivos fuente JSON.

******

### Enlaces

******

- Documentacion OCR de AutoJs6: https://docs.autojs6.com/#/ocr
- Proyecto oficial PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- Proyecto oficial Paddle Lite: https://github.com/PaddlePaddle/Paddle-Lite
- Sitio oficial OpenCV: https://opencv.org/


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
