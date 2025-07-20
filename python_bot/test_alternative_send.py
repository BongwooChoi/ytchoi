#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
대안 메시지 전송 방법 테스트
"""

from alternative_send import send_message_alternative
import time

def test_alternative_send():
    """대안 전송 방법 테스트"""
    print("🧪 대안 메시지 전송 테스트")
    print("=" * 40)
    
    # 채팅방 이름 입력
    room_name = input("테스트할 채팅방 이름: ").strip()
    if not room_name:
        print("❌ 채팅방 이름이 필요합니다.")
        return
    
    # 테스트 메시지
    test_message = "🤖 대안 전송 방법 테스트 메시지입니다!"
    
    print(f"\n📱 '{room_name}' 채팅방에 메시지를 전송합니다...")
    print(f"💬 메시지: {test_message}")
    print("\n⚠️  주의: 10초 후 자동으로 전송됩니다!")
    print("   카카오톡 창을 미리 열어놓으세요.")
    
    # 카운트다운
    for i in range(10, 0, -1):
        print(f"⏰ {i}초 남음...")
        time.sleep(1)
    
    # 메시지 전송 시도
    print("\n🚀 메시지 전송 중...")
    success = send_message_alternative(room_name, test_message)
    
    if success:
        print("✅ 메시지 전송 성공!")
        print("📱 카카오톡에서 메시지가 전송되었는지 확인하세요.")
    else:
        print("❌ 메시지 전송 실패!")
        print("💡 문제 해결 방법:")
        print("   1. 카카오톡이 실행되어 있는지 확인")
        print("   2. 채팅방 이름이 정확한지 확인")
        print("   3. 카카오톡 창이 다른 창에 가려져 있지 않은지 확인")

if __name__ == "__main__":
    test_alternative_send() 