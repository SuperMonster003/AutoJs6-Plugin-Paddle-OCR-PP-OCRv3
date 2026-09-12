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

# v1.0.2

###### 2026/09/12

* `Correccion` El comando `clean` fallaba cuando no se inicializaba la opción de limpieza de las dependencias nativas de Paddle OCR
* `Mejora` Sincronizada la biblioteca nativa OpenCV 4.8.0 con la reconstrucción NDK r28c (Clang 19.0.1) (donante: AutoJs6-Plugin-OpenCV); `libopencv_java4.so` de las 4 ABI mantiene la alineación `PT_LOAD` de 16 KB e incluye un manifiesto de provenance

# v1.0.1

###### 2026/09/11

* `Mejora` Verificación de compilación de la alineación de páginas de 16 KB en bibliotecas nativas de 64 bits, con controles del contrato manifest e informes JSON

# v1.0.0

###### 2026/09/01

* `Nuevo` Servicio de complemento Paddle OCR (PP-OCRv3), con ID de complemento `paddle-ocr-pp-ocrv3`, motor `paddle-ocr` y variante `v3`
* `Nuevo` Soporte para descubrir e invocar el complemento mediante `org.autojs.plugin.PADDLE_OCR`
* `Nuevo` Soporte para reconocimiento de texto `ocr.paddle.recognizeText(image)` y deteccion de texto `ocr.paddle.detect(image)` en capturas de pantalla, archivos de imagen locales y entrada de imagen ARGB_8888 sin procesar
* `Nuevo` Modelos CPU PaddleOCR PP-OCRv3 integrados, ejecutados con Paddle Lite y OpenCV 4.8.0
* `Nuevo` Recursos multilingues para informacion del complemento, instrucciones, README y CHANGELOG: espanol/frances/ruso/arabe/japones/coreano/ingles/chino simplificado/chino tradicional de Hong Kong/chino tradicional de Taiwan
* `Mejora` Soporte para compilaciones APK por ABI, incluidos `arm64-v8a`/`armeabi-v7a` y paquetes `universal`
* `Mejora` Los nombres de archivo APK de publicacion incluyen nombre del proyecto, numero de version y variante ABI
* `Mejora` Unificar el diseño del README y la gestión de versiones de la plataforma Gradle

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

Los parametros de compilacion vienen de `version.properties`, con SDK minimo actual 24 y SDK objetivo 36.

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
