# 🎥 YouTube 요약 봇

YouTube 영상의 자막을 추출하여 AI로 요약해주는 카카오톡 봇입니다.

## 📋 주요 기능

- **YouTube URL 자동 감지**: 다양한 형태의 YouTube URL 지원
- **자막 추출**: Apify API를 통한 다국어 자막 추출
- **AI 요약**: Google Gemini 2.0 Flash를 통한 고품질 요약
- **실시간 피드백**: 처리 상태와 결과를 카카오톡으로 즉시 전달

## 🔗 지원하는 YouTube URL 형태

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/live/VIDEO_ID` (라이브 스트림)
- `https://www.youtube.com/shorts/VIDEO_ID` (YouTube 쇼츠)

## 🏗️ 시스템 아키텍처

```
[카카오톡] ←→ [안드로이드 폰 + Messenger Bot R] ←→ [Vercel 서버리스 함수] ←→ [Apify API + Gemini API]
```

### 구성 요소
1. **안드로이드 앱**: Messenger Bot R (카카오톡 메시지 감지 및 응답)
2. **서버**: Vercel 서버리스 함수 (24/7 운영)
3. **API**: Apify (자막 추출) + Google Gemini (AI 요약)

## 🚀 설치 및 설정

### 1. 서버 배포 (Vercel)

```bash
# 저장소 클론
git clone https://github.com/BongwooChoi/ytchoi.git
cd ytchoi

# Vercel 배포
vercel --prod
```

### 2. 환경 변수 설정 (Vercel Dashboard)

```
APIFY_API_TOKEN=your_apify_token
GEMINI_API_KEY=your_gemini_api_key
```

### 3. 안드로이드 설정

1. **Messenger Bot R** 앱 설치
2. 카카오톡 접근 권한 허용
3. 배터리 최적화 해제
4. 스크립트 등록 (`messengerbot_script.js` 복사)

## 📱 사용 방법

1. 카카오톡에서 YouTube URL 전송
2. 봇이 자동으로 감지하여 처리 시작 메시지 전송
3. 자막 추출 및 AI 요약 진행
4. 완성된 요약 결과를 카카오톡으로 전송

## 💬 봇 응답 예시

### 성공 시
```
📝 YouTube 영상 요약:

🎥 [영상 제목]

• 영상 개요
• 주요 내용
• 결론 및 시사점
```

### 자막 없는 영상
```
😔 죄송합니다. 이 영상은 자막이 없어서 요약할 수 없어요.

📝 자막이 있는 영상을 올려주시면 요약해드릴게요!
```

## 🛠️ 기술 스택

### 서버 (Python)
- **Vercel**: 서버리스 함수 호스팅
- **BaseHTTPRequestHandler**: HTTP 요청 처리
- **Apify Client**: YouTube 자막 추출
- **Google Generative AI**: 텍스트 요약

### 클라이언트 (JavaScript)
- **Messenger Bot R**: 안드로이드 카카오톡 봇 프레임워크
- **Java HTTP**: 서버와의 통신

## 📊 성능 최적화

- **세마포어**: 동시 처리 요청 수 제한 (최대 5개)
- **타임아웃 설정**: 연결 30초, 읽기 120초
- **언어 fallback**: 한국어 → 영어 → 기본값 순으로 시도
- **토큰 제한 해제**: 최대 2048 토큰으로 완전한 요약


## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

- GitHub: [@BongwooChoi](https://github.com/BongwooChoi)
- 프로젝트 링크: [https://github.com/BongwooChoi/ytchoi](https://github.com/BongwooChoi/ytchoi) 