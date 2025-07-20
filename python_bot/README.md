# 카카오톡 YouTube 봇 - Python 버전 🐍

Python과 pyautokakao를 사용한 카카오톡 YouTube 자막 요약 봇입니다.

## ✨ 주요 기능

- 📺 **YouTube URL 자동 감지**: 채팅방에 올라온 YouTube 링크를 실시간으로 감지
- 🎬 **자막 추출**: Apify API를 통한 다국어 자막 추출
- 🤖 **AI 요약**: Gemini AI를 활용한 스마트한 동영상 요약
- 💬 **자동 응답**: 카카오톡에 요약 결과 자동 전송
- 🔄 **실시간 모니터링**: 여러 채팅방 동시 모니터링

## 🛠️ 설치 및 설정

### 1. 사전 요구사항

- **Windows 10/11** (필수)
- **Python 3.8+**
- **카카오톡 PC 버전** 설치 및 로그인
- **Apify API 토큰**
- **Google Gemini API 키**

### 2. 의존성 설치

```bash
# Python 패키지 설치
pip install -r requirements-python.txt
```

### 3. API 키 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
# API Keys
APIFY_API_TOKEN=your_apify_api_token_here
GEMINI_API_KEY=your_gemini_api_key_here

# Bot Settings (선택사항)
CHECK_INTERVAL=2
MAX_TRANSCRIPT_LENGTH=10000
```

### 4. API 키 발급

#### Apify API 토큰
1. [Apify 콘솔](https://console.apify.com/) 접속
2. Account → Integrations → API tokens에서 토큰 생성

#### Gemini API 키
1. [Google AI Studio](https://aistudio.google.com/) 접속
2. API key 생성

## 🚀 사용법

### 1. 봇 실행

```bash
cd python_bot
python main.py
```

### 2. 채팅방 설정

프로그램 실행 후 모니터링할 카카오톡 채팅방 이름을 입력하세요:

```
채팅방 이름: 친구들,가족,업무방
```

### 3. 봇 사용

1. 카카오톡 채팅방에 YouTube URL을 보내세요
2. 봇이 자동으로 동영상을 분석합니다
3. 몇 초 후 AI가 생성한 요약이 전송됩니다

## 📋 실행 중 명령어

봇 실행 중에 다음 명령어를 사용할 수 있습니다:

- `status`: 봇 상태 확인
- `add <채팅방이름>`: 모니터링 채팅방 추가
- `remove <채팅방이름>`: 모니터링 채팅방 제거
- `help`: 도움말 표시
- `quit` / `exit`: 봇 종료

## ⚠️ 주의사항

### 필수 조건
- **Windows에서만 작동**: pyautokakao는 Windows 전용입니다
- **카카오톡 PC 버전 필요**: 모바일 버전으로는 작동하지 않습니다
- **정확한 채팅방 이름**: 대소문자를 정확히 맞춰야 합니다

### 제약사항
- **UI 기반 자동화**: 화면 상태에 따라 오동작할 수 있습니다
- **메시지 읽기 제한**: pyautokakao의 메시지 읽기 기능이 제한적일 수 있습니다
- **카카오톡 업데이트**: 카카오톡 UI 변경 시 오동작 가능성

## 🔧 문제 해결

### 자주 발생하는 문제

1. **"채팅방을 찾을 수 없습니다"**
   - 채팅방 이름을 정확히 입력했는지 확인
   - 카카오톡이 실행되어 있는지 확인

2. **"메시지를 읽을 수 없습니다"**
   - 카카오톡이 활성 상태인지 확인
   - 다른 창이 카카오톡을 가리고 있지 않은지 확인

3. **"API 토큰이 없습니다"**
   - `.env` 파일이 올바른 위치에 있는지 확인
   - API 키가 올바르게 입력되었는지 확인

### 로그 확인

봇 실행 시 콘솔에 표시되는 로그를 통해 문제를 파악할 수 있습니다.

## 🔄 Node.js 버전과의 차이점

| 기능 | Node.js 버전 | Python 버전 |
|------|-------------|-------------|
| 카카오톡 연동 | node-kakao (deprecated) | pyautokakao |
| 플랫폼 지원 | 모든 플랫폼 | Windows만 |
| 안정성 | 높음 (API 기반) | 중간 (UI 기반) |
| 설정 복잡도 | 높음 | 낮음 |
| 메시지 읽기 | 완전 지원 | 제한적 |

## 📝 라이센스

MIT License - 자유롭게 사용하세요!

## 🤝 기여하기

버그 리포트나 개선사항이 있으시면 이슈를 남겨주세요.

---

**💡 팁**: 더 안정적인 봇을 원한다면 안드로이드의 "채팅 자동응답봇" 앱 사용을 고려해보세요! 