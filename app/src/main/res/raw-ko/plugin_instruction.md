Paddle OCR을 사용해 화면 캡처의 텍스트 내용을 인식합니다:

```js
/* 전체 형식. */

let capt = images.captureScreen();
ocr.paddle.recognizeText(capt);

/* 축약 형식. */

ocr.paddle.recognizeText();

/* 최소 형식. */

ocr.paddle();
```

Paddle OCR을 사용해 로컬 이미지 파일의 텍스트 내용을 인식합니다 (`test.png` 예시):

```js
/* 전체 형식. */

let img = images.read("test.png");
ocr.paddle.recognizeText(img);

/* 축약 형식. */

ocr.paddle.recognizeText("test.png");

/* 최소 형식. */

ocr.paddle("test.png");
```

언어 패키지와 인식 옵션을 지정합니다 (`profile` 과 `useCls` 는 AutoJs6 6.8.0 이상 필요):

```js
let img = images.read("test.png");

/* 일본어 패키지를 사용합니다. */

ocr.paddle(img, { profile: "ja" });

/* 인식 전에 글자 방향을 판별하여 180 도 회전한 글자도 인식합니다 (기본값 꺼짐). */

ocr.paddle(img, { useCls: true });

/* useOpenCL 은 ONNX Runtime 버전에서 NNAPI 로 매핑되며, 쓸 수 없으면 CPU 로 돌아갑니다. */

ocr.paddle(img, { useOpenCL: true });
```

더 많은 사용 방법은 AutoJs6 앱 문서의 [광학 문자 인식 (OCR)](https://docs.autojs6.com/#/ocr)
섹션을 참고하세요.