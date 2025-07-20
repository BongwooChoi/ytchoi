#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apify API 자막 추출 테스트 스크립트
"""

import config
from youtube_transcript import YouTubeTranscriptExtractor

def test_transcript_extraction():
    """자막 추출 테스트"""
    print("🎬 Apify API 자막 추출 테스트")
    print("=" * 50)
    
    # 테스트할 YouTube 영상들 (자막이 있는 영상들)
    test_urls = [
        "https://www.youtube.com/watch?v=UF8uR6Z6KLc",  # Stanford 강연
        "https://www.youtube.com/watch?v=_VwNVgdJGaQ",  # TED 강연
        "https://www.youtube.com/watch?v=W_VV2Fx32_Y",  # 한국어 영상
    ]
    
    extractor = YouTubeTranscriptExtractor()
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. 테스트 URL: {url}")
        print("자막 추출 중...")
        
        try:
            result = extractor.extract_with_fallback(url)
            
            if result and result.get('success'):
                print("✅ 자막 추출 성공!")
                print(f"   언어: {result.get('language', '알 수 없음')}")
                print(f"   제목: {result.get('title', '제목 없음')}")
                transcript = result.get('transcript', '')
                preview = transcript[:150] + "..." if len(transcript) > 150 else transcript
                print(f"   미리보기: {preview}")
                break  # 성공하면 테스트 중단
            else:
                print("❌ 자막 추출 실패")
                if result:
                    print(f"   결과: {result}")
                
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_transcript_extraction() 