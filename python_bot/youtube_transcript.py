import os
from apify_client import ApifyClient
import time
from typing import Optional, Dict

def get_youtube_transcript_backup(url: str):
    """
    백업용 Apify Actor를 사용하여 YouTube 자막을 추출합니다.
    """
    try:
        client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))
        
        # 다른 YouTube 자막 추출 Actor 시도
        run_input = {
            "startUrls": [url],
            "maxRequestRetries": 2
        }
        
        print(f"🔄 백업 Actor로 시도: {run_input}")
        
        # 다른 Actor 사용 (예: youtube-transcript-extractor)
        run = client.actor("drobnikj/youtube-transcript-extractor").call(run_input=run_input)
        
        if run and run.get('status') == 'SUCCEEDED':
            print("✅ 백업 Actor 실행 성공!")
            
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                print(f"📄 백업 데이터: {item}")
                
                # 다양한 필드명 시도
                text = item.get("transcript") or item.get("text") or item.get("content") or item.get("subtitle")
                video_title = item.get("videoTitle") or item.get("title") or item.get("name")
                
                if text:
                    return text.strip(), "backup", video_title
        
        print("❌ 백업 Actor도 실패")
        return None, None, None
        
    except Exception as e:
        print(f"❌ 백업 Actor 오류: {e}")
        return None, None, None

def get_youtube_transcript(url: str, prefer_korean: bool = True):
    """
    Apify를 사용하여 YouTube 동영상의 자막을 추출합니다.
    먼저 기본 Actor를 시도하고, 실패하면 백업 Actor를 시도합니다.
    """
    # 먼저 기본 Actor 시도
    transcript, lang, video_title = get_youtube_transcript_main(url, prefer_korean)
    
    if transcript:
        return transcript, lang, video_title
    
    # 기본 Actor 실패 시 백업 Actor 시도
    print("🔄 기본 Actor 실패, 백업 Actor로 시도합니다...")
    return get_youtube_transcript_backup(url)

def get_youtube_transcript_main(url: str, prefer_korean: bool = True):
    """
    메인 Apify Actor를 사용하여 YouTube 동영상의 자막을 추출합니다.
    공식 샘플 코드 형식을 따릅니다.
    """
    languages = ["Korean", "English", "Japanese"] if prefer_korean else ["English", "Japanese"]
    
    for lang in languages:
        print(f"➡️ '{lang}' 언어로 추출 시도...")
        try:
            client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))
            
            # 공식 샘플에 맞춘 정확한 형식
            run_input = {
                "startUrls": [url],  # 단순 문자열 배열
                "language": lang,
                "includeTimestamps": "No"  # 공식 샘플의 필수 파라미터
            }
            
            print(f"🔍 Apify 요청 데이터: {run_input}")
            
            # 공식 샘플의 정확한 Actor ID 사용
            run = client.actor("dB9f4B02ocpTICIEY").call(run_input=run_input)

            if run and run.get('status') == 'SUCCEEDED':
                print(f"✅ Apify 실행 성공, 데이터셋 확인 중...")
                transcript = ""
                video_title = None
                item_count = 0
                
                for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                    item_count += 1
                    print(f"📄 데이터 항목 {item_count}: {item}")
                    
                    # 실제 필드명인 'transcript' 사용
                    text = item.get("transcript") or item.get("text")
                    if text:
                        transcript += text + " "
                    
                    # 영상 제목도 함께 추출
                    if not video_title:
                        video_title = item.get("videoTitle")
                
                print(f"📊 총 {item_count}개 항목 처리됨")
                
                if transcript.strip():
                    print(f"✅ '{lang}' 언어 자막 추출 성공! (길이: {len(transcript)} 문자)")
                    print(f"🎥 영상 제목: {video_title}")
                    return transcript.strip(), lang, video_title
                else:
                    print(f"⚠️ '{lang}' 언어 데이터는 있지만 텍스트가 비어있음")

            else:
                print(f"❌ '{lang}' 언어 Apify 실행 실패: {run}")

        except Exception as e:
            print(f"❌ '{lang}' 언어 추출 중 오류 발생: {e}")
            continue

    print("❌ 모든 언어로 자막 추출에 실패했습니다.")
    return None, None, None

def get_video_title(url: str) -> str:
    """Apify를 사용하여 YouTube 영상의 제목을 가져옵니다."""
    print(f"🎥 영상 제목 가져오는 중: {url}")
    try:
        run_input = {
            "startUrls": [{"url": url}],
            "maxRequestRetries": 2,
        }
        
        client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))
        run = client.actor("topaz_sharingan/youtube-transcript-scraper-1").call(run_input=run_input)

        if run and run.get('status') == 'SUCCEEDED':
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                title = item.get("title")
                if title:
                    print(f"✅ 영상 제목: {title}")
                    return title
        print("⚠️ 영상 제목을 가져오지 못했습니다.")
        return "제목 없음"
    except Exception as e:
        print(f"❌ 영상 제목 추출 중 오류 발생: {e}")
        return "제목 없음"

# 사용 예제
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=your_video_id"
    # API 키가 설정되어 있어야 합니다.
    # os.environ['APIFY_API_KEY'] = 'YOUR_APIFY_KEY'
    
    if os.environ.get("APIFY_API_KEY"):
        title = get_video_title(test_url)
        print(f"\nTitle: {title}")
        
        transcript, lang, video_title = get_youtube_transcript(test_url)
        if transcript:
            print(f"\nTranscript ({lang}):\n{transcript[:500]}...")
            print(f"Video Title: {video_title}")
    else:
        print("테스트를 위해 APIFY_API_KEY 환경 변수를 설정해주세요.") 