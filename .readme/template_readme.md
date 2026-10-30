<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="{{ repo_url }}/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="{{ icon_alt }}" border="0" width="128" />
    </picture>
  </p>

  <p>{{ text_plugin_synopsis }}</p>

  <p>
    <a href="{{ repo_url }}/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/{{ repo_slug }}?label=Release"/></a>
    <a href="{{ repo_url }}/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/{{ repo_slug }}?color=A24232&label=Issues"/></a>
    <a href="{{ license_url }}"><img alt="GitHub License" src="https://img.shields.io/github/license/{{ repo_slug }}?color=534BAE&label=License"/></a>
  </p>
</div>

******

### {{ h3_languages_with_ascii }}

******

{{ p_languages_all_supported_for_readme }}:

{{ placeholder_ul_languages_all_supported }}

******

### {{ h3_introduction }}

******

{{ p_introduction }}

> {{ p_paddle_lite_edition }}

******

### {{ h3_functions }}

******

{{ placeholder_features }}

******

### {{ h3_language_packages }}

******

{{ p_language_packages }}:

| {{ th_language }} | `profile` | {{ th_plugin_id }} | {{ th_package_name }} | {{ th_apk }} |
| --- | --- | --- | --- | --- |
| {{ text_lang_zh }} | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| {{ text_lang_en }} | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| {{ text_lang_zh_hant }} | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zh-hant-<ABI>-*.apk` |
| {{ text_lang_ja }} | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| {{ text_lang_ko }} | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |
| {{ text_lang_latin }} | `latin` | `paddle-ocr-pp-ocrv3-latin` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.latin` | `*-latin-<ABI>-*.apk` |
| {{ text_lang_arabic }} | `arabic` | `paddle-ocr-pp-ocrv3-arabic` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.arabic` | `*-arabic-<ABI>-*.apk` |
| {{ text_lang_cyrillic }} | `cyrillic` | `paddle-ocr-pp-ocrv3-cyrillic` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.cyrillic` | `*-cyrillic-<ABI>-*.apk` |
| {{ text_lang_devanagari }} | `devanagari` | `paddle-ocr-pp-ocrv3-devanagari` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.devanagari` | `*-devanagari-<ABI>-*.apk` |
| {{ text_lang_te }} | `te` | `paddle-ocr-pp-ocrv3-te` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.te` | `*-te-<ABI>-*.apk` |
| {{ text_lang_ka }} | `ka` | `paddle-ocr-pp-ocrv3-ka` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ka` | `*-ka-<ABI>-*.apk` |
| {{ text_lang_ta }} | `ta` | `paddle-ocr-pp-ocrv3-ta` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ta` | `*-ta-<ABI>-*.apk` |

{{ p_which_to_install }}

******

### {{ h3_usage }}

******

{{ p_usage_screenshot }}:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

{{ p_usage_local_file }}:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

{{ p_usage_shortcut }}:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

{{ p_usage_options }}:

```js
let img = images.read("test.png");
/* {{ text_comment_profile }} */
ocr.paddle(img, { profile: "ja" });
/* {{ text_comment_engine_id }} */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* {{ text_comment_slim_cls }} */
ocr.paddle(img, { useSlim: true, useCls: true });
/* {{ text_comment_nnapi }} */
ocr.paddle(img, { useOpenCL: true });
/* {{ text_comment_paddle_lite }} */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

{{ p_usage_options_note }}.

******

### {{ h3_api_methods }}

******

{{ p_api_methods }}:

```text
{{ placeholder_api_methods }}
```

{{ p_api_shortcuts }}.

******

### {{ h3_release_history }}

******

{{ placeholder_latest_release_history }}

##### {{ h5_for_more_release_history }}

* {{ placeholder_read_more_in_changelog_md }}

******

### {{ h3_build }}

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

{{ text_release_build }}:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

{{ p_build_params }}.

******

### {{ h3_resource_layout }}

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

{{ p_resource_layout }}.

******

### {{ h3_links }}

******

- {{ text_link_autojs6_ocr_docs }}: {{ docs_ocr_url }}
- {{ text_link_paddle_ocr }}: {{ paddle_ocr_url }}
- {{ text_link_onnxruntime }}: {{ onnxruntime_url }}
- {{ text_link_opencv }}: {{ opencv_url }}
- {{ text_link_paddle_lite_plugin }}: {{ paddle_lite_plugin_url }}


[16 KB page alignment and build verification]({{ repo_url }}/blob/master/docs/16kb.md)
