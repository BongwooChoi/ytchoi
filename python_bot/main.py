#!/usr/bin/env python3
"""
카카오톡 YouTube 봇 - Python 버전
pyautokakao를 사용한 자동 응답 봇
"""

import sys
import os
import signal
import time
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config import Config
from kakao_bot import KakaoYouTubeBot

def signal_handler(signum, frame):
    """시그널 핸들러 (Ctrl+C 처리)"""
    print("\n프로그램을 종료합니다...")
    if 'bot' in globals():
        bot.stop()
    sys.exit(0)

def print_banner():
    """시작 배너 출력"""
    banner = """
    ╔══════════════════════════════════════╗
    ║       카카오톡 YouTube 봇 v2.0       ║
    ║            Python 버전               ║
    ╚══════════════════════════════════════╝
    
    📺 YouTube URL 자동 감지 및 요약
    🤖 Gemini AI 기반 스마트 요약
    💬 카카오톡 자동 응답
    
    """
    print(banner)

def get_user_rooms():
    """사용자로부터 모니터링할 채팅방 목록 입력받기"""
    print("🏠 모니터링할 카카오톡 채팅방을 입력하세요.")
    print("   (여러 개일 경우 쉼표로 구분하세요)")
    print("   예: 친구들,가족,업무방")
    
    while True:
        rooms_input = input("\n채팅방 이름: ").strip()
        
        if not rooms_input:
            print("❌ 최소 하나의 채팅방 이름을 입력해야 합니다.")
            continue
        
        # 쉼표로 분리하고 공백 제거
        rooms = [room.strip() for room in rooms_input.split(',') if room.strip()]
        
        if rooms:
            return rooms
        else:
            print("❌ 유효한 채팅방 이름을 입력해주세요.")

def print_usage_instructions():
    """사용법 안내 출력"""
    instructions = """
    📋 사용법 안내:
    
    1. 카카오톡 PC 버전이 실행되어 있어야 합니다
    2. 모니터링할 채팅방 이름을 정확히 입력하세요
    3. 봇이 시작되면 채팅방에 YouTube URL을 보내보세요
    4. 봇이 자동으로 동영상을 분석하고 요약을 제공합니다
    
    ⚠️  주의사항:
    - Windows에서만 작동합니다
    - 채팅방 이름은 대소문자를 정확히 맞춰주세요
    - 컴퓨터가 켜져있어야 합니다
    
    🎮 실행 중 명령어:
    - 'status': 봇 상태 확인
    - 'add <채팅방>': 채팅방 추가
    - 'remove <채팅방>': 채팅방 제거
    - 'quit': 봇 종료
    """
    print(instructions)

def main():
    """메인 함수"""
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    
    # 배너 출력
    print_banner()
    
    try:
        # 설정 유효성 검사
        print("🔧 설정을 확인하는 중...")
        Config.validate()
        print("✅ 설정 확인 완료!")
        
        # 설정 정보 출력
        config_info = Config.get_info()
        print(f"📊 설정 정보:")
        print(f"   - 메시지 확인 주기: {config_info['check_interval']}초")
        print(f"   - 최대 자막 길이: {config_info['max_transcript_length']}자")
        print(f"   - Gemini 모델: {config_info['gemini_model']}")
        print(f"   - Apify 토큰: {'✅' if config_info['has_apify_token'] else '❌'}")
        print(f"   - Gemini 키: {'✅' if config_info['has_gemini_key'] else '❌'}")
        
    except ValueError as e:
        print(f"❌ 설정 오류: {e}")
        print("\n.env 파일을 확인하거나 환경변수를 설정해주세요.")
        return 1
    
    try:
        # 봇 생성
        print("\n🤖 봇을 초기화하는 중...")
        bot = KakaoYouTubeBot(
            apify_token=Config.APIFY_API_TOKEN,
            gemini_key=Config.GEMINI_API_KEY
        )
        bot.check_interval = Config.CHECK_INTERVAL
        bot.max_transcript_length = Config.MAX_TRANSCRIPT_LENGTH
        
        # 채팅방 설정
        rooms = get_user_rooms()
        for room in rooms:
            bot.add_room(room)
        
        print(f"\n✅ {len(rooms)}개 채팅방 모니터링 설정 완료!")
        
        # 사용법 안내
        print_usage_instructions()
        
        # 봇 시작
        print("🚀 봇을 시작합니다...\n")
        bot.start()
        
        print("✨ 봇이 성공적으로 시작되었습니다!")
        print("💡 YouTube URL을 채팅방에 보내서 테스트해보세요.")
        print("🔄 실시간 모니터링 중... (Ctrl+C로 종료)\n")
        
        # 메인 루프
        while True:
            try:
                command = input("📝 명령어 입력 (help: 도움말): ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    break
                elif command == 'status':
                    status = bot.get_status()
                    print(f"🤖 봇 상태:")
                    print(f"   - 실행 중: {'✅' if status['is_running'] else '❌'}")
                    print(f"   - 모니터링 채팅방: {status['monitored_rooms']}")
                    print(f"   - 처리된 메시지 수: {status['processed_messages_count']}")
                elif command.startswith('add '):
                    room_name = command[4:].strip()
                    if room_name:
                        bot.add_room(room_name)
                    else:
                        print("❌ 채팅방 이름을 입력해주세요.")
                elif command.startswith('remove '):
                    room_name = command[7:].strip()
                    if room_name:
                        bot.remove_room(room_name)
                    else:
                        print("❌ 채팅방 이름을 입력해주세요.")
                elif command == 'help':
                    print("""
📖 사용 가능한 명령어:
   - status: 봇 상태 확인
   - add <채팅방이름>: 모니터링 채팅방 추가
   - remove <채팅방이름>: 모니터링 채팅방 제거
   - quit/exit: 봇 종료
   - help: 이 도움말 표시
                    """)
                elif command == '':
                    continue
                else:
                    print("❓ 알 수 없는 명령어입니다. 'help'를 입력해서 도움말을 확인하세요.")
                    
            except EOFError:
                break
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        print("자세한 내용은 로그를 확인해주세요.")
        return 1
    
    finally:
        if 'bot' in locals():
            bot.stop()
        print("\n👋 봇이 종료되었습니다. 안녕히 가세요!")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 