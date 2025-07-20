#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pyautokakao 메시지 전송 테스트 스크립트
"""

import pyautokakao
import time

def test_message_sending():
    """메시지 전송 테스트"""
    print("📤 pyautokakao 메시지 전송 테스트")
    print("=" * 50)
    
    # 채팅방 이름 입력
    room_name = input("테스트할 채팅방 이름을 입력하세요: ").strip()
    
    if not room_name:
        print("❌ 채팅방 이름이 입력되지 않았습니다.")
        return
    
    # 테스트 메시지들
    test_messages = [
        "🔧 테스트 메시지 1 - 기본 전송",
        "🔧 테스트 메시지 2 - 한글 전송",
        "🔧 Test message 3 - English",
        "🔧 테스트 완료!"
    ]
    
    print(f"\n📤 '{room_name}' 채팅방에 테스트 메시지 전송...")
    print("⚠️ 카카오톡을 확인하여 메시지가 실제로 전송되는지 확인하세요!")
    print()
    
    for i, message in enumerate(test_messages, 1):
        try:
            print(f"📤 메시지 {i}/{len(test_messages)} 전송 중: {message}")
            
            # pyautokakao로 메시지 전송
            pyautokakao.send(room_name, message)
            print(f"✅ pyautokakao.send() 함수 실행 완료")
            
            # 사용자에게 확인 요청
            user_check = input("   💬 카카오톡에 메시지가 나타났나요? (y/n): ").strip().lower()
            
            if user_check == 'y':
                print(f"   ✅ 메시지 {i} 전송 성공 확인됨!")
            else:
                print(f"   ❌ 메시지 {i} 전송 실패 - 카카오톡에 나타나지 않음")
                
                # 문제 해결 시도
                print("   🔧 문제 해결 시도...")
                print("   1. 카카오톡 창을 직접 클릭해서 활성화")
                print("   2. 해당 채팅방을 열어보세요")
                input("   ⏳ 준비되면 Enter를 누르세요...")
                
                # 재시도
                print(f"   🔄 메시지 {i} 재전송 시도...")
                pyautokakao.send(room_name, f"{message} (재전송)")
                
                user_retry = input("   💬 이번에는 메시지가 나타났나요? (y/n): ").strip().lower()
                if user_retry == 'y':
                    print(f"   ✅ 메시지 {i} 재전송 성공!")
                else:
                    print(f"   ❌ 메시지 {i} 재전송도 실패")
            
            print()
            time.sleep(2)  # 메시지 간 간격
            
        except Exception as e:
            print(f"   ❌ 메시지 전송 중 오류: {e}")
            print()
    
    print("🎉 메시지 전송 테스트 완료!")
    print()
    print("📋 결과 분석:")
    print("- 모든 메시지가 성공: pyautokakao가 정상 작동")
    print("- 일부 메시지만 성공: 타이밍이나 활성화 문제")
    print("- 모든 메시지가 실패: pyautokakao 호환성 문제")

if __name__ == "__main__":
    test_message_sending() 