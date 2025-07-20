#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyAutoGUI + 클립보드를 이용한 카카오톡 메시지 전송 대안
"""

import pyautogui
import pyperclip
import time
import subprocess
import psutil

def find_kakao_window():
    """카카오톡 창 찾기"""
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if 'KakaoTalk' in proc.info['name']:
                return True
        return False
    except:
        return False

def send_message_alternative(room_name: str, message: str) -> bool:
    """PyAutoGUI를 이용한 메시지 전송"""
    try:
        print(f"🔧 대안 방법으로 메시지 전송 시도 ({room_name}): {message[:30]}...")
        
        # 1. 카카오톡 프로세스 확인
        if not find_kakao_window():
            print("❌ 카카오톡이 실행되지 않았습니다.")
            return False
        
        # 2. 카카오톡 창 활성화
        print("🪟 카카오톡 창 활성화 중...")
        
        # Windows에서 카카오톡 활성화
        try:
            subprocess.run(['powershell', '-Command', 
                          '(New-Object -ComObject WScript.Shell).AppActivate("KakaoTalk")'], 
                          capture_output=True, timeout=3)
            time.sleep(1.5)
        except:
            print("⚠️ 카카오톡 창 활성화 실패, 계속 진행...")
        
        # 3. 채팅방 검색 및 이동
        print(f"🔍 '{room_name}' 채팅방 검색 중...")
        
        # Ctrl+F로 검색창 열기
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)
        
        # 채팅방 이름 입력
        pyautogui.write(room_name)
        time.sleep(0.5)
        
        # Enter로 검색 실행
        pyautogui.press('enter')
        time.sleep(1)
        
        # ESC로 검색창 닫기
        pyautogui.press('escape')
        time.sleep(0.5)
        
        # 4. 메시지 입력창 클릭 (카카오톡 하단 입력창 위치)
        print("🎯 메시지 입력창 클릭...")
        
        # 화면 크기 가져오기
        screen_width, screen_height = pyautogui.size()
        
        # 카카오톡 입력창 예상 위치 (하단 중앙)
        click_x = screen_width // 2
        click_y = screen_height - 100  # 하단에서 100픽셀 위
        
        pyautogui.click(click_x, click_y)
        time.sleep(1)
        
        # 5. 기존 텍스트 전체 선택 후 삭제
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.press('delete')
        time.sleep(0.3)
        
        # 6. 메시지 길이 확인 및 제한
        max_length = 500  # 안전한 길이로 제한
        if len(message) > max_length:
            message = message[:max_length] + "..."
            print(f"⚠️ 메시지가 너무 길어서 {max_length}자로 제한됨")
        
        # 7. 직접 타이핑 (클립보드 대신)
        print("⌨️ 메시지 직접 타이핑...")
        
        # 메시지를 작은 단위로 나누어 타이핑
        chunk_size = 50
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i+chunk_size]
            pyautogui.write(chunk, interval=0.01)  # 빠른 타이핑
            time.sleep(0.1)
        
        time.sleep(0.5)
        
        # 8. Enter로 전송
        print("📤 메시지 전송...")
        pyautogui.press('enter')
        time.sleep(1)
        
        print("✅ 대안 방법으로 메시지 전송 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 대안 전송 실패: {e}")
        return False

def test_alternative_send():
    """대안 전송 방법 테스트"""
    print("🧪 대안 메시지 전송 테스트")
    print("=" * 40)
    
    print("⚠️ 중요: 카카오톡을 열고 채팅방을 활성화한 상태에서 테스트하세요!")
    print("📋 순서:")
    print("1. 카카오톡 PC 버전 실행")
    print("2. 테스트할 채팅방 열기")
    print("3. 이 스크립트 실행")
    print()
    
    input("⏳ 준비되면 Enter를 누르세요...")
    
    test_messages = [
        "🔧 대안 전송 테스트 1",
        "🔧 대안 전송 테스트 2 - 한글",
        "🔧 Alternative test 3 - English"
    ]
    
    success_count = 0
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📤 테스트 {i}/{len(test_messages)}: {message}")
        
        if send_message_alternative(message):
            user_check = input(f"💬 카카오톡에 메시지가 나타났나요? (y/n): ").strip().lower()
            if user_check == 'y':
                print(f"✅ 테스트 {i} 성공!")
                success_count += 1
            else:
                print(f"❌ 테스트 {i} 실패")
        else:
            print(f"❌ 테스트 {i} 전송 오류")
        
        time.sleep(2)
    
    print(f"\n📊 테스트 결과: {success_count}/{len(test_messages)} 성공")
    
    if success_count > 0:
        print("🎉 대안 방법이 작동합니다!")
        print("💡 이 방법을 봇에 적용할 수 있습니다.")
    else:
        print("😞 대안 방법도 실패했습니다.")
        print("💡 추가 해결 방법이 필요합니다.")

if __name__ == "__main__":
    test_alternative_send() 