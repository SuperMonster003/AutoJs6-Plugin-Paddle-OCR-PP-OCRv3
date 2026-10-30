<!--suppress HtmlDeprecatedAttribute, HttpUrlsUsage -->

<div align="center">
  <p>
    <picture>
      <img src="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/res/mipmap/ic_launcher.png?raw=true" alt="autojs6-plugin-paddle-ocr-pp-ocrv3-ic-launcher" border="0" width="128" />
    </picture>
  </p>

  <p>AutoJs6용 Paddle OCR PP-OCRv3 텍스트 인식 플러그인</p>

  <p>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/releases"><img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?label=Release"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/issues"><img alt="GitHub closed issues" src="https://img.shields.io/github/issues/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=A24232&label=Issues"/></a>
    <a href="https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/LICENSE"><img alt="GitHub License" src="https://img.shields.io/github/license/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3?color=534BAE&label=License"/></a>
  </p>
</div>

******

### 언어

******

현재 README.md 는 다음 언어를 지원합니다:

- [简体中文 [zh-Hans]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hans.md)
- [繁體中文 (香港) [zh-Hant-HK]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-HK.md)
- [繁體中文 (台灣) [zh-Hant-TW]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-zh-Hant-TW.md)
- [English [en]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-en.md)
- [Français [fr]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-fr.md)
- [Español [es]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-es.md)
- [日本語 [ja]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ja.md)
- 한국어 [ko] # 현재
- [Русский [ru]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ru.md)
- [العربية [ar]](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/.readme/README-ar.md)

******

### 소개

******

AutoJs6 Paddle OCR (PP-OCRv3) 플러그인은 PaddleOCR PP-OCRv3 와 ONNX Runtime 기반 광학 문자 인식 기능을 AutoJs6 에 추가하며, 화면 캡처, 로컬 이미지 파일, 원시 이미지 입력을 지원합니다. 2.0.0 부터 추론 엔진을 Paddle Lite 에서 ONNX Runtime 으로 바꾸어 4 개 ABI 를 지원하며, 인식 언어별로 5 개 언어 패키지로 나뉩니다.

> **Paddle Lite 버전**: 1.0.x 의 Paddle Lite 구현은 [Paddle OCR (PP-OCRv3 Paddle Lite)](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite) 로 이름을 바꾸어 별도로 배포됩니다 (플러그인 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 변형 `v3-paddle-lite`). arm64-v8a 와 armeabi-v7a 만 지원하며 이 플러그인과 함께 설치할 수 있습니다.

******

### 기능

******

- 중국어 간체, 영어, 중국어 번체, 일본어, 한국어의 5 개 언어 패키지를 제공합니다. 중국어 간체 패키지는 1.0.x 의 패키지 이름과 플러그인 ID `paddle-ocr-pp-ocrv3` 를 그대로 사용하며, 모든 패키지의 엔진은 `paddle-ocr`, 변형은 `v3` 입니다.
- AutoJs6 의 `ocr.paddle.recognizeText(image)` 와 `ocr.paddle.detect(image)` 를 지원합니다.
- 화면 캡처, 로컬 이미지 파일, 원시 ARGB_8888 이미지 입력을 지원합니다.
- 플러그인 정보, 사용 설명, README, CHANGELOG 는 스페인어/프랑스어/러시아어/아랍어/일본어/한국어/영어/중국어 간체/홍콩 번체 중국어/대만 번체 중국어를 지원합니다.
- PaddleOCR PP-OCRv3, ONNX Runtime 1.21.1, OpenCV 4.8.0 기반이며 arm64-v8a, armeabi-v7a, x86_64, x86 의 4 개 ABI 를 지원합니다.
- `useSlim: true` 는 ONNX Runtime 동적 양자화 (int8) 로 만든 검출 및 인식 모델을 사용합니다.
- `useCls: true` 는 인식 전에 글자 방향을 판별하여 180 도 회전한 글자도 인식합니다. 기본값은 꺼짐이며 1.0.x 와 같습니다.
- `useOpenCL` 은 ONNX Runtime 버전에서 NNAPI 로 매핑됩니다. Android 8.1 (API 27) 이상에서는 NNAPI 실행 공급자를 사용하고, 그보다 낮은 버전이거나 NNAPI 초기화에 실패하면 CPU 로 돌아갑니다. 더 빨라지는지는 기기마다 다릅니다.
- 이미지는 최대 16777216픽셀, 원시 이미지 버퍼는 최대 64 MiB까지 지원
- 인코딩된 이미지는 최대 64 MiB이며 파일 디스크립터와 파이프를 지원합니다

******

### 언어 패키지

******

언어 패키지는 각각 독립된 APK 이며 여러 개를 동시에 설치할 수 있습니다:

| 언어 | `profile` | 플러그인 ID | 패키지 이름 | APK 파일 이름 |
| --- | --- | --- | --- | --- |
| 중국어 간체 | `zh` | `paddle-ocr-pp-ocrv3` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3` | `*-zh-<ABI>-*.apk` |
| 영어 | `en` | `paddle-ocr-pp-ocrv3-en` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.en` | `*-en-<ABI>-*.apk` |
| 중국어 번체 | `zh-hant` | `paddle-ocr-pp-ocrv3-zh-hant` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.zhhant` | `*-zhhant-<ABI>-*.apk` |
| 일본어 | `ja` | `paddle-ocr-pp-ocrv3-ja` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ja` | `*-ja-<ABI>-*.apk` |
| 한국어 | `ko` | `paddle-ocr-pp-ocrv3-ko` | `io.github.supermonster003.autojs6.plugin.paddleocr.v3.ko` | `*-ko-<ABI>-*.apk` |

인식할 글자에 맞는 언어 패키지를 고르세요. 중국어 간체 패키지는 영문자와 숫자도 인식하며 기본 추천입니다. 중국어 번체, 일본어, 한국어 글자에는 해당 언어 패키지를 설치하고, 영어만 인식할 때는 영어 패키지를 설치해도 됩니다. 각 언어 패키지는 ABI 별로 `arm64-v8a` (대부분의 휴대폰), `armeabi-v7a`, `x86_64`, `x86`, `universal` (4 개 ABI 를 모두 포함, 가장 큼) 의 5 개 APK 가 있으며, 기기에 맞는 하나만 설치하면 됩니다.

******

### 사용 예

******

화면 캡처의 텍스트 내용을 인식합니다:

```js
let capt = images.captureScreen();
let texts = ocr.paddle.recognizeText(capt);
console.log(texts.join("\n"));
```

로컬 이미지 파일의 텍스트 내용을 인식합니다. `test.png` 를 예로 사용합니다:

```js
let img = images.read("test.png");
let results = ocr.paddle.detect(img);
console.log(results);
```

축약 형식도 사용할 수 있습니다:

```js
ocr.paddle.recognizeText();
ocr.paddle("test.png");
```

언어 패키지와 옵션 지정:

```js
let img = images.read("test.png");
/* 일본어 패키지를 사용합니다. */
ocr.paddle(img, { profile: "ja" });
/* 플러그인 ID 로 한국어 패키지를 지정합니다. */
ocr.paddle(img, { engineId: "paddle-ocr-pp-ocrv3-ko" });
/* 양자화 모델을 사용하고 글자 방향 분류를 켭니다. */
ocr.paddle(img, { useSlim: true, useCls: true });
/* useOpenCL 은 ONNX Runtime 버전에서 NNAPI 로 매핑됩니다. */
ocr.paddle(img, { useOpenCL: true });
/* Paddle Lite 버전 플러그인을 사용합니다. */
ocr.paddle(img, { variant: "v3-paddle-lite" });
```

`profile` 로 언어 패키지를 고르는 기능과 `useCls` 옵션은 AutoJs6 6.8.0 이상이 필요합니다. 이전 호스트는 `profile` 로 고르지 않고 `useCls` 도 전달하지 않으므로, 여러 언어 패키지를 설치했다면 `engineId` 로 지정하세요.

******

### API 메서드

******

일반적인 OCR API 는 다음과 같습니다:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle(image, options)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` 은 기본적으로 현재 화면 캡처를 인식하고, `ocr.paddle(path)` 는 로컬 이미지 파일을 인식합니다.

******

### 릴리스 기록

******

# v2.0.0

###### 2026/10/30

* `알림` 인식 엔진을 Paddle Lite 에서 ONNX Runtime 으로 바꾸고 개발자를 SuperMonster003 으로 변경했습니다. 기존 Paddle Lite 구현은 Paddle OCR (PP-OCRv3 Paddle Lite) 로 별도 배포되며 (플러그인 ID `paddle-ocr-pp-ocrv3-paddle-lite`, 변형 `v3-paddle-lite`), 이 플러그인과 함께 설치할 수 있습니다
* `알림` 인식 언어별로 중국어 간체, 영어, 중국어 번체, 일본어, 한국어의 5 개 언어 패키지로 나뉘며 각각 독립된 APK 입니다. 중국어 간체 패키지는 기존 패키지 이름과 플러그인 ID 를 그대로 사용합니다
* `알림` `profile` 로 언어 패키지를 고르는 기능과 `useCls` 옵션은 AutoJs6 6.8.0 이상이 필요합니다. 이전 호스트는 `profile` 로 고르지 않고 `useCls` 도 전달하지 않습니다
* `추가` x86_64 와 x86 기기 (에뮬레이터 포함) 를 지원하여 모두 4 개 ABI 를 지원합니다
* `추가` `useCls` 옵션 추가: 인식 전에 글자 방향을 판별하여 180 도 회전한 글자도 인식합니다. 기본값은 꺼짐입니다
* `추가` `useOpenCL` 은 ONNX Runtime 버전에서 NNAPI 로 매핑됩니다. Android 8.1 이상은 NNAPI 를 사용하고, 그보다 낮은 버전이거나 NNAPI 를 쓸 수 없으면 CPU 로 돌아갑니다
* `개선` `useSlim` 은 ONNX Runtime 동적 양자화 (int8) 로 만든 검출 및 인식 모델을 사용합니다
* `의존성` ONNX Runtime Android 1.21.1 추가, Paddle Lite 제거
* `의존성` PaddleOCR PP-OCRv3 모델을 ONNX 형식으로 변경 (공식 추론 모델에서 변환), 영어, 중국어 번체, 일본어, 한국어 인식 모델과 글자 방향 분류 모델 추가
* `의존성` OpenCV 4.8.0 을 공유 라이브러리 libopencv_java4.so 로 제공 (PP-OCRv4 플러그인과 동일)

# v1.0.6

###### 2026/10/10

* `알림` 패키징된 앱에서 이 버전을 사용하려면 호스트가 AutoJs6 6.8.0 이상이어야 함 (이전 호스트는 OpenCV를 함께 선택한 경우에만 패키징 가능)
* `수정` 모델 로드 또는 추론 중 네이티브 예외가 발생하면 플러그인 프로세스가 강제 종료되던 문제 (이제 호스트에 오류로 반환)
* `개선` libNative.so가 더 이상 OpenCV 심볼을 내보내지 않고 APK에 libopencv_java4.so가 포함되지 않아 크기가 줄었으며, 패키징된 앱에서 다른 버전의 OpenCV와 함께 사용 가능
* `의존성` OpenCV Android AAR 4.8.0을 제거하고 정적 링크되는 OpenCV Android SDK 4.8.0만 사용 (다운로드 시 SHA-256 검증)

# v1.0.5

###### 2026/10/05

* `수정` 공유 빌드 플러그인 1.8.3을 통해 AGP 9.1의 SDK XML v4 파싱 경고 및 JVM 단위 테스트 조립 작업에서 APK 네이티브 라이브러리 정렬 검사가 잘못 실행되는 문제 해결
* `개선` compileSdk 와 targetSdk 를 37 (Android 17) 로 올리며, 플러그인 동작은 새 대상 버전의 영향을 받지 않음
* `개선` Android 앱 정보 아이콘에 Icon Studio의 그림과 밝은 배경 및 어두운 배경을 사용하고 플러그인 센터의 투명 그림과 기존 런처 옵션을 유지

##### 더 많은 릴리스 기록은 다음을 참조하세요

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ko.md)

******

### 빌드

******

```powershell
python -I scripts\prepare_ppocrv3_assets.py --profile all --slim
.\gradlew.bat :app:assembleZhDebug
```

Release 빌드:

```powershell
.\gradlew.bat :app:appendDigestToReleasedFiles
```

빌드 매개변수는 `version.properties` 에서 가져오며, 현재 최소 SDK 는 24, 대상 SDK 는 37 입니다. ONNX 모델은 저장소에 포함되지 않습니다. 빌드 전에 위의 `prepare_ppocrv3_assets.py` 를 실행하면 PaddleOCR 공식 모델을 내려받아 ONNX 로 변환하고 `libs/ppocr-android-sdk/models.provenance.json` 과 대조합니다. `--profile` 에는 `zh`, `en`, `zhHant`, `ja`, `ko`, `all` 을 쓸 수 있습니다. 서드파티 구성 요소와 라이선스는 [THIRD_PARTY_NOTICES.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/THIRD_PARTY_NOTICES.md) 를 참고하세요.

******

### 리소스 구조

******

```text
.readme/lang_*.json
.changelog/lang_*.json
.python/generate_markdown.py
app/src/main/assets/doc/CHANGELOG*.md
app/src/main/res/values-*/strings.xml
app/src/main/res/raw-*/plugin_instruction.md
```

`strings.xml` 은 현지화된 플러그인 설명을 제공합니다; `plugin_instruction.md` 는 호스트에 표시되는 플러그인 사용 설명을 제공합니다. README 와 CHANGELOG 는 `.python/generate_markdown.py` 가 JSON 소스 파일에서 생성합니다.

******

### 관련 링크

******

- AutoJs6 OCR 문서: https://docs.autojs6.com/#/ocr
- PaddleOCR 공식 프로젝트: https://github.com/PaddlePaddle/PaddleOCR
- ONNX Runtime 공식 프로젝트: https://github.com/microsoft/onnxruntime
- OpenCV 공식 웹사이트: https://opencv.org/
- Paddle OCR (PP-OCRv3 Paddle Lite) 플러그인: https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3-Paddle-Lite


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
