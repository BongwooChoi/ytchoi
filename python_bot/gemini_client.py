import google.generativeai as genai
import os

def configure_gemini():
    """Gemini API 키를 설정합니다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
    genai.configure(api_key=api_key)

def summarize_with_gemini(transcript: str, title: str) -> str:
    """
    주어진 텍스트(자막)를 Gemini AI를 사용하여 요약합니다.
    영상 제목을 참고하여 더 자연스러운 요약을 생성합니다.
    """
    configure_gemini()
    
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)

    # 한글 요약을 위한 프롬프트
    prompt = f"""
    당신은 YouTube 영상 요약 전문가입니다. 다음은 '{title}'라는 제목의 영상에서 추출한 자막입니다.
    이 자막 내용을 바탕으로, 영상의 핵심 내용을 3~5개의 주요 항목으로 정리하여 한국어로 요약해주세요.
    각 항목은 글머리 기호(•)로 시작하고, 간결하고 명확하게 설명해야 합니다.
    전체적으로는 친근하고 이해하기 쉬운 어조를 사용해주세요.

    --- 자막 내용 ---
    {transcript}
    --- 자막 끝 ---

    요약:
    """

    try:
        print(f"'{model_name}' 모델로 요약 생성 중...")
        response = model.generate_content(prompt)
        
        # 때때로 response.text가 비어있는 경우를 대비
        if not response.text:
             # response.parts를 직접 확인
            if response.parts:
                summary = "".join(part.text for part in response.parts)
                if summary: return summary.strip()

            print("⚠️ Gemini AI가 비어있는 응답을 반환했습니다.")
            # 실패 시 간단한 대체 텍스트 제공
            return f"'{title}' 영상의 내용을 요약하는 데 실패했습니다."

        return response.text.strip()

    except Exception as e:
        print(f"❌ Gemini AI 요약 중 오류 발생: {e}")
        return f"'{title}' 영상의 내용을 요약 중 오류가 발생했습니다."

# 사용 예시
if __name__ == '__main__':
    # 테스트를 위해 API 키 환경 변수 설정 필요
    # from dotenv import load_dotenv
    # load_dotenv()

    if os.environ.get("GEMINI_API_KEY"):
        sample_title = "파이썬으로 자동화 봇 만들기"
        sample_transcript = """
        안녕하세요, 여러분. 오늘은 파이썬을 사용해서 어떻게 업무를 자동화할 수 있는지 알아보겠습니다.
        파이썬은 매우 강력한 언어이고, 특히 반복적인 작업을 처리하는 데 탁월합니다.
        예를 들어, 매일 아침 여러 웹사이트에서 데이터를 수집해야 한다고 상상해보세요.
        이것을 수동으로 하는 것은 매우 지루하고 시간이 많이 걸립니다.
        하지만 파이썬의 'requests'와 'BeautifulSoup' 라이브러리를 사용하면 단 몇 줄의 코드로 이 과정을 자동화할 수 있습니다.
        먼저 'requests'로 웹사이트의 HTML을 가져오고, 'BeautifulSoup'으로 필요한 데이터를 파싱하는 거죠.
        정말 간단하지 않나요? 이제 여러분도 자동화의 달인이 될 수 있습니다.
        """
        
        summary = summarize_with_gemini(sample_transcript, sample_title)
        print("\n--- 생성된 요약 ---")
        print(summary)
    else:
        print("테스트를 위해 GEMINI_API_KEY 환경 변수를 설정해주세요.") 