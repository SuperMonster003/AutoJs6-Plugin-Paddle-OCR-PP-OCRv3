<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>Плагин распознавания текста Paddle OCR PP-OCRv3 для AutoJs6</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### Языки

******

Текущий README.md поддерживает следующие языки:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- [한국어 [ko]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ko.md)
- Русский [ru] # текущий
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### Введение

******

Плагин AutoJs6 Paddle OCR (PP-OCRv3) добавляет оптическое распознавание символов на базе PaddleOCR PP-OCRv3, с поддержкой снимков экрана, локальных файлов изображений и необработанного ввода изображений.

******

### Функции

******

- Предоставляет сервис плагина `paddle-ocr-pp-ocrv3`, с ID плагина `paddle-ocr-pp-ocrv3`.
- Поддерживает `ocr.paddle.recognizeText(image)` и `ocr.paddle.detect(image)` в AutoJs6.
- Поддерживает снимки экрана, локальные файлы изображений и необработанный ввод ARGB_8888.
- Информация о плагине, инструкции, README и CHANGELOG поддерживают испанский/французский/русский/арабский/японский/корейский/английский/упрощенный китайский/традиционный китайский Гонконга/традиционный китайский Тайваня.
- Основан на PaddleOCR PP-OCRv3, Paddle Lite и OpenCV 4.8.0.

******

### Примеры

******

Распознать текстовое содержимое на снимке экрана:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

Распознать текстовое содержимое в локальном файле изображения, используя `test.png` как пример:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

Также доступны краткие формы:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

******

### Методы API

******

Распространенные OCR API включают:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` по умолчанию распознает текущий снимок экрана, а `ocr.paddle(path)` распознает локальный файл изображения.

******

### История выпусков

******

# v1.0.2

###### 2026/09/12

* `Улучшено` Нативная библиотека OpenCV 4.8.0 синхронизирована с пересборкой NDK r28c (Clang 19.0.1) (донор: AutoJs6-Plugin-OpenCV); `libopencv_java4.so` для всех 4 ABI сохраняет выравнивание `PT_LOAD` 16 КБ и поставляется с манифестом provenance

# v1.0.1

###### 2026/09/11

* `Улучшено` Проверка выравнивания страниц 16 KB для 64-битных нативных библиотек при сборке, включая контракт manifest и отчеты JSON

# v1.0.0

###### 2026/09/01

* `Добавлено` Сервис плагина Paddle OCR (PP-OCRv3), с ID плагина `paddle-ocr-pp-ocrv3`, движком `paddle-ocr` и вариантом `v3`
* `Добавлено` Поддержка обнаружения и вызова плагина через `org.autojs.plugin.PADDLE_OCR`
* `Добавлено` Поддержка распознавания текста `ocr.paddle.recognizeText(image)` и обнаружения текста `ocr.paddle.detect(image)` для снимков экрана, локальных файлов изображений и необработанного ввода ARGB_8888
* `Добавлено` Встроенные CPU модели PaddleOCR PP-OCRv3, работающие на Paddle Lite и OpenCV 4.8.0
* `Добавлено` Многоязычные ресурсы для информации о плагине, инструкций, README и CHANGELOG: испанский/французский/русский/арабский/японский/корейский/английский/упрощенный китайский/традиционный китайский Гонконга/традиционный китайский Тайваня
* `Улучшено` Поддержка сборок APK по ABI, включая `arm64-v8a`/`armeabi-v7a` и пакеты `universal`
* `Улучшено` Имена файлов APK выпуска включают имя проекта, номер версии и вариант ABI
* `Улучшено` Унифицировать оформление README и управление версиями платформы Gradle

##### Дополнительную историю выпусков см.

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ru.md)

******

### Сборка

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Сборка Release:

```powershell
.\gradlew.bat :app:assembleRelease
```

Параметры сборки берутся из `version.properties`, текущий min SDK 24 и target SDK 36.

******

### Структура ресурсов

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` предоставляет локализованные описания плагина; `plugin_instruction.md` предоставляет инструкции плагина, отображаемые хостом. README и CHANGELOG генерируются `.python/generate_markdown.py` из исходных файлов JSON.

******

### Ссылки

******

- Документация AutoJs6 OCR: https://docs.autojs6.com/#/ocr
- Официальный проект PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- Официальный проект Paddle Lite: https://github.com/PaddlePaddle/Paddle-Lite
- Официальный сайт OpenCV: https://opencv.org/


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
