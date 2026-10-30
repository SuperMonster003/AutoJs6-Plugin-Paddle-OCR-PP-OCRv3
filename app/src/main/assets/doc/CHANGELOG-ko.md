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

# v1.0.4

###### 2026/09/13

* `수정` 초기화 중 문자열 변환 시 JNI 임시 참조 정리가 불완전한 문제를 해결하고 JNI 예외 발생 시 초기화를 즉시 중단 _[`issue #575`](http://issues.autojs6.com/575)_
* `수정` 플러그인 센터의 버전과 ABI 정보가 설치된 APK와 일치
* `수정` 인코딩된 이미지는 최대 64 MiB이며 파일 디스크립터와 파이프를 지원합니다
* `수정` 버전 날짜를 일관된 영어 형식으로 표시
* `개선` 다운로드 파일 생성 전에 릴리스 APK의 버전, 서명 및 전체 변형 구성을 검증
* `개선` 이미지는 최대 16777216픽셀, 원시 이미지 버퍼는 최대 64 MiB까지 지원

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

# v1.0.0

###### 2026/09/01

* `추가` Paddle OCR (PP-OCRv3) 플러그인 서비스, 플러그인 ID `paddle-ocr-pp-ocrv3`, 엔진 `paddle-ocr`, 변형 `v3`
* `추가` `org.autojs.plugin.PADDLE_OCR` 를 통한 플러그인 발견 및 호출 지원
* `추가` 화면 캡처, 로컬 이미지 파일, 원시 ARGB_8888 이미지 입력에 대해 `ocr.paddle.recognizeText(image)` 텍스트 인식과 `ocr.paddle.detect(image)` 텍스트 감지 지원
* `추가` PaddleOCR PP-OCRv3 CPU 모델을 포함하고 Paddle Lite 및 OpenCV 4.8.0 으로 실행
* `추가` 플러그인 정보, 사용 설명, README, CHANGELOG 의 다국어 리소스: 스페인어/프랑스어/러시아어/아랍어/일본어/한국어/영어/중국어 간체/홍콩 번체 중국어/대만 번체 중국어
* `개선` `arm64-v8a`/`armeabi-v7a` 및 `universal` 패키지를 포함한 ABI 별 APK 빌드 지원
* `개선` 릴리스 APK 파일 이름에 프로젝트 이름, 버전 번호, ABI 변형 포함
* `개선` README 레이아웃과 Gradle 플랫폼 버전 관리 방식을 통일
