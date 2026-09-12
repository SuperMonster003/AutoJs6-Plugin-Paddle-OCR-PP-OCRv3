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

AutoJs6 Paddle OCR (PP-OCRv3) 플러그인은 PaddleOCR PP-OCRv3 기반 광학 문자 인식 기능을 AutoJs6 에 추가하며, 화면 캡처, 로컬 이미지 파일, 원시 이미지 입력을 지원합니다.

******

### 기능

******

- `paddle-ocr-pp-ocrv3` 플러그인 서비스를 제공하며, 플러그인 ID 는 `paddle-ocr-pp-ocrv3` 입니다.
- AutoJs6 의 `ocr.paddle.recognizeText(image)` 와 `ocr.paddle.detect(image)` 를 지원합니다.
- 화면 캡처, 로컬 이미지 파일, 원시 ARGB_8888 이미지 입력을 지원합니다.
- 플러그인 정보, 사용 설명, README, CHANGELOG 는 스페인어/프랑스어/러시아어/아랍어/일본어/한국어/영어/중국어 간체/홍콩 번체 중국어/대만 번체 중국어를 지원합니다.
- PaddleOCR PP-OCRv3, Paddle Lite, OpenCV 4.8.0 기반입니다.

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

******

### API 메서드

******

일반적인 OCR API 는 다음과 같습니다:

```text
ocr.paddle.recognizeText(image)
ocr.paddle.detect(image)
ocr.paddle(image)
ocr.paddle.recognizeText()
ocr.paddle()
```

`ocr.paddle()` 은 기본적으로 현재 화면 캡처를 인식하고, `ocr.paddle(path)` 는 로컬 이미지 파일을 인식합니다.

******

### 릴리스 기록

******

# v1.0.3

###### 2026/09/12

* `수정` 프로세스의 첫 문자 검출에 1000 x 320 같은 낮은 이미지를 사용하면 Paddle Lite 가 크래시 (SIGSEGV) 하던 문제를 수정; 이제 첫 실제 검출 전에 960 x 960 빈 이미지로 검출기를 한 번 워밍업함

# v1.0.2

###### 2026/09/12

* `수정` Paddle OCR 네이티브 종속성 정리 설정이 초기화되지 않으면 `clean` 작업이 실패하는 문제
* `개선` OpenCV 4.8.0 네이티브 라이브러리를 NDK r28c (Clang 19.0.1) 재빌드 버전으로 동기화 (donor: AutoJs6-Plugin-OpenCV); 4개 ABI의 `libopencv_java4.so`는 16 KB `PT_LOAD` 정렬을 유지하며 provenance 매니페스트를 포함

# v1.0.1

###### 2026/09/11

* `개선` 64비트 네이티브 라이브러리의 16 KB 페이지 정렬을 빌드 시 검증, manifest 계약 검사 및 JSON 보고서 지원

##### 더 많은 릴리스 기록은 다음을 참조하세요

* [CHANGELOG.md](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/app/src/main/assets/doc/CHANGELOG-ko.md)

******

### 빌드

******

```powershell
.\gradlew.bat :app:assembleDebug
```

Release 빌드:

```powershell
.\gradlew.bat :app:assembleRelease
```

빌드 매개변수는 `version.properties` 에서 가져오며, 현재 최소 SDK 는 24, 대상 SDK 는 36 입니다.

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
- Paddle Lite 공식 프로젝트: https://github.com/PaddlePaddle/Paddle-Lite
- OpenCV 공식 웹사이트: https://opencv.org/


[16 KB page alignment and build verification](https://github.com/SuperMonster003/AutoJs6-Plugin-Paddle-OCR-PP-OCRv3/blob/master/docs/16kb.md)
