#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apify API 응답 데이터 구조 디버깅 스크립트
"""

import config
import json
from youtube_transcript import YouTubeTranscriptExtractor

def debug_apify_response():
    """Apify API 응답 구조 확인"""
    print("🔍 Apify API 응답 데이터 구조 디버깅")
    print("=" * 60)
    
    # 성공한 URL 사용
    test_url = "https://www.youtube.com/watch?v=AXWvNFjt4ZM"
    
    try:
        extractor = YouTubeTranscriptExtractor()
        
        print(f"테스트 URL: {test_url}")
        print("API 호출 중...")
        
        # 직접 extract_transcript 호출 (디버그용)
        run_input = {
            "startUrls": [test_url],
            "language": "Default",
            "includeTimestamps": "No"
        }
        
        run = extractor.client.actor(extractor.actor_id).call(run_input=run_input)
        print("✅ API 호출 성공!")
        
        # 데이터셋 ID 확인
        dataset_id = run.get('defaultDatasetId')
        print(f"📊 Dataset ID: {dataset_id}")
        
        if not dataset_id:
            print("❌ Dataset ID를 찾을 수 없습니다.")
            return
        
        # 데이터셋에서 결과 가져오기
        dataset_items = list(extractor.client.dataset(dataset_id).iterate_items())
        print(f"📋 Dataset items 개수: {len(dataset_items)}")
        
        if not dataset_items:
            print("❌ 데이터셋이 비어있습니다.")
            return
        
        # 첫 번째 아이템 구조 분석
        first_item = dataset_items[0]
        print(f"\n📄 첫 번째 아이템 구조:")
        print(f"타입: {type(first_item)}")
        print(f"키들: {list(first_item.keys()) if isinstance(first_item, dict) else 'dict가 아님'}")
        
        # 전체 데이터 출력 (JSON 형태로)
        print(f"\n🔍 전체 데이터 내용:")
        print(json.dumps(first_item, ensure_ascii=False, indent=2))
        
        # 자막 데이터 확인
        if 'transcript' in first_item:
            transcript_data = first_item['transcript']
            print(f"\n📝 자막 데이터 타입: {type(transcript_data)}")
            
            if isinstance(transcript_data, list) and len(transcript_data) > 0:
                print(f"📝 자막 배열 길이: {len(transcript_data)}")
                print(f"📝 첫 번째 자막 아이템: {transcript_data[0]}")
                print(f"📝 첫 번째 자막 아이템 타입: {type(transcript_data[0])}")
            elif isinstance(transcript_data, str):
                print(f"📝 자막이 문자열로 저장됨: {transcript_data[:100]}...")
            else:
                print(f"📝 예상과 다른 자막 데이터 구조: {transcript_data}")
        else:
            print("❌ 'transcript' 키가 없습니다.")
        
        # 제목과 언어 확인
        print(f"\n📄 제목: {first_item.get('title', '없음')}")
        print(f"🌍 언어: {first_item.get('language', '없음')}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_apify_response() 