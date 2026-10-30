<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>Plugin Paddle OCR PP-OCRv3 de reconnaissance de texte pour AutoJs6</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### Langues

******

Le README.md actuel prend en charge les langues suivantes:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- Français [fr] # actuel
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### Introduction

******

Le plugin AutoJs6 Paddle OCR (PP-OCRv3) ajoute une reconnaissance optique de caractères basée sur PaddleOCR PP-OCRv3 et ONNX Runtime, avec prise en charge des captures d'écran, des fichiers image locaux et des entrées image brutes. Depuis la version 2.0.0, il fonctionne avec ONNX Runtime au lieu de Paddle Lite, prend en charge quatre ABI et se décline en cinq paquets de langue.

> **Édition Paddle Lite**: l'implémentation Paddle Lite de 1.0.x est désormais publiée séparément sous le nom [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) (ID de plugin `paddle-ocr-pp-ocrv3-paddle-lite`, variante `v3-paddle-lite`). Elle ne prend en charge que arm64-v8a et armeabi-v7a et peut être installée à côté de ce plugin.

******

### Fonctions

******

- Se décline en cinq paquets de langue (chinois simplifié, anglais, chinois traditionnel, japonais et coréen). Le paquet chinois simplifié conserve le nom de paquet et l'ID de plugin `paddle-ocr-pp-ocrv3` de 1.0.x; tous les paquets utilisent le moteur `paddle-ocr` et la variante `v3`.
- Prend en charge `ocr.paddle.recognizeText(image)` et `ocr.paddle.detect(image)` dans AutoJs6.
- Prend en charge les captures d'ecran, les fichiers image locaux et les entrees image brutes ARGB_8888.
- Les informations du plugin, les instructions, le README et le CHANGELOG prennent en charge espagnol/francais/russe/arabe/japonais/coreen/anglais/chinois simplifie/chinois traditionnel de Hong Kong/chinois traditionnel de Taiwan.
- Basé sur PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 et OpenCV 4.8.0, pour quatre ABI (arm64-v8a, armeabi-v7a, x86_64 et x86).
- `useSlim: true` utilise des modèles de détection et de reconnaissance quantifiés en int8 par la quantification dynamique d'ONNX Runtime.
- `useCls: true` détermine l'orientation du texte avant la reconnaissance, ce qui permet de lire un texte tourné de 180 degrés; désactivé par défaut, comme en 1.0.x.
- `useOpenCL` est associé à NNAPI dans l'édition ONNX Runtime. Sous Android 8.1 (API 27) ou ultérieur, le fournisseur d'exécution NNAPI est utilisé; sur les versions antérieures, ou si NNAPI ne démarre pas, la reconnaissance repasse sur le CPU. Le gain de vitesse dépend de l'appareil.
- Les images peuvent contenir jusqu'à 16777216 pixels; les tampons bruts sont limités à 64 MiB
- Les images encodées sont limitées à 64 MiB avec prise en charge des fichiers et des tubes

******

### Paquets de langue

******

Chaque paquet de langue est un APK distinct, et plusieurs peuvent être installés en même temps:

| Langue | `profile` | ID de plugin | Nom de paquet | Nom de l'APK |
| --- | --- | --- | --- | --- |
| Chinois simplifié | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| Anglais | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| Chinois traditionnel | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zh-hant-<ABI>-*.apk` |
| Japonais | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| Coréen | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

Choisissez le paquet selon le texte à lire. Le paquet chinois simplifié lit aussi les lettres latines et les chiffres et constitue la recommandation par défaut. Pour du texte en chinois traditionnel, en japonais ou en coréen, installez le paquet correspondant; pour du texte uniquement en anglais, vous pouvez aussi installer le paquet anglais. Chaque paquet existe en cinq APK selon l'ABI (`arm64-v8a` pour la plupart des téléphones, `armeabi-v7a`, `x86_64`, `x86` et `universal`, qui contient les quatre ABI et est le plus volumineux). N'installez que celui qui correspond à votre appareil.

******

### Utilisation

******

Reconnaitre le contenu texte d'une capture d'ecran:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

Reconnaitre le contenu texte d'un fichier image local, avec `test.png` comme exemple:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

Des formes abregees sont egalement disponibles:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

Choisir un paquet de langue et régler les options de reconnaissance:

```js
let img = images.read("test.png");
/* Utiliser le paquet japonais. */
ocr.paddle(img, { profile: "ja" });
/* Choisir le paquet coréen par ID de plugin. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* Utiliser les modèles quantifiés et activer la classification de l'orientation du texte. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL est associé à NNAPI dans l'édition ONNX Runtime. */
ocr.paddle(img, { useOpenCL: true });
/* Utiliser l'édition Paddle Lite. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

Le choix d'un paquet par `profile` et l'option `useCls` nécessitent AutoJs6 6.8.0 ou ultérieur. Les hôtes plus anciens ne choisissent pas par `profile` et ne transmettent pas `useCls`; si plusieurs paquets de langue sont installés, utilisez `engineId` pour en choisir un.

******

### Methodes API

******

Les API OCR courantes incluent:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` reconnait la capture d'ecran actuelle par defaut, et `ocr.paddle(path)` reconnait un fichier image local.

******

### Historique des versions

******

# v2.0.0

###### 2026/10/30

* `Note` La reconnaissance fonctionne désormais avec ONNX Runtime au lieu de Paddle Lite, et le développeur devient SuperMonster003. L'ancienne implémentation Paddle Lite est publiée séparément sous le nom Paddle OCR (PP-OCRv3 Paddle Lite) (ID de plugin `paddle-ocr-pp-ocrv3-paddle-lite`, variante `v3-paddle-lite`) et peut être installée à côté de ce plugin. Les versions 1.0.6 et antérieures appartiennent à ce plugin Paddle Lite, qui se poursuit dans son propre dépôt
* `Note` Le plugin se décline désormais en cinq paquets de langue (chinois simplifié, anglais, chinois traditionnel, japonais et coréen), chacun étant un APK distinct; le paquet chinois simplifié conserve le nom de paquet et l'ID de plugin d'origine
* `Note` Le choix d'un paquet par `profile` et l'option `useCls` nécessitent AutoJs6 6.8.0 ou ultérieur; les hôtes plus anciens ne choisissent pas par `profile` et ne transmettent pas `useCls`; ce plugin déclare comme minimum le code de version d'hôte 5935 (AutoJs6 6.8.0)
* `Ajout` Prise en charge des appareils x86_64 et x86, émulateurs compris, soit quatre ABI au total
* `Ajout` Nouvelle option `useCls`, qui détermine l'orientation du texte avant la reconnaissance pour lire aussi un texte tourné de 180 degrés; désactivée par défaut
* `Ajout` `useOpenCL` est associé à NNAPI dans l'édition ONNX Runtime: Android 8.1 ou ultérieur utilise NNAPI, et les versions antérieures ou les appareils sans NNAPI disponible repassent sur le CPU
* `Ajout` Choisissez la langue avec `profile` (`zh`, `en`, `zh-hant`, `ja`, `ko`) et l'édition Paddle Lite avec `variant: "v3-paddle-lite"`; sans ces options, le paquet en chinois simplifié est utilisé par défaut parmi les plugins PP-OCRv3
* `Amelioration` `useSlim` utilise désormais des modèles de détection et de reconnaissance quantifiés en int8 par la quantification dynamique d'ONNX Runtime
* `Dependance` Ajout d'ONNX Runtime Android 1.21.1 et suppression de Paddle Lite
* `Dependance` Les modèles PaddleOCR PP-OCRv3 passent au format ONNX, convertis à partir des modèles d'inférence officiels, avec de nouveaux modèles de reconnaissance anglais, chinois traditionnel, japonais et coréen et un modèle d'orientation du texte
* `Dependance` OpenCV 4.8.0 est de nouveau fourni sous forme de bibliothèque partagée libopencv_java4.so, une par ABI, comme dans le plugin PP-OCRv4 (1.0.6 la liait statiquement à libNative.so). Les applications empaquetées prennent cette bibliothèque dans le plugin OpenCV, pas dans ce plugin: l'empaquetage avec ce plugin ajoute OpenCV automatiquement et échoue s'il n'est pas installé

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

##### Pour plus d'historique des versions, voir

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-fr.md)

******

### Compilation

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Compilation Release:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

Les paramètres de compilation viennent de `version.properties`, avec le SDK minimum actuel 24 et le SDK cible 37. Les modèles ONNX ne sont pas versionnés: avant de compiler, exécutez `prepare_ppocrv3_assets.py` comme ci-dessus. Il télécharge les modèles officiels de PaddleOCR, les convertit en ONNX et les vérifie avec `libs/ppocr-android-sdk/models.provenance.json`; `--profile` accepte `zh`, `en`, `zhHant`, `ja`, `ko` ou `all`. Les composants tiers et leurs licences sont listés dans [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

******

### Structure des ressources

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` fournit les descriptions localisees du plugin; `plugin_instruction.md` fournit les instructions du plugin affichees par l'hote. README et CHANGELOG sont generes par `.python/generate_markdown.py` depuis les fichiers source JSON.

******

### Liens

******

- Documentation OCR AutoJs6: https://docs.autojs6.com/#/ocr
- Projet officiel PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- Projet officiel ONNX Runtime: https://github.com/microsoft/onnxruntime
- Site officiel OpenCV: https://opencv.org/
- Plugin Paddle OCR (PP-OCRv3 Paddle Lite): https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
