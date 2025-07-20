#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
수정된 카카오톡 봇 - 대안 전송 방법 우선 사용
"""

import os
import sys
from dotenv import load_dotenv
from kakao_bot import KakaoYouTubeBot

class FixedKakaoYouTubeBot(KakaoYouTubeBot):
    """대안 전송 방법을 우선 사용하는 수정된 봇"""
    
    def send_response(self, room_name: str, message: str, max_retries: int = 3):
        """응답 메시지를 보냅니다 (대안 방법 우선 사용)"""
        import time
        
        print(f"📤 대안 방법으로 메시지 전송 시작 ({room_name})")
        
        # 바로 대안 전송 방법 사용 (pyautokakao 건너뛰기)
        try:
            print("🔧 대안 전송 방법 시도 (PyAutoGUI + 클립보드)")
            from alternative_send import send_message_alternative
            
            if send_message_alternative(room_name, message):
                print(f"✅ 대안 방법으로 메시지 전송 성공! ({room_name})")
                self.processed_messages.add(message)
                return True
            else:
                print(f"❌ 대안 방법 실패 ({room_name})")
                
        except Exception as e:
            print(f"❌ 대안 방법 오류: {str(e)}")
        
        # 실패 시 사용자에게 알림
        print(f"\n🚨 메시지 전송 실패 알림:")
        print(f"   채팅방: {room_name}")
        print(f"   메시지: {message[:100]}...")
        print(f"   💡 수동으로 복사해서 전송하세요!")
        
        return False

def fixed_start():
    """수정된 봇 시작"""
    print("🚀 수정된 YouTube 봇 시작 (대안 전송 방법 사용)")
    print("=" * 50)
    
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    apify_token = os.getenv('APIFY_API_TOKEN')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not apify_token or not gemini_key:
        print("❌ API 키가 설정되지 않았습니다!")
        return False
    
    print("✅ API 키 확인 완료")
    
    # 수정된 봇 생성
    try:
        bot = FixedKakaoYouTubeBot(apify_token=apify_token, gemini_key=gemini_key)
        print("✅ 수정된 봇 생성 완료")
    except Exception as e:
        print(f"❌ 봇 생성 실패: {e}")
        return False
    
    # 채팅방 설정
    print("\n💬 모니터링할 채팅방 이름을 입력하세요:")
    room_name = input("채팅방 이름: ").strip()
    
    if not room_name:
        print("❌ 채팅방 이름이 필요합니다.")
        return False
    
    bot.add_room(room_name)
    print(f"✅ '{room_name}' 추가됨")
    
    # 카카오톡 상태 확인
    print("\n🔍 카카오톡 상태 확인 중...")
    if not bot.check_kakao_status():
        print("❌ 카카오톡 연결 실패!")
        return False
    
    # 봇 시작
    print("\n🤖 수정된 봇을 시작합니다...")
    bot.start()
    
    if not bot.is_running:
        print("❌ 봇 시작 실패!")
        return False
    
    print("✅ 수정된 봇이 성공적으로 시작되었습니다!")
    print(f"🔄 모니터링 중: {list(bot.monitored_rooms)}")
    print("\n💡 주요 변경사항:")
    print("   - pyautokakao 방법을 건너뛰고 바로 대안 방법 사용")
    print("   - 채팅방 자동 검색 및 이동")
    print("   - 클립보드 기반 메시지 전송")
    print("\n📋 명령어:")
    print("   - 'status': 봇 상태 확인")
    print("   - 'test': 테스트 메시지 전송")
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
            elif command == 'test':
                print("🧪 테스트 메시지 전송...")
                success = bot.send_response(room_name, "🔧 수정된 봇 테스트 메시지입니다!")
                if success:
                    print("✅ 테스트 메시지 전송 성공!")
                else:
                    print("❌ 테스트 메시지 전송 실패")
            elif command == '':
                continue
            else:
                print("❓ 사용 가능한 명령어: status, test, quit")
                
    except KeyboardInterrupt:
        print("\n\n🛑 Ctrl+C로 중단됨")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        bot.stop()
        print("👋 수정된 봇이 종료되었습니다.")
    
    return True

if __name__ == "__main__":
    try:
        success = fixed_start()
        if not success:
            print("\n💥 봇 실행 실패!")
    except Exception as e:
        print(f"💥 치명적 오류: {e}")
        import traceback
        traceback.print_exc() 