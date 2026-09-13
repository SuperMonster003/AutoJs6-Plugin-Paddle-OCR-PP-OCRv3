******

### Historique des versions

******

# v1.0.4

###### 2026/09/13

* `Correction` Les informations de version et d'ABI du centre des plugins correspondent à l'APK installé
* `Correction` Les images encodées sont limitées à 64 MiB avec prise en charge des fichiers et des tubes
* `Correction` Les dates de version utilisent un format anglais uniforme
* `Amelioration` Validation des versions, signatures et variantes complètes des APK avant la création des fichiers à télécharger
* `Amelioration` Les images peuvent contenir jusqu'à 16777216 pixels; les tampons bruts sont limités à 64 MiB

# v1.0.3

###### 2026/09/12

* `Correction` Paddle Lite plantait (SIGSEGV) lorsque la première détection de texte d'un processus utilisait une image basse telle que 1000 x 320 ; le détecteur est désormais préchauffé une fois avec une image vierge de 960 x 960 avant la première détection réelle

# v1.0.2

###### 2026/09/12

* `Correction` Échec de la tâche `clean` lorsque l'option de nettoyage des dépendances natives de Paddle OCR n'était pas initialisée
* `Amelioration` Bibliothèque native OpenCV 4.8.0 synchronisée avec la recompilation NDK r28c (Clang 19.0.1) (donneur : AutoJs6-Plugin-OpenCV) ; `libopencv_java4.so` des 4 ABI conserve l'alignement `PT_LOAD` de 16 Ko et embarque un manifeste de provenance

# v1.0.1

###### 2026/09/11

* `Amelioration` Vérification à la compilation de l'alignement des pages de 16 KB des bibliothèques natives 64 bits, avec contrôle du contrat manifest et rapports JSON

# v1.0.0

###### 2026/09/01

* `Ajout` Service de plugin Paddle OCR (PP-OCRv3), avec ID de plugin `paddle-ocr-pp-ocrv3`, moteur `paddle-ocr` et variante `v3`
* `Ajout` Prise en charge de la decouverte et de l'appel du plugin via `org.autojs.plugin.PADDLE_OCR`
* `Ajout` Prise en charge de la reconnaissance de texte `ocr.paddle.recognizeText(image)` et de la detection de texte `ocr.paddle.detect(image)` pour les captures d'ecran, les fichiers image locaux et les entrees image brutes ARGB_8888
* `Ajout` Modeles CPU PaddleOCR PP-OCRv3 integres, executes avec Paddle Lite et OpenCV 4.8.0
* `Ajout` Ressources multilingues pour les informations du plugin, les instructions, README et CHANGELOG: espagnol/francais/russe/arabe/japonais/coreen/anglais/chinois simplifie/chinois traditionnel de Hong Kong/chinois traditionnel de Taiwan
* `Amelioration` Prise en charge des builds APK par ABI, y compris `arm64-v8a`/`armeabi-v7a` et les paquets `universal`
* `Amelioration` Les noms de fichiers APK de publication incluent le nom du projet, le numero de version et la variante ABI
* `Amelioration` Uniformiser la mise en page du README et la gestion des versions de la plateforme Gradle
