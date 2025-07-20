#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
간단한 봇 시작 스크립트 (인코딩 문제 해결)
"""

import os
import sys
from dotenv import load_dotenv

def simple_start():
    """간단한 봇 시작"""
    print("🚀 YouTube 봇 시작")
    print("=" * 40)
    
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    apify_token = os.getenv('APIFY_API_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not apify_token:
        print("❌ APIFY_API_TOKEN이 설정되지 않았습니다!")
        return False
    
    if not gemini_key:
        print("❌ GEMINI_API_KEY가 설정되지 않았습니다!")
        return False
    
    print("✅ API 키 확인 완료")
    
    # 봇 import 및 생성
    try:
        from kakao_bot import KakaoYouTubeBot
        bot = KakaoYouTubeBot(apify_token=apify_token, gemini_key=gemini_key)
        print("✅ 봇 생성 완료")
    except Exception as e:
        print(f"❌ 봇 생성 실패: {e}")
        return False
    
    # 채팅방 설정
    print("\n💬 모니터링할 채팅방 이름을 입력하세요:")
    print("   (여러 개는 쉼표로 구분: 방1,방2,방3)")
    rooms_input = input("채팅방 이름: ").strip()
    
    if not rooms_input:
        print("❌ 채팅방 이름이 필요합니다.")
        return False
    
    # 채팅방 추가
    rooms = [room.strip() for room in rooms_input.split(',')]
    for room in rooms:
        bot.add_room(room)
        print(f"✅ '{room}' 추가됨")
    
    # 카카오톡 상태 확인
    print("\n🔍 카카오톡 상태 확인 중...")
    if not bot.check_kakao_status():
        print("❌ 카카오톡 연결 실패!")
        print("💡 해결 방법:")
        print("   1. 카카오톡 PC 버전을 실행하세요")
        print("   2. 카카오톡에 로그인하세요")
        print("   3. 채팅방 이름을 정확히 입력했는지 확인하세요")
        return False
    
    # 봇 시작
    print("\n🤖 봇을 시작합니다...")
    bot.start()
    
    if not bot.is_running:
        print("❌ 봇 시작 실패!")
        return False
    
    print("✅ 봇이 성공적으로 시작되었습니다!")
    print(f"🔄 모니터링 중: {list(bot.monitored_rooms)}")
    print("\n💡 사용법:")
    print("   1. 카카오톡 채팅방에 YouTube URL을 보내세요")
    print("   2. 예: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print("   3. 봇이 자동으로 요약을 전송합니다")
    print("\n📋 명령어:")
    print("   - 'status': 봇 상태 확인")
    print("   - 'quit': 봇 종료")
    
    # 메인 루프
    try:
        while True:
            command = input("\n명령어: ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                break
            elif command == 'status':
                status = bot.get_status()
                print(f"📊 봇 상태:")
                print(f"   - 실행 중: {'✅' if status['is_running'] else '❌'}")
                print(f"   - 모니터링 채팅방: {status['monitored_rooms']}")
                print(f"   - 처리된 메시지: {status['processed_messages_count']}")
            elif command == '':
                continue
            else:
                print("❓ 사용 가능한 명령어: status, quit")
                
    except KeyboardInterrupt:
        print("\n\n🛑 Ctrl+C로 중단됨")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        bot.stop()
        print("👋 봇이 종료되었습니다.")
    
    return True

if __name__ == "__main__":
    try:
        success = simple_start()
        if not success:
            print("\n💥 봇 실행 실패!")
            print("💡 문제가 지속되면 다음을 확인하세요:")
            print("   1. .env 파일의 API 키")
            print("   2. 카카오톡 PC 버전 실행 상태")
            print("   3. 채팅방 이름 정확성")
    except Exception as e:
        print(f"💥 치명적 오류: {e}")
        import traceback
        traceback.print_exc() 