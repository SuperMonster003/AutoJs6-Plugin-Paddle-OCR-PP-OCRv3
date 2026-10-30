******

### Historique des versions

******

# v2.0.0

###### 2026/10/30

* `Note` La reconnaissance fonctionne désormais avec ONNX Runtime au lieu de Paddle Lite, et le développeur devient SuperMonster003. L'ancienne implémentation Paddle Lite est publiée séparément sous le nom Paddle OCR (PP-OCRv3 Paddle Lite) (ID de plugin `paddle-ocr-pp-ocrv3-paddle-lite`, variante `v3-paddle-lite`) et peut être installée à côté de ce plugin
* `Note` Le plugin se décline désormais en cinq paquets de langue (chinois simplifié, anglais, chinois traditionnel, japonais et coréen), chacun étant un APK distinct; le paquet chinois simplifié conserve le nom de paquet et l'ID de plugin d'origine
* `Note` Le choix d'un paquet par `profile` et l'option `useCls` nécessitent AutoJs6 6.8.0 ou ultérieur; les hôtes plus anciens ne choisissent pas par `profile` et ne transmettent pas `useCls`
* `Ajout` Prise en charge des appareils x86_64 et x86, émulateurs compris, soit quatre ABI au total
* `Ajout` Nouvelle option `useCls`, qui détermine l'orientation du texte avant la reconnaissance pour lire aussi un texte tourné de 180 degrés; désactivée par défaut
* `Ajout` `useOpenCL` est associé à NNAPI dans l'édition ONNX Runtime: Android 8.1 ou ultérieur utilise NNAPI, et les versions antérieures ou les appareils sans NNAPI disponible repassent sur le CPU
* `Amelioration` `useSlim` utilise désormais des modèles de détection et de reconnaissance quantifiés en int8 par la quantification dynamique d'ONNX Runtime
* `Dependance` Ajout d'ONNX Runtime Android 1.21.1 et suppression de Paddle Lite
* `Dependance` Les modèles PaddleOCR PP-OCRv3 passent au format ONNX, convertis à partir des modèles d'inférence officiels, avec de nouveaux modèles de reconnaissance anglais, chinois traditionnel, japonais et coréen et un modèle d'orientation du texte
* `Dependance` OpenCV 4.8.0 est désormais fourni sous forme de bibliothèque partagée libopencv_java4.so, comme dans le plugin PP-OCRv4

# v1.0.6

###### 2026/10/10

* `Note` Les applications empaquetées qui utilisent cette version nécessitent AutoJs6 6.8.0 ou une version ultérieure comme hôte ; les hôtes plus anciens ne peuvent l'empaqueter qu'avec OpenCV
* `Correction` Les erreurs natives lors du chargement du modèle ou de l'inférence arrêtaient le processus du plugin ; elles sont désormais renvoyées à l'hôte comme erreurs
* `Amelioration` libNative.so n'exporte plus les symboles OpenCV et l'APK n'inclut plus libopencv_java4.so ; il est plus léger et les applications empaquetées peuvent l'utiliser avec une autre version d'OpenCV
* `Dependance` Suppression de l'AAR OpenCV pour Android 4.8.0 ; seul le SDK Android OpenCV 4.8.0 lié statiquement subsiste, vérifié par SHA-256 au téléchargement

# v1.0.5

###### 2026/10/05

* `Correction` Avertissements de lecture SDK XML v4 avec AGP 9.1 et contrôles d'alignement natif des APK déclenchés par erreur lors de l'assemblage des tests unitaires JVM, avec les plugins de compilation partagés 1.8.3
* `Amelioration` compileSdk et targetSdk passent à 37 (Android 17) ; le comportement du plugin ne dépend pas de la nouvelle cible
* `Amelioration` Les icônes des informations d'application Android utilisent les illustrations et les fonds clairs et sombres d'Icon Studio, en conservant les images transparentes du centre de plugins et les choix du lanceur

# v1.0.4

###### 2026/09/13

* `Correction` Nettoyage incomplet des références JNI temporaires lors de la conversion des chaînes pendant l'initialisation; celle-ci s'arrête désormais immédiatement en cas d'exception JNI _[`issue #575`](http://issues.autojs6.com/575)_
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
