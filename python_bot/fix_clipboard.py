#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
클립보드 문제 진단 및 해결
"""

import pyperclip
import time
import os
import subprocess

def test_clipboard():
    """클립보드 테스트"""
    print("🔍 클립보드 상태 진단")
    print("=" * 40)
    
    # 1. 기본 클립보드 테스트
    try:
        print("📋 클립보드 기본 테스트...")
        test_text = "클립보드 테스트"
        pyperclip.copy(test_text)
        result = pyperclip.paste()
        
        if result == test_text:
            print("✅ 클립보드 기본 기능 정상")
        else:
            print("❌ 클립보드 기본 기능 실패")
            return False
            
    except Exception as e:
        print(f"❌ 클립보드 오류: {e}")
        return False
    
    # 2. 연속 클립보드 테스트
    print("\n🔄 연속 클립보드 접근 테스트...")
    try:
        for i in range(5):
            test_msg = f"테스트 메시지 {i+1}"
            pyperclip.copy(test_msg)
            time.sleep(0.1)
            result = pyperclip.paste()
            
            if result != test_msg:
                print(f"❌ {i+1}번째 테스트 실패")
                return False
            else:
                print(f"✅ {i+1}번째 테스트 통과")
                
    except Exception as e:
        print(f"❌ 연속 클립보드 테스트 실패: {e}")
        return False
    
    print("✅ 모든 클립보드 테스트 통과!")
    return True

def kill_clipboard_programs():
    """클립보드 관련 프로그램 종료"""
    print("\n🛑 클립보드 관련 프로그램 정리...")
    
    clipboard_programs = [
        'clipdiary.exe',
        'ditto.exe', 
        'clipmate.exe',
        'clipx.exe',
        'clcl.exe'
    ]
    
    killed_any = False
    for program in clipboard_programs:
        try:
            # taskkill 명령어로 프로그램 종료
            result = subprocess.run(
                ['taskkill', '/f', '/im', program], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                print(f"✅ {program} 종료됨")
                killed_any = True
        except:
            pass
    
    if not killed_any:
        print("ℹ️  특별히 종료할 클립보드 프로그램이 없습니다.")

def fix_clipboard_issue():
    """클립보드 문제 해결 시도"""
    print("🔧 클립보드 문제 해결 시도")
    print("=" * 40)
    
    # 1. 클립보드 프로그램 정리
    kill_clipboard_programs()
    
    # 2. 클립보드 초기화
    print("\n🔄 클립보드 초기화...")
    try:
        pyperclip.copy("")
        time.sleep(0.5)
        pyperclip.copy("초기화 완료")
        print("✅ 클립보드 초기화 완료")
    except Exception as e:
        print(f"❌ 클립보드 초기화 실패: {e}")
        return False
    
    # 3. 클립보드 테스트
    print("\n🧪 클립보드 테스트...")
    if test_clipboard():
        print("\n✅ 클립보드 문제 해결됨!")
        return True
    else:
        print("\n❌ 클립보드 문제 지속됨")
        return False

def show_alternative_solutions():
    """대안 해결책 제시"""
    print("\n🛠️  대안 해결책:")
    print("=" * 40)
    print("1. 📱 PyAutoGUI 직접 타이핑 사용")
    print("2. 🔄 카카오톡 재시작 후 재시도")
    print("3. 💻 컴퓨터 재부팅 후 재시도")
    print("4. 🛡️  Windows Defender 예외 추가")
    print("5. 📋 클립보드 매니저 프로그램 제거")

if __name__ == "__main__":
    print("🩺 클립보드 문제 진단 및 해결 도구")
    print("=" * 50)
    
    # 기본 테스트 먼저
    if test_clipboard():
        print("\n🎉 클립보드가 정상 작동 중입니다!")
        print("💡 pyautokakao 문제일 수 있습니다. 대안 방법을 사용하세요.")
    else:
        print("\n⚠️  클립보드 문제가 감지되었습니다.")
        
        # 문제 해결 시도
        if fix_clipboard_issue():
            print("\n🎉 문제가 해결되었습니다! 봇을 다시 시작하세요.")
        else:
            print("\n💔 자동 해결 실패. 대안 방법을 사용하세요.")
            show_alternative_solutions()
    
    print("\n📝 추천 다음 단계:")
    print("   1. python test_alternative_send.py (대안 전송 테스트)")
    print("   2. python simple_start.py (봇 재시작)") 