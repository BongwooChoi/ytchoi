import re
import os
import threading
import json
import sys

# 현재 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'python_bot'))

# python_bot 모듈들 임포트
from python_bot.youtube_transcript import get_youtube_transcript
from python_bot.gemini_client import summarize_with_gemini

# 로깅 설정
import logging
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
        # 요청 데이터 파싱
        body = request.get_json() or {}
        
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