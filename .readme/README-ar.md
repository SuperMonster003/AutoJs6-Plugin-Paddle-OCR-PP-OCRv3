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

يضيف مكون AutoJs6 Paddle OCR (PP-OCRv3) التعرف الضوئي على الحروف بالاعتماد على PaddleOCR PP-OCRv3 و ONNX Runtime, مع دعم لقطات الشاشة, وملفات الصور المحلية, وإدخال الصور الخام. منذ الإصدار 2.0.0 يعمل على ONNX Runtime بدلا من Paddle Lite, ويدعم أربع واجهات ABI, ويأتي في خمس حزم لغات.

> **إصدار Paddle Lite**: أصبح تنفيذ Paddle Lite من الإصدار 1.0.x ينشر بشكل منفصل باسم [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) (معرف المكون `paddle-ocr-pp-ocrv3-paddle-lite`, والمتغير `v3-paddle-lite`). يدعم arm64-v8a و armeabi-v7a فقط, ويمكن تثبيته مع هذا المكون في الوقت نفسه.

******

### الميزات

******

- يأتي في خمس حزم لغات: الصينية المبسطة, والإنجليزية, والصينية التقليدية, واليابانية, والكورية. تحتفظ حزمة الصينية المبسطة باسم الحزمة ومعرف المكون `paddle-ocr-pp-ocrv3` من الإصدار 1.0.x, وتستخدم جميع الحزم المحرك `paddle-ocr` والمتغير `v3`.
- يدعم `ocr.paddle.recognizeText(image)` و `ocr.paddle.detect(image)` في AutoJs6.
- يدعم لقطات الشاشة, وملفات الصور المحلية, وإدخال صور ARGB_8888 الخام.
- تدعم معلومات المكون, والتعليمات, و README, و CHANGELOG الاسبانية/الفرنسية/الروسية/العربية/اليابانية/الكورية/الانجليزية/الصينية المبسطة/الصينية التقليدية في هونغ كونغ/الصينية التقليدية في تايوان.
- يعتمد على PaddleOCR PP-OCRv3, و ONNX Runtime 1.21.1, و OpenCV 4.8.0, ويدعم أربع واجهات ABI: arm64-v8a, و armeabi-v7a, و x86_64, و x86.
- `useSlim: true` يستخدم نماذج كشف وتعرف مكممة إلى int8 بالتكميم الديناميكي في ONNX Runtime.
- `useCls: true` يحدد اتجاه النص قبل التعرف, فيمكن قراءة النص المدار بمقدار 180 درجة; وهو معطل افتراضيا كما في 1.0.x.
- `useOpenCL` يقابل NNAPI في إصدار ONNX Runtime: على Android 8.1 (API 27) وما بعده يستخدم موفر التنفيذ NNAPI, وفي الإصدارات الأقدم أو عند فشل تشغيل NNAPI يعود التعرف إلى المعالج المركزي CPU. تختلف زيادة السرعة حسب الجهاز.
- تقبل الصور حتى 16777216 بكسل, ويقتصر حجم مخزن الصورة الخام على 64 MiB
- يقتصر حجم الصورة المشفرة على 64 MiB مع دعم واصفات الملفات والأنابيب

******

### حزم اللغات

******

كل حزمة لغة هي APK مستقل, ويمكن تثبيت عدة حزم في الوقت نفسه:

| اللغة | `profile` | معرف المكون | اسم الحزمة | اسم ملف APK |
| --- | --- | --- | --- | --- |
| الصينية المبسطة | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| الإنجليزية | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| الصينية التقليدية | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| اليابانية | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| الكورية | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

اختر الحزمة حسب النص الذي تريد قراءته: حزمة الصينية المبسطة تقرأ أيضا الحروف اللاتينية والأرقام وهي الخيار الموصى به افتراضيا; للنص الصيني التقليدي أو الياباني أو الكوري ثبت الحزمة المقابلة; وللنص الإنجليزي فقط يمكنك أيضا تثبيت الحزمة الإنجليزية. لكل حزمة خمسة ملفات APK حسب ABI: `arm64-v8a` (معظم الهواتف), و `armeabi-v7a`, و `x86_64`, و `x86`, و `universal` (يضم الواجهات الأربع وهو الأكبر). ثبت فقط الملف المناسب لجهازك.

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

اختيار حزمة لغة وضبط خيارات التعرف:

```js
let img = images.read("test.png");
/* استخدام حزمة اليابانية. */
ocr.paddle(img, { profile: "ja" });
/* اختيار حزمة الكورية بمعرف المكون. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* استخدام النماذج المكممة وتفعيل تصنيف اتجاه النص. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL يقابل NNAPI في إصدار ONNX Runtime. */
ocr.paddle(img, { useOpenCL: true });
/* استخدام إصدار Paddle Lite. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

يتطلب اختيار الحزمة عبر `profile` وخيار `useCls` الإصدار AutoJs6 6.8.0 أو أحدث. المضيفات الأقدم لا تختار حسب `profile` ولا تمرر `useCls`; إذا كانت عدة حزم لغات مثبتة فاستخدم `engineId` لاختيار واحدة.

******

### طرق API

******

تشمل واجهات OCR الشائعة:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

يتعرف `ocr.paddle()` افتراضيا على لقطة الشاشة الحالية, ويتعرف `ocr.paddle(path)` على ملف صورة محلي.

******

### سجل الاصدارات

******

# v2.0.0

###### 2026/10/30

* `ملاحظة` أصبح التعرف يعمل على ONNX Runtime بدلا من Paddle Lite, وأصبح المطور SuperMonster003. ينشر تنفيذ Paddle Lite السابق بشكل منفصل باسم Paddle OCR (PP-OCRv3 Paddle Lite) (معرف المكون `paddle-ocr-pp-ocrv3-paddle-lite`, والمتغير `v3-paddle-lite`), ويمكن تثبيته مع هذا المكون
* `ملاحظة` يأتي المكون الآن في خمس حزم لغات (الصينية المبسطة, والإنجليزية, والصينية التقليدية, واليابانية, والكورية), وكل حزمة APK مستقل; تحتفظ حزمة الصينية المبسطة باسم الحزمة ومعرف المكون الأصليين
* `ملاحظة` يتطلب اختيار الحزمة عبر `profile` وخيار `useCls` الإصدار AutoJs6 6.8.0 أو أحدث; المضيفات الأقدم لا تختار حسب `profile` ولا تمرر `useCls`
* `اضافة` دعم أجهزة x86_64 و x86, بما في ذلك المحاكيات, ليصبح المجموع أربع واجهات ABI
* `اضافة` خيار جديد `useCls` يحدد اتجاه النص قبل التعرف لقراءة النص المدار بمقدار 180 درجة أيضا; معطل افتراضيا
* `اضافة` `useOpenCL` يقابل NNAPI في إصدار ONNX Runtime: يستخدم Android 8.1 وما بعده NNAPI, وتعود الإصدارات الأقدم أو الأجهزة التي لا يتوفر فيها NNAPI إلى المعالج المركزي CPU
* `تحسين` `useSlim` يستخدم الآن نماذج كشف وتعرف مكممة إلى int8 بالتكميم الديناميكي في ONNX Runtime
* `اعتماد` إضافة ONNX Runtime Android 1.21.1 وإزالة Paddle Lite
* `اعتماد` تحويل نماذج PaddleOCR PP-OCRv3 إلى صيغة ONNX من نماذج الاستدلال الرسمية, مع نماذج تعرف جديدة للإنجليزية والصينية التقليدية واليابانية والكورية ونموذج لاتجاه النص
* `اعتماد` أصبح OpenCV 4.8.0 يقدم كمكتبة مشتركة libopencv_java4.so, كما في مكون PP-OCRv4

# v1.0.6

###### 2026/10/10

* `ملاحظة` تحتاج التطبيقات المحزّمة التي تستخدم هذا الإصدار إلى AutoJs6 6.8.0 أو أحدث كمضيف; لا يمكن للمضيفات الأقدم تحزيمه إلا مع OpenCV
* `اصلاح` كانت الأخطاء الأصلية أثناء تحميل النموذج أو الاستدلال تنهي عملية المكون الإضافي, وأصبحت تُعاد الآن إلى المضيف كأخطاء
* `تحسين` لم تعد libNative.so تصدّر رموز OpenCV ولم يعد ملف APK يتضمن libopencv_java4.so فأصبح أصغر حجمًا, ويمكن للتطبيقات المحزّمة استخدامه مع إصدار آخر من OpenCV
* `اعتماد` إزالة OpenCV Android AAR 4.8.0 والإبقاء فقط على OpenCV Android SDK 4.8.0 المربوط بشكل ثابت مع التحقق من SHA-256 عند التنزيل

# v1.0.5

###### 2026/10/05

* `اصلاح` تحذيرات قراءة SDK XML v4 مع AGP 9.1 وتشغيل فحص محاذاة مكتبات APK الأصلية خطأ عند تجميع اختبارات JVM, باستخدام إضافات البناء المشتركة 1.8.3
* `تحسين` رفع compileSdk و targetSdk إلى 37 (Android 17)؛ لا يعتمد سلوك المكون الإضافي على الهدف الجديد
* `تحسين` تستخدم أيقونات معلومات التطبيق في Android صور Icon Studio وخلفياته الفاتحة والداكنة مع الحفاظ على الصور الشفافة في مركز الملحقات وخيارات المشغل الحالية

##### لمزيد من سجل الاصدارات, راجع

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ar.md)

******

### البناء

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

بناء Release:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

تأتي معلمات البناء من `version.properties`, مع حد SDK أدنى حالي 24 و SDK هدف 37. نماذج ONNX غير مضمنة في المستودع: قبل البناء شغل `prepare_ppocrv3_assets.py` كما هو موضح أعلاه. يقوم بتنزيل نماذج PaddleOCR الرسمية وتحويلها إلى ONNX والتحقق منها مقابل `libs/ppocr-android-sdk/models.provenance.json`; ويقبل `--profile` القيم `zh` و `en` و `zhHant` و `ja` و `ko` و `all`. المكونات الخارجية وتراخيصها مذكورة في [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md).

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
- مشروع ONNX Runtime الرسمي: https://github.com/microsoft/onnxruntime
- موقع OpenCV الرسمي: https://opencv.org/
- مكون Paddle OCR (PP-OCRv3 Paddle Lite): https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
