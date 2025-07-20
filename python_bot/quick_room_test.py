#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyautokakao

def test_room_names():
    """다양한 채팅방 이름으로 테스트"""
    print("🔍 채팅방 이름 테스트")
    print("=" * 30)
    
    # 가능한 채팅방 이름들
    possible_names = [
        "나와의 채팅",
        "나와의채팅", 
        "나",
        "최봉우",
        "Me",
        "나의 채팅"
    ]
    
    print("📋 테스트할 채팅방 이름들:")
    for i, name in enumerate(possible_names, 1):
        print(f"  {i}. '{name}'")
    
    print("\n🔍 각 이름으로 메시지 읽기 테스트...")
    
    for name in possible_names:
        try:
            print(f"\n📖 '{name}' 테스트 중...")
            messages = pyautokakao.read(name)
            
            if messages:
                print(f"✅ '{name}' - 메시지 읽기 성공!")
                print(f"   데이터 타입: {type(messages)}")
                if isinstance(messages, str):
                    print(f"   메시지 길이: {len(messages)} 문자")
                elif isinstance(messages, list):
                    print(f"   메시지 개수: {len(messages)} 개")
                
                # 간단한 테스트 메시지 전송
                test_msg = "🔧 채팅방 이름 테스트"
                print(f"   📤 테스트 메시지 전송 시도...")
                pyautokakao.send(name, test_msg)
                print(f"   ✅ 전송 함수 실행 완료")
                
                user_input = input(f"   💬 '{name}' 채팅방에 메시지가 나타났나요? (y/n): ").strip().lower()
                if user_input == 'y':
                    print(f"   🎉 정답! 올바른 채팅방 이름: '{name}'")
                    return name
                else:
                    print(f"   ❌ '{name}'은 올바른 이름이 아님")
            else:
                print(f"❌ '{name}' - 메시지 읽기 실패 (채팅방 없음)")
                
        except Exception as e:
            print(f"❌ '{name}' - 오류: {e}")
    
    print("\n⚠️ 모든 이름 테스트 실패!")
    print("💡 다음을 확인해보세요:")
    print("  1. 카카오톡 PC 버전이 실행되어 있는지")
    print("  2. 채팅방 목록에서 정확한 이름 확인")
    print("  3. 최근에 대화한 채팅방인지")
    
    return None

if __name__ == "__main__":
    correct_name = test_room_names()
    if correct_name:
        print(f"\n🎯 결론: 올바른 채팅방 이름은 '{correct_name}' 입니다!")
        print(f"💡 봇 설정에서 채팅방 이름을 '{correct_name}'로 변경하세요.") 