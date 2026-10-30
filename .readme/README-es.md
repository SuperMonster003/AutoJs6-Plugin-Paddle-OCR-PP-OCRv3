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

El complemento AutoJs6 Paddle OCR (PP-OCRv3) agrega reconocimiento óptico de caracteres basado en PaddleOCR PP-OCRv3 y ONNX Runtime, con soporte para capturas de pantalla, archivos de imagen locales y entrada de imagen sin procesar. Desde la versión 2.0.0 funciona con ONNX Runtime en lugar de Paddle Lite, admite cuatro ABI y se distribuye en cinco paquetes de idioma.

> **Edición Paddle Lite**: la implementación Paddle Lite de 1.0.x se publica ahora por separado como [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) (ID de complemento `paddle-ocr-pp-ocrv3-paddle-lite`, variante `v3-paddle-lite`). Solo admite arm64-v8a y armeabi-v7a y puede instalarse junto con este complemento.

******

### Funciones

******

- Se distribuye en cinco paquetes de idioma: chino simplificado, inglés, chino tradicional, japonés y coreano. El paquete de chino simplificado conserva el nombre de paquete y el ID de complemento `paddle-ocr-pp-ocrv3` de 1.0.x; todos los paquetes usan el motor `paddle-ocr` y la variante `v3`.
- Admite `ocr.paddle.recognizeText(image)` y `ocr.paddle.detect(image)` en AutoJs6.
- Admite capturas de pantalla, archivos de imagen locales y entrada de imagen ARGB_8888 sin procesar.
- La informacion del complemento, las instrucciones, README y CHANGELOG admiten espanol/frances/ruso/arabe/japones/coreano/ingles/chino simplificado/chino tradicional de Hong Kong/chino tradicional de Taiwan.
- Basado en PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 y OpenCV 4.8.0, para cuatro ABI: arm64-v8a, armeabi-v7a, x86_64 y x86.
- `useSlim: true` usa modelos de detección y reconocimiento cuantizados a int8 con la cuantización dinámica de ONNX Runtime.
- `useCls: true` determina la orientación del texto antes del reconocimiento, de modo que también se lee el texto girado 180 grados; está desactivado de forma predeterminada, como en 1.0.x.
- `useOpenCL` se asigna a NNAPI en la edición ONNX Runtime: en Android 8.1 (API 27) o posterior se usa el proveedor de ejecución NNAPI; en versiones anteriores, o si NNAPI no se inicia, el reconocimiento vuelve a la CPU. Que sea más rápido depende del dispositivo.
- Las imágenes admiten hasta 16777216 píxeles; los búferes de imagen sin procesar se limitan a 64 MiB
- La imagen codificada admite hasta 64 MiB mediante descriptores de archivo y tuberías

******

### Paquetes de idioma

******

Cada paquete de idioma es un APK independiente, y se pueden instalar varios a la vez:

| Idioma | `profile` | ID de complemento | Nombre de paquete | Nombre del APK |
| --- | --- | --- | --- | --- |
| Chino simplificado | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| Inglés | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| Chino tradicional | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| Japonés | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| Coreano | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

Elija el paquete según el texto que quiera leer: el paquete de chino simplificado también lee letras latinas y dígitos y es la recomendación predeterminada; para texto en chino tradicional, japonés o coreano, instale el paquete correspondiente; para texto solo en inglés también puede instalar el paquete de inglés. Cada paquete tiene cinco APK por ABI: `arm64-v8a` (la mayoría de los teléfonos), `armeabi-v7a`, `x86_64`, `x86` y `universal` (las cuatro ABI, el más grande). Instale solo el que corresponda a su dispositivo.

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

Elegir un paquete de idioma y ajustar opciones de reconocimiento:

```js
let img = images.read("test.png");
/* Usar el paquete de japonés. */
ocr.paddle(img, { profile: "ja" });
/* Elegir el paquete de coreano por ID de complemento. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* Usar los modelos cuantizados y activar la clasificación de orientación del texto. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL se asigna a NNAPI en la edición ONNX Runtime. */
ocr.paddle(img, { useOpenCL: true });
/* Usar la edición Paddle Lite. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

Elegir un paquete por `profile` y la opción `useCls` requieren AutoJs6 6.8.0 o posterior. Los hosts anteriores no eligen por `profile` ni transmiten `useCls`; si hay varios paquetes de idioma instalados, use `engineId` para elegir uno.

******

### Metodos API

******

Las API OCR comunes incluyen:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` reconoce la captura de pantalla actual de forma predeterminada, y `ocr.paddle(path)` reconoce un archivo de imagen local.

******

### Historial de versiones

******

# v2.0.0

###### 2026/10/30

* `Nota` El reconocimiento funciona ahora con ONNX Runtime en lugar de Paddle Lite, y el desarrollador pasa a ser SuperMonster003. La implementación Paddle Lite anterior se publica por separado como Paddle OCR (PP-OCRv3 Paddle Lite) (ID de complemento `paddle-ocr-pp-ocrv3-paddle-lite`, variante `v3-paddle-lite`) y puede instalarse junto con este complemento
* `Nota` El complemento se distribuye ahora en cinco paquetes de idioma (chino simplificado, inglés, chino tradicional, japonés y coreano), cada uno un APK independiente; el paquete de chino simplificado conserva el nombre de paquete y el ID de complemento originales
* `Nota` Elegir un paquete por `profile` y la opción `useCls` requieren AutoJs6 6.8.0 o posterior; los hosts anteriores no eligen por `profile` ni transmiten `useCls`
* `Nuevo` Compatibilidad con dispositivos x86_64 y x86, incluidos los emuladores, para un total de cuatro ABI
* `Nuevo` Nueva opción `useCls`, que determina la orientación del texto antes del reconocimiento para leer también el texto girado 180 grados; desactivada de forma predeterminada
* `Nuevo` `useOpenCL` se asigna a NNAPI en la edición ONNX Runtime: Android 8.1 o posterior usa NNAPI, y las versiones anteriores o los dispositivos sin NNAPI disponible vuelven a la CPU
* `Mejora` `useSlim` usa ahora modelos de detección y reconocimiento cuantizados a int8 con la cuantización dinámica de ONNX Runtime
* `Dependencia` Añadir ONNX Runtime Android 1.21.1 y eliminar Paddle Lite
* `Dependencia` Los modelos PaddleOCR PP-OCRv3 pasan al formato ONNX, convertidos desde los modelos de inferencia oficiales, con nuevos modelos de reconocimiento para inglés, chino tradicional, japonés y coreano y un modelo de orientación del texto
* `Dependencia` OpenCV 4.8.0 se incluye ahora como la biblioteca compartida libopencv_java4.so, igual que en el complemento PP-OCRv4

# v1.0.6

###### 2026/10/10

* `Nota` Las aplicaciones empaquetadas que usan esta versión necesitan AutoJs6 6.8.0 o posterior como host; los hosts anteriores solo pueden empaquetarla junto con OpenCV
* `Correccion` Los fallos nativos durante la carga del modelo o la inferencia cerraban el proceso del plugin; ahora se devuelven al host como errores
* `Mejora` libNative.so ya no exporta símbolos de OpenCV y el APK ya no incluye libopencv_java4.so, por lo que es más pequeño y las aplicaciones empaquetadas pueden usarlo junto con otra versión de OpenCV
* `Dependencia` Eliminado el AAR de OpenCV para Android 4.8.0; solo queda el SDK de OpenCV para Android 4.8.0 enlazado estáticamente y verificado con SHA-256 al descargarse

# v1.0.5

###### 2026/10/05

* `Correccion` Advertencias de lectura de SDK XML v4 con AGP 9.1 y comprobaciones de alineación nativa de APK activadas por error al ensamblar pruebas unitarias JVM, mediante los plugins de compilación compartidos 1.8.3
* `Mejora` compileSdk y targetSdk suben a 37 (Android 17); el comportamiento del plugin no depende del nuevo objetivo
* `Mejora` Los iconos de información de la aplicación de Android comparten las imágenes y los fondos claros y oscuros de Icon Studio, conservando las imágenes transparentes del centro de plugins y las opciones del lanzador

##### Para mas historial de versiones, consulta

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-es.md)

******

### Compilacion

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Compilacion Release:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

Los parámetros de compilación vienen de `version.properties`, con SDK mínimo actual 24 y SDK objetivo 37. Los modelos ONNX no están en el repositorio: antes de compilar, ejecute `prepare_ppocrv3_assets.py` como se muestra arriba. Descarga los modelos oficiales de PaddleOCR, los convierte a ONNX y los verifica con `libs/ppocr-android-sdk/models.provenance.json`; `--profile` acepta `zh`, `en`, `zhHant`, `ja`, `ko` o `all`. Los componentes de terceros y sus licencias figuran en [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

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
- Proyecto oficial ONNX Runtime: https://github.com/microsoft/onnxruntime
- Sitio oficial OpenCV: https://opencv.org/
- Complemento Paddle OCR (PP-OCRv3 Paddle Lite): https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
