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
