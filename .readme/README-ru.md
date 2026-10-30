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

Плагин AutoJs6 Paddle OCR (PP-OCRv3) добавляет оптическое распознавание символов на базе PaddleOCR PP-OCRv3 и ONNX Runtime, с поддержкой снимков экрана, локальных файлов изображений и необработанного ввода изображений. Начиная с версии 2.0.0 он работает на ONNX Runtime вместо Paddle Lite, поддерживает четыре ABI и выпускается в виде пяти языковых пакетов.

> **Версия Paddle Lite**: реализация Paddle Lite из 1.0.x теперь выпускается отдельно под названием [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) (ID плагина `paddle-ocr-pp-ocrv3-paddle-lite`, вариант `v3-paddle-lite`). Она поддерживает только arm64-v8a и armeabi-v7a и может быть установлена вместе с этим плагином.

******

### Функции

******

- Выпускается в виде пяти языковых пакетов: китайский упрощённый, английский, китайский традиционный, японский и корейский. Пакет для китайского упрощённого сохраняет имя пакета и ID плагина `paddle-ocr-pp-ocrv3` из 1.0.x; все пакеты используют движок `paddle-ocr` и вариант `v3`.
- Поддерживает `ocr.paddle.recognizeText(image)` и `ocr.paddle.detect(image)` в AutoJs6.
- Поддерживает снимки экрана, локальные файлы изображений и необработанный ввод ARGB_8888.
- Информация о плагине, инструкции, README и CHANGELOG поддерживают испанский/французский/русский/арабский/японский/корейский/английский/упрощенный китайский/традиционный китайский Гонконга/традиционный китайский Тайваня.
- Основан на PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1 и OpenCV 4.8.0, для четырёх ABI: arm64-v8a, armeabi-v7a, x86_64 и x86.
- `useSlim: true` использует модели обнаружения и распознавания, квантованные в int8 динамическим квантованием ONNX Runtime.
- `useCls: true` перед распознаванием определяет направление текста, поэтому читается и текст, повёрнутый на 180 градусов; по умолчанию выключено, как в 1.0.x.
- `useOpenCL` в версии ONNX Runtime сопоставлен с NNAPI: на Android 8.1 (API 27) и новее используется поставщик выполнения NNAPI, на более старых версиях или при сбое запуска NNAPI распознавание возвращается на CPU. Будет ли быстрее, зависит от устройства.
- Изображения могут содержать до 16777216 пикселей; размер буферов необработанных изображений ограничен 64 MiB
- Размер закодированного изображения ограничен 64 MiB с поддержкой файловых дескрипторов и каналов

******

### Языковые пакеты

******

Каждый языковой пакет является отдельным APK, можно установить несколько одновременно:

| Язык | `profile` | ID плагина | Имя пакета | Имя файла APK |
| --- | --- | --- | --- | --- |
| Китайский упрощённый | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| Английский | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| Китайский традиционный | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zh-hant-<ABI>-*.apk` |
| Японский | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| Корейский | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

Выбирайте пакет по тексту, который нужно распознавать: пакет для китайского упрощённого читает и латинские буквы с цифрами и рекомендуется по умолчанию; для китайского традиционного, японского или корейского текста установите соответствующий пакет; для текста только на английском можно установить и английский пакет. Каждый пакет выпускается в пяти APK по ABI: `arm64-v8a` (большинство телефонов), `armeabi-v7a`, `x86_64`, `x86` и `universal` (все четыре ABI, самый большой). Устанавливайте только тот, что подходит устройству.

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

Выбор языкового пакета и параметров распознавания:

```js
let img = images.read("test.png");
/* Использовать японский пакет. */
ocr.paddle(img, { profile: "ja" });
/* Выбрать корейский пакет по ID плагина. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* Использовать квантованные модели и включить классификацию направления текста. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL в версии ONNX Runtime сопоставлен с NNAPI. */
ocr.paddle(img, { useOpenCL: true });
/* Использовать версию Paddle Lite. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

Выбор пакета через `profile` и параметр `useCls` требуют AutoJs6 6.8.0 или новее. Более старые хосты не выбирают пакет по `profile` и не передают `useCls`; если установлено несколько языковых пакетов, укажите нужный через `engineId`.

******

### Методы API

******

Распространенные OCR API включают:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` по умолчанию распознает текущий снимок экрана, а `ocr.paddle(path)` распознает локальный файл изображения.

******

### История выпусков

******

# v2.0.0

###### 2026/10/30

* `Заметка` Распознавание теперь работает на ONNX Runtime вместо Paddle Lite, разработчиком указан SuperMonster003. Прежняя реализация на Paddle Lite выпускается отдельно как Paddle OCR (PP-OCRv3 Paddle Lite) (ID плагина `paddle-ocr-pp-ocrv3-paddle-lite`, вариант `v3-paddle-lite`) и может быть установлена вместе с этим плагином. Версии 1.0.6 и более ранние относятся к этому плагину Paddle Lite, который теперь развивается в отдельном репозитории
* `Заметка` Плагин теперь выпускается в виде пяти языковых пакетов (китайский упрощённый, английский, китайский традиционный, японский и корейский), каждый является отдельным APK; пакет для китайского упрощённого сохраняет прежние имя пакета и ID плагина
* `Заметка` Выбор пакета через `profile` и параметр `useCls` требуют AutoJs6 6.8.0 или новее; более старые хосты не выбирают пакет по `profile` и не передают `useCls`; минимальный код версии хоста, объявленный плагином: 5935 (AutoJs6 6.8.0)
* `Добавлено` Поддержка устройств x86_64 и x86, включая эмуляторы, всего четыре ABI
* `Добавлено` Новый параметр `useCls`: перед распознаванием определяется направление текста, поэтому читается и текст, повёрнутый на 180 градусов; по умолчанию выключен
* `Добавлено` `useOpenCL` в версии ONNX Runtime сопоставлен с NNAPI: Android 8.1 и новее использует NNAPI, более старые версии или устройства без доступного NNAPI возвращаются на CPU
* `Добавлено` Язык выбирается через `profile` (`zh`, `en`, `zh-hant`, `ja`, `ko`), версия Paddle Lite: через `variant: "v3-paddle-lite"`; без этих параметров среди плагинов PP-OCRv3 по умолчанию используется пакет упрощённого китайского
* `Улучшено` `useSlim` теперь использует модели обнаружения и распознавания, квантованные в int8 динамическим квантованием ONNX Runtime
* `Зависимость` Добавлен ONNX Runtime Android 1.21.1, удалён Paddle Lite
* `Зависимость` Модели PaddleOCR PP-OCRv3 переведены в формат ONNX (конвертированы из официальных моделей вывода), добавлены модели распознавания для английского, китайского традиционного, японского и корейского и модель направления текста
* `Зависимость` OpenCV 4.8.0 снова поставляется как общая библиотека libopencv_java4.so, по одной на ABI, как в плагине PP-OCRv4 (в 1.0.6 она была статически связана с libNative.so). Упакованные приложения берут эту библиотеку из плагина OpenCV, а не из этого плагина: при упаковке с этим плагином OpenCV добавляется автоматически, а если он не установлен, упаковка завершается ошибкой

# v1.0.6

###### 2026/10/10

* `Заметка` Для упакованных приложений с этой версией нужен хост AutoJs6 6.8.0 или новее; старые хосты могут упаковать плагин только вместе с OpenCV
* `Исправлено` Нативные ошибки при загрузке модели или распознавании аварийно завершали процесс плагина; теперь они передаются хосту как ошибки
* `Улучшено` libNative.so больше не экспортирует символы OpenCV, а APK больше не содержит libopencv_java4.so и стал меньше; упакованные приложения могут использовать плагин вместе с другой версией OpenCV
* `Зависимость` Удалён OpenCV Android AAR 4.8.0; остаётся только статически связанный OpenCV Android SDK 4.8.0 с проверкой SHA-256 при загрузке

# v1.0.5

###### 2026/10/05

* `Исправлено` Предупреждения чтения SDK XML v4 с AGP 9.1 и ошибочный запуск проверки выравнивания нативных библиотек APK при сборке модульных тестов JVM, устраненные общими плагинами сборки 1.8.3
* `Улучшено` Подняты compileSdk и targetSdk до 37 (Android 17); поведение плагина не зависит от нового целевого уровня
* `Улучшено` Значки в сведениях о приложении Android используют изображения и светлый и тёмный фон Icon Studio, сохраняя прозрачные изображения центра плагинов и существующие варианты значков лаунчера

##### Дополнительную историю выпусков см.

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ru.md)

******

### Сборка

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Сборка Release:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

Параметры сборки берутся из `version.properties`, текущий min SDK 24 и target SDK 37. Модели ONNX не хранятся в репозитории: перед сборкой запустите `prepare_ppocrv3_assets.py`, как показано выше. Скрипт скачивает официальные модели PaddleOCR, конвертирует их в ONNX и сверяет с `libs/ppocr-android-sdk/models.provenance.json`; `--profile` принимает `zh`, `en`, `zhHant`, `ja`, `ko` или `all`. Сторонние компоненты и лицензии перечислены в [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

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
- Официальный проект ONNX Runtime: https://github.com/microsoft/onnxruntime
- Официальный сайт OpenCV: https://opencv.org/
- Плагин Paddle OCR (PP-OCRv3 Paddle Lite): https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
