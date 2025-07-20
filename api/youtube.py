import re
import os
import threading
import json
import requests
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 동시 처리 제한을 위한 세마포어
semaphore = threading.Semaphore(5) 
# 처리된 URL 추적 (메모리 기반, 재시작 시 초기화)
processed_urls = set()

def normalize_url(url):
    """다양한 형태의 YouTube URL을 표준 watch?v=ID 형태로 정규화합니다."""
    # youtu.be/ID 형태
    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    
    # youtube.com/watch?v=ID 형태 (다른 파라미터 포함 가능)
    match = re.search(r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)", url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    
    return None

def get_video_id(url):
    """정규화된 URL에서 비디오 ID를 추출합니다."""
    match = re.search(r"watch\?v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def get_youtube_transcript(youtube_url):
    """Apify를 사용하여 YouTube 자막을 추출합니다."""
    from apify_client import ApifyClient
    
    # 환경변수에서 API 토큰 가져오기
    api_token = os.environ.get('APIFY_API_TOKEN')
    if not api_token:
        logging.error("APIFY_API_TOKEN 환경변수가 설정되지 않았습니다.")
        return None, None, None
    
    client = ApifyClient(api_token)
    actor_id = "dB9f4B02ocpTICIEY"  # YouTube Transcript Scraper
    
    # 언어 시도 순서
    languages = ['Korean', 'English', 'Default']
    
    for language in languages:
        try:
            logging.info(f"➡️ '{language}' 언어로 추출 시도...")
            
            run_input = {
                "startUrls": [youtube_url],
                "language": language,
                "includeTimestamps": "No"
            }
            
            logging.info(f"🔍 Apify 요청 데이터: {run_input}")
            
            # Actor 실행
            run = client.actor(actor_id).call(run_input=run_input)
            
            # 결과 가져오기 (최대 10번 시도)
            max_attempts = 10
            for attempt in range(max_attempts):
                try:
                    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
                    
                    if items:
                        item = items[0]
                        logging.info(f"📄 데이터 항목 {attempt + 1}: {item}")
                        
                        transcript = item.get('transcript', '')
                        video_title = item.get('videoTitle', '')
                        
                        if transcript and transcript.strip():
                            processed_urls.add(get_video_id(youtube_url))
                            logging.info(f"📊 총 {len(items)}개 항목 처리됨")
                            logging.info(f"✅ '{language}' 언어 자막 추출 성공! (길이: {len(transcript)} 문자)")
                            return transcript.strip(), language, video_title
                        else:
                            logging.warning(f"❌ '{language}' 언어로 자막을 찾을 수 없습니다.")
                            break
                    else:
                        logging.info(f"⏳ 시도 {attempt + 1}/{max_attempts}: 아직 데이터가 없습니다. 2초 후 재시도...")
                        time.sleep(2)
                        
                except Exception as e:
                    logging.error(f"데이터 가져오기 오류 (시도 {attempt + 1}): {e}")
                    time.sleep(2)
            
        except Exception as e:
            logging.error(f"'{language}' 언어 처리 중 오류: {e}")
            continue
    
    logging.error("❌ 모든 언어에서 자막 추출 실패")
    return None, None, None

def summarize_with_gemini(transcript, video_title="YouTube 영상"):
    """Google Gemini API를 사용하여 자막을 요약합니다."""
    import google.generativeai as genai
    
    # 환경변수에서 API 키 가져오기
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        logging.error("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")
        return None
    
    try:
        # Gemini API 설정
        genai.configure(api_key=api_key)
        
        # 모델 선택 (gemini-1.5-flash 사용)
        model_name = 'gemini-1.5-flash'
        logging.info(f"'{model_name}' 모델로 요약 생성 중...")
        
        model = genai.GenerativeModel(model_name)
        
        # 프롬프트 생성
        prompt = f"""
다음은 "{video_title}" 영상의 자막입니다. 이를 한국어로 3-5문장으로 간결하게 요약해주세요.

자막 내용:
{transcript}

요약 조건:
1. 핵심 내용만 포함
2. 한국어로 작성
3. 3-5문장으로 간결하게
4. 불필요한 감탄사나 반복 제거
5. 명확하고 이해하기 쉽게 작성

요약:
"""
        
        # API 호출
        response = model.generate_content(prompt)
        
        if response and response.text:
            summary = response.text.strip()
            logging.info("✅ Gemini 요약 생성 성공")
            return summary
        else:
            logging.error("Gemini API 응답이 비어있습니다.")
            return None
            
    except Exception as e:
        logging.error(f"Gemini API 호출 중 오류 발생: {e}")
        return None

def handler(request):
    """Vercel 서버리스 함수 핸들러"""
    
    # HTTP 메서드 확인
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Method not allowed"})
        }
        
    # 동시 처리 제한
    if not semaphore.acquire(blocking=False):
        logging.warning("동시 처리 한도 초과로 요청을 거부합니다.")
        return {
            'statusCode': 429,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Too many requests, please try again later."})
        }

    try:
        # 요청 데이터 파싱 (Vercel request 객체에서)
        import json as json_module
        if hasattr(request, 'get_json'):
            body = request.get_json() or {}
        elif hasattr(request, 'json'):
            body = request.json or {}
        else:
            # request.body에서 직접 파싱
            body_str = request.body.decode('utf-8') if hasattr(request, 'body') else '{}'
            body = json_module.loads(body_str) if body_str else {}
        
        room = body.get('room')
        sender = body.get('sender')
        message = body.get('msg')
        
        logging.info(f"[{room}] '{sender}'로부터 메시지 수신: {message}")

        if not message:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"status": "no_message"})
            }

        # URL 정규화 및 ID 추출
        normalized_url = normalize_url(message)
        if not normalized_url:
            logging.info(f"YouTube URL이 아님: {message}")
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"status": "not_a_youtube_url"})
            }
            
        video_id = get_video_id(normalized_url)
        if not video_id:
            logging.error(f"비디오 ID를 추출할 수 없음: {normalized_url}")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Could not extract video ID"})
            }

        # 중복 처리 방지
        if video_id in processed_urls:
            logging.info(f"이미 처리된 URL입니다: {video_id}")
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"status": "already_processed"})
            }
            
        logging.info(f"처리 시작: {normalized_url} (ID: {video_id})")

        # 자막 추출 (제목도 함께)
        transcript, language, video_title = get_youtube_transcript(normalized_url)
        
        if not transcript:
            logging.warning(f"자막 추출 실패: {video_id}")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "자막을 추출할 수 없습니다."})
            }

        logging.info(f"✅ '{language}' 자막 추출 성공 (길이: {len(transcript)})")
        
        # 영상 제목이 없는 경우 기본값 설정
        if not video_title:
            logging.warning("⚠️ 영상 제목을 가져오지 못했습니다.")
            video_title = "제목 없음"
        else:
            logging.info(f"🎥 영상 제목: {video_title}")

        # Gemini로 요약 생성
        logging.info("Gemini AI로 요약 생성 중...")
        summary = summarize_with_gemini(transcript, video_title)
        
        if not summary:
            logging.error("요약 생성 실패")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "요약을 생성할 수 없습니다."})
            }

        logging.info("✅ 요약 생성 완료")

        response_data = {
            "summary": summary,
            "video_title": video_title,
            "language": language,
            "transcript_length": len(transcript)
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response_data)
        }

    except Exception as e:
        logging.error(f"처리 중 오류 발생: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "An internal error occurred"})
        }
    finally:
        semaphore.release() 