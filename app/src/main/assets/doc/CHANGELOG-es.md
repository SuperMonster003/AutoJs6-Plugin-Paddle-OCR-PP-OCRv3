******

### Historial de versiones

******

# v1.0.4

###### 2026/09/13

* `Correccion` La versión y las ABI del centro de complementos coinciden con el APK instalado
* `Correccion` La imagen codificada admite hasta 64 MiB mediante descriptores de archivo y tuberías
* `Correccion` Las fechas de versión mantienen un formato uniforme en inglés
* `Mejora` Validación de las versiones, firmas y variantes completas de los APK antes de crear los archivos de descarga
* `Mejora` Las imágenes admiten hasta 16777216 píxeles; los búferes de imagen sin procesar se limitan a 64 MiB

# v1.0.3

###### 2026/09/12

* `Correccion` Paddle Lite fallaba (SIGSEGV) cuando la primera detección de texto de un proceso usaba una imagen baja como 1000 x 320; ahora el detector se precalienta una vez con una imagen en blanco de 960 x 960 antes de la primera detección real

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
