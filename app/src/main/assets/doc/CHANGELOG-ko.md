******

### 릴리스 기록

******

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
