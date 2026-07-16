******

### Historial de versiones

******

# v1.0.0

###### 2026/07/17

* `Nuevo` Servicio de complemento Paddle OCR (PP-OCRv3), con ID de complemento `paddle-ocr-pp-ocrv3`, motor `paddle-ocr` y variante `v3`
* `Nuevo` Soporte para descubrir e invocar el complemento mediante `org.autojs.plugin.PADDLE_OCR`
* `Nuevo` Soporte para reconocimiento de texto `ocr.paddle.recognizeText(image)` y deteccion de texto `ocr.paddle.detect(image)` en capturas de pantalla, archivos de imagen locales y entrada de imagen ARGB_8888 sin procesar
* `Nuevo` Modelos CPU PaddleOCR PP-OCRv3 integrados, ejecutados con Paddle Lite y OpenCV 4.8.0
* `Nuevo` Recursos multilingues para informacion del complemento, instrucciones, README y CHANGELOG: espanol/frances/ruso/arabe/japones/coreano/ingles/chino simplificado/chino tradicional de Hong Kong/chino tradicional de Taiwan
* `Mejora` Soporte para compilaciones APK por ABI, incluidos `arm64-v8a`/`armeabi-v7a` y paquetes `universal`
* `Mejora` Los nombres de archivo APK de publicacion incluyen nombre del proyecto, numero de version y variante ABI
