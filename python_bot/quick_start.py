#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
빠른 봇 테스트용 스크립트
"""

import os
import sys
from dotenv import load_dotenv
from kakao_bot import KakaoYouTubeBot

def quick_start():
    """빠른 시작"""
    print("🚀 빠른 봇 테스트 시작")
    print("=" * 50)
    
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    apify_token = os.getenv('APIFY_API_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not apify_token or not gemini_key:
        print("❌ API 키가 설정되지 않았습니다!")
        print("💡 .env 파일을 확인하세요.")
        return
    
    print("✅ API 키 확인 완료")
    
    # 봇 생성
    bot = KakaoYouTubeBot(apify_token=apify_token, gemini_key=gemini_key)
    
    # 채팅방 이름 입력받기
    print("\n💬 모니터링할 채팅방 이름을 입력하세요:")
    room_name = input("채팅방 이름: ").strip()
    
    if not room_name:
        print("❌ 채팅방 이름이 입력되지 않았습니다.")
        return
    
    bot.add_room(room_name)
    print(f"✅ '{room_name}' 채팅방 추가 완료")
    
    # 봇 시작
    print("\n🤖 봇을 시작합니다...")
    bot.start()
    
    if bot.is_running:
        print("✅ 봇이 성공적으로 시작되었습니다!")
        print(f"🔄 '{room_name}' 채팅방을 모니터링 중...")
        print("\n💡 테스트 방법:")
        print("   1. 카카오톡 채팅방에 YouTube URL을 보내세요")
        print("   2. 예: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("   3. 봇이 자동으로 응답할 것입니다")
        print("\n🔄 상태 확인: 'status' 입력")
        print("🛑 종료: 'quit' 입력")
        
        # 명령어 루프
        while True:
            try:
                command = input("\n명령어: ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'status':
                    status = bot.get_status()
                    print(f"📊 봇 상태:")
                    print(f"   - 실행 중: {'✅' if status['is_running'] else '❌'}")
                    print(f"   - 모니터링 채팅방: {status['monitored_rooms']}")
                    print(f"   - 처리된 메시지: {status['processed_messages_count']}")
                elif command == 'test':
                    print("🧪 연결 테스트를 실행합니다...")
                    if bot.check_kakao_status():
                        print("✅ 카카오톡 연결 정상")
                    else:
                        print("❌ 카카오톡 연결 문제")
                elif command == 'help':
                    print("📖 사용 가능한 명령어:")
                    print("   - status: 봇 상태 확인")
                    print("   - test: 카카오톡 연결 테스트")
                    print("   - quit: 봇 종료")
                    print("   - help: 도움말")
                else:
                    print("❓ 알 수 없는 명령어. 'help' 입력으로 도움말 확인")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 오류: {e}")
    
    else:
        print("❌ 봇 시작 실패!")
        print("💡 문제 해결 방법:")
        print("   1. 카카오톡 PC 버전을 실행하세요")
        print("   2. 카카오톡에 로그인하세요")
        print("   3. Python을 관리자 권한으로 실행해보세요")
    
    # 봇 정리
    bot.stop()
    print("👋 봇이 종료되었습니다.")

if __name__ == "__main__":
    try:
        quick_start()
    except Exception as e:
        print(f"💥 치명적 오류: {e}")
        import traceback
        traceback.print_exc() 