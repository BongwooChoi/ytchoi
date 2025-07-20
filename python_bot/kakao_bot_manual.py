#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
수동 복사용 카카오톡 봇 - 콘솔 출력 방식
"""

import os
import sys
from dotenv import load_dotenv
from kakao_bot import KakaoYouTubeBot
import pyperclip

class ManualCopyBot(KakaoYouTubeBot):
    """콘솔에 요약을 출력하는 수동 복사용 봇"""
    
    def send_response(self, room_name: str, message: str, max_retries: int = 3):
        """응답 메시지를 콘솔에 출력하고 클립보드에 복사"""
        print("\n" + "="*80)
        print(f"🎯 [{room_name}] 채팅방에 전송할 메시지:")
        print("="*80)
        print(message)
        print("="*80)
        
        # 클립보드에 자동 복사
        try:
            pyperclip.copy(message)
            print("📋 메시지가 클립보드에 복사되었습니다!")
            print("💡 카카오톡에서 Ctrl+V로 붙여넣기하세요!")
        except Exception as e:
            print(f"⚠️ 클립보드 복사 실패: {e}")
        
        print("\n🔔 알림: 위 메시지를 카카오톡에 수동으로 전송해주세요!")
        print("⏰ 10초 후 다음 메시지 모니터링을 계속합니다...\n")
        
        # 봇이 보낸 메시지로 기록 (중복 방지)
        self.processed_messages.add(message)
        
        # 잠시 대기
        import time
        time.sleep(10)
        
        return True  # 항상 성공으로 처리

def manual_start():
    """수동 복사용 봇 시작"""
    print("🚀 YouTube 봇 시작 (수동 복사 방식)")
    print("=" * 50)
    print("💡 이 봇은 요약을 콘솔에 출력하고 클립보드에 복사합니다.")
    print("📋 사용자가 직접 카카오톡에 붙여넣기해야 합니다.")
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
    
    # 수동 복사용 봇 생성
    try:
        bot = ManualCopyBot(apify_token=apify_token, gemini_key=gemini_key)
        print("✅ 수동 복사용 봇 생성 완료")
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
    print("\n🤖 수동 복사용 봇을 시작합니다...")
    bot.start()
    
    if not bot.is_running:
        print("❌ 봇 시작 실패!")
        return False
    
    print("✅ 수동 복사용 봇이 성공적으로 시작되었습니다!")
    print(f"🔄 모니터링 중: {list(bot.monitored_rooms)}")
    print("\n💡 작동 방식:")
    print("   1. YouTube URL을 채팅방에 보내세요")
    print("   2. 봇이 요약을 생성하고 콘솔에 출력합니다")
    print("   3. 요약이 자동으로 클립보드에 복사됩니다")
    print("   4. 카카오톡에서 Ctrl+V로 붙여넣기하세요")
    print("\n📋 명령어:")
    print("   - 'status': 봇 상태 확인")
    print("   - 'last': 마지막 요약 다시 보기")
    print("   - 'quit': 봇 종료")
    
    # 마지막 요약 저장용
    bot.last_summary = ""
    
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
            elif command == 'last':
                if hasattr(bot, 'last_summary') and bot.last_summary:
                    print("\n" + "="*80)
                    print("📄 마지막 생성된 요약:")
                    print("="*80)
                    print(bot.last_summary)
                    print("="*80)
                    try:
                        pyperclip.copy(bot.last_summary)
                        print("📋 클립보드에 다시 복사했습니다!")
                    except:
                        pass
                else:
                    print("❌ 아직 생성된 요약이 없습니다.")
            elif command == '':
                continue
            else:
                print("❓ 사용 가능한 명령어: status, last, quit")
                
    except KeyboardInterrupt:
        print("\n\n🛑 Ctrl+C로 중단됨")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
    finally:
        bot.stop()
        print("👋 수동 복사용 봇이 종료되었습니다.")
    
    return True

if __name__ == "__main__":
    try:
        success = manual_start()
        if not success:
            print("\n💥 봇 실행 실패!")
    except Exception as e:
        print(f"💥 치명적 오류: {e}")
        import traceback
        traceback.print_exc() 