from http.server import BaseHTTPRequestHandler
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
    
    # youtube.com/live/ID 형태 (라이브 스트림)
    match = re.search(r"youtube\.com/live/([a-zA-Z0-9_-]+)", url)
    if match:
        return f"https://www.youtube.com/watch?v={match.group(1)}"
    
    # youtube.com/shorts/ID 형태 (쇼츠)
    match = re.search(r"youtube\.com/shorts/([a-zA-Z0-9_-]+)", url)
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
        
        # 모델 선택 (gemini-2.0-flash 사용)
        model_name = 'gemini-2.0-flash'
        logging.info(f"'{model_name}' 모델로 요약 생성 중...")
        
        # 생성 설정 - 출력 토큰 수 늘리기
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2048,  # 최대 출력 토큰 수 (기본값 대비 증가)
            temperature=0.7,  # 창의성 조절 (0.0-1.0)
        )
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
        # 향상된 프롬프트 생성
        prompt = f"""
다음 YouTube 영상의 정보를 바탕으로 가독성 있는 한 페이지의 보고서 형태로 요약하세요. 최종 결과는 한국어로 작성하고, 마크다운 문법은 사용하지 마세요.

요약 구조:
• 개요
• 내용
• 결론

주의사항:
- 마크다운 문법 사용 금지 (**, ##, ```, - 등)
- 일반 텍스트로만 작성
- 불릿 포인트는 • 사용
- 줄바꿈은 자연스럽게

영상 정보
제목: {video_title}
내용: {transcript}
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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 동시 처리 제한
        if not semaphore.acquire(blocking=False):
            logging.warning("동시 처리 한도 초과로 요청을 거부합니다.")
            self.send_response(429)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Too many requests, please try again later."}).encode())
            return

        try:
            # Content-Length 헤더에서 요청 본문 크기 가져오기
            content_length = int(self.headers.get('Content-Length', 0))
            
            # 요청 본문 읽기
            post_data = self.rfile.read(content_length)
            
            # JSON 파싱
            body = json.loads(post_data.decode('utf-8')) if post_data else {}
            
            room = body.get('room')
            sender = body.get('sender')
            message = body.get('msg')
            
            logging.info(f"[{room}] '{sender}'로부터 메시지 수신: {message}")

            if not message:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "no_message"}).encode())
                return

            # URL 정규화 및 ID 추출
            normalized_url = normalize_url(message)
            if not normalized_url:
                logging.info(f"YouTube URL이 아님: {message}")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "not_a_youtube_url"}).encode())
                return
                
            video_id = get_video_id(normalized_url)
            if not video_id:
                logging.error(f"비디오 ID를 추출할 수 없음: {normalized_url}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Could not extract video ID"}).encode())
                return

            logging.info(f"처리 시작: {normalized_url} (ID: {video_id})")

            # 자막 추출 (제목도 함께)
            transcript, language, video_title = get_youtube_transcript(normalized_url)
            
            if not transcript:
                logging.warning(f"자막 추출 실패: {video_id}")
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "자막을 추출할 수 없습니다."}).encode())
                return

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
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "요약을 생성할 수 없습니다."}).encode())
                return

            logging.info("✅ 요약 생성 완료")

            response_data = {
                "summary": summary,
                "video_title": video_title,
                "language": language,
                "transcript_length": len(transcript)
            }

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            logging.error(f"처리 중 오류 발생: {e}", exc_info=True)
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "An internal error occurred"}).encode())
        finally:
            semaphore.release()

    def do_GET(self):
        self.send_response(405)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Method not allowed"}).encode()) 