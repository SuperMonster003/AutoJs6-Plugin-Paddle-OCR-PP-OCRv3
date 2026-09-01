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

Le plugin AutoJs6 Paddle OCR (PP-OCRv3) ajoute une reconnaissance optique de caracteres basee sur PaddleOCR PP-OCRv3, avec prise en charge des captures d'ecran, des fichiers image locaux et des entrees image brutes.

******

### Fonctions

******

- Fournit le service de plugin `paddle-ocr-pp-ocrv3`, avec l'ID de plugin `paddle-ocr-pp-ocrv3`.
- Prend en charge `ocr.paddle.recognizeText(image)` et `ocr.paddle.detect(image)` dans AutoJs6.
- Prend en charge les captures d'ecran, les fichiers image locaux et les entrees image brutes ARGB_8888.
- Les informations du plugin, les instructions, le README et le CHANGELOG prennent en charge espagnol/francais/russe/arabe/japonais/coreen/anglais/chinois simplifie/chinois traditionnel de Hong Kong/chinois traditionnel de Taiwan.
- Base sur PaddleOCR PP-OCRv3, Paddle Lite et OpenCV 4.8.0.

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

******

### Methodes API

******

Les API OCR courantes incluent:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` reconnait la capture d'ecran actuelle par defaut, et `ocr.paddle(path)` reconnait un fichier image local.

******

### Historique des versions

******

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

##### Pour plus d'historique des versions, voir

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-fr.md)

******

### Compilation

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Compilation Release:

```powershell
.\gradlew.bat :app:assembleRelease
```

Les parametres de compilation viennent de `version.properties`, avec le SDK minimum actuel 24 et le SDK cible 36.

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
- Projet officiel Paddle Lite: https://github.com/PaddlePaddle/Paddle-Lite
- Site officiel OpenCV: https://opencv.org/
