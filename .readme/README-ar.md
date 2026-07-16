<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>مكون Paddle OCR PP-OCRv3 للتعرف على النصوص في AutoJs6</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/commit/6c83d3092ae569a4e84fad3a5e8cec99b5c65856"><img alt="Created" src="https://img.shields.io/date/1773538952?color=2e7d32&label=Created"/></a>
    <br>
    <a href="https://developer.android.com/studio/archive"><img alt="Android Studio" src="https://img.shields.io/badge/Android%20Studio-2023.3+-B64FC8"/></a>
    <a href="https://www.jetbrains.com/idea/download/other.html"><img alt="IntelliJ IDEA" src="https://img.shields.io/badge/IntelliJ%20IDEA-2023.3+-EE4677"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### اللغات

******

يدعم README.md الحالي اللغات التالية:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- العربية [ar] # الحالي

******

### مقدمة

******

يضيف مكون AutoJs6 Paddle OCR (PP-OCRv3) التعرف الضوئي على الحروف بالاعتماد على PaddleOCR PP-OCRv3, مع دعم لقطات الشاشة, وملفات الصور المحلية, وإدخال الصور الخام.

******

### الميزات

******

- يوفر خدمة المكون `paddle-ocr-pp-ocrv3`, مع معرف المكون `paddle-ocr-pp-ocrv3`.
- يدعم `ocr.paddle.recognizeText(image)` و `ocr.paddle.detect(image)` في AutoJs6.
- يدعم لقطات الشاشة, وملفات الصور المحلية, وإدخال صور ARGB_8888 الخام.
- تدعم معلومات المكون, والتعليمات, و README, و CHANGELOG الاسبانية/الفرنسية/الروسية/العربية/اليابانية/الكورية/الانجليزية/الصينية المبسطة/الصينية التقليدية في هونغ كونغ/الصينية التقليدية في تايوان.
- يعتمد على PaddleOCR PP-OCRv3, و Paddle Lite, و OpenCV 4.8.0.

******

### الاستخدام

******

التعرف على المحتوى النصي في لقطة شاشة:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

التعرف على المحتوى النصي في ملف صورة محلي, باستخدام `test.png` كمثال:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

تتوفر ايضا صيغ مختصرة:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

******

### طرق API

******

تشمل واجهات OCR الشائعة:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

يتعرف `ocr.paddle()` افتراضيا على لقطة الشاشة الحالية, ويتعرف `ocr.paddle(path)` على ملف صورة محلي.

******

### سجل الاصدارات

******

# v1.0.0

###### 2026/07/03

* `اضافة` خدمة مكون Paddle OCR (PP-OCRv3), مع معرف المكون `paddle-ocr-pp-ocrv3`, والمحرك `paddle-ocr`, والمتغير `v3`
* `اضافة` دعم اكتشاف المكون واستدعائه عبر `org.autojs.plugin.PADDLE_OCR`
* `اضافة` دعم التعرف على النص `ocr.paddle.recognizeText(image)` واكتشاف النص `ocr.paddle.detect(image)` للقطات الشاشة, وملفات الصور المحلية, وإدخال صور ARGB_8888 الخام
* `اضافة` تضمين نماذج PaddleOCR PP-OCRv3 CPU, تعمل عبر Paddle Lite و OpenCV 4.8.0
* `اضافة` موارد متعددة اللغات لمعلومات المكون, والتعليمات, و README, و CHANGELOG: الاسبانية/الفرنسية/الروسية/العربية/اليابانية/الكورية/الانجليزية/الصينية المبسطة/الصينية التقليدية في هونغ كونغ/الصينية التقليدية في تايوان
* `تحسين` دعم بناء APK حسب ABI, بما في ذلك `arm64-v8a`/`armeabi-v7a` وحزم `universal`
* `تحسين` تتضمن اسماء ملفات APK المنشورة اسم المشروع, ورقم الاصدار, ومتغير ABI

##### لمزيد من سجل الاصدارات, راجع

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.changelog/CHANGELOG-ar.md)

******

### البناء

******

```powershell
.\gradlew.bat :app:assembleDebug
```

بناء Release:

```powershell
.\gradlew.bat :app:assembleRelease
```

تأتي معلمات البناء من `version.properties`, مع حد SDK ادنى حالي 24 و SDK هدف 36.

******

### هيكل الموارد

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

يوفر `strings.xml` اوصاف المكون المترجمة; ويوفر `plugin_instruction.md` تعليمات المكون التي يعرضها المضيف. يتم توليد README و CHANGELOG بواسطة `.python/generate_markdown.py` من ملفات JSON المصدرية.

******

### روابط

******

- وثائق AutoJs6 OCR: https://docs.autojs6.com/#/ocr
- مشروع PaddleOCR الرسمي: https://github.com/PaddlePaddle/PaddleOCR
- مشروع Paddle Lite الرسمي: https://github.com/PaddlePaddle/Paddle-Lite
- موقع OpenCV الرسمي: https://opencv.org/
