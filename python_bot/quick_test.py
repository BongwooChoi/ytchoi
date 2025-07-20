#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
간단한 기능 테스트 스크립트
"""

from youtube_detector import YouTubeDetector

def test_youtube_detection():
    """YouTube URL 감지 테스트"""
    print("🔍 YouTube URL 감지 기능 테스트")
    print("=" * 50)
    
    detector = YouTubeDetector()
    
    # 테스트 메시지들
    test_messages = [
        "안녕하세요! 이 영상 보세요: https://www.youtube.com/watch?v=dQw4w9WgXcQ 재미있어요!",
        "https://youtu.be/dQw4w9WgXcQ",
        "YouTube 링크가 없는 일반 메시지입니다.",
        "여러 링크: https://www.youtube.com/watch?v=abc123 그리고 https://youtu.be/def456",
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 테스트 메시지: {message}")
        result = detector.detect_urls(message)
        
        if result:
            print(f"   ✅ 감지된 URL 개수: {len(result)}")
            for url_info in result:
                print(f"      - Video ID: {url_info['video_id']}")
                print(f"      - Clean URL: {url_info['clean_url']}")
        else:
            print("   ❌ YouTube URL이 감지되지 않았습니다.")

def test_pyautokakao_status():
    """pyautokakao 상태 테스트"""
    print("\n📱 pyautokakao 라이브러리 상태 확인")
    print("=" * 50)
    
    try:
        import pyautokakao
        print("✅ pyautokakao 라이브러리가 정상적으로 로드되었습니다.")
        print("⚠️  실제 카카오톡 연동은 카카오톡 PC 프로그램이 실행된 상태에서만 가능합니다.")
        return True
    except Exception as e:
        print(f"❌ pyautokakao 라이브러리 문제: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Python 카카오톡 봇 기능 테스트 시작\n")
    
    # YouTube URL 감지 테스트
    test_youtube_detection()
    
    # pyautokakao 상태 테스트
    test_pyautokakao_status()
    
    print("\n🎉 기능 테스트 완료!")
    print("\n💡 다음 단계:")
    print("   1. .env 파일에 API 키 설정")
    print("   2. 카카오톡 PC 프로그램 실행")
    print("   3. python main.py 명령어로 봇 시작") 