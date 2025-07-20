#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
카카오톡 연결 상태 디버그 스크립트
"""

import pyautokakao
import time

def test_kakao_connection():
    """카카오톡 연결 테스트"""
    print("🔍 카카오톡 연결 상태 테스트")
    print("=" * 50)
    
    # 1. pyautokakao 라이브러리 테스트
    try:
        print("📚 pyautokakao 라이브러리 로드 테스트...")
        import pyautokakao
        print("✅ pyautokakao 라이브러리 정상 로드")
    except ImportError as e:
        print(f"❌ pyautokakao 라이브러리 로드 실패: {e}")
        return False
    
    # 2. 카카오톡 프로세스 확인
    try:
        print("\n🔍 카카오톡 프로세스 확인...")
        import psutil
        kakao_found = False
        for proc in psutil.process_iter(['pid', 'name']):
            if 'KakaoTalk' in proc.info['name']:
                print(f"✅ 카카오톡 프로세스 발견: PID {proc.info['pid']}")
                kakao_found = True
                break
        
        if not kakao_found:
            print("❌ 카카오톡 프로세스를 찾을 수 없습니다!")
            print("💡 카카오톡 PC 버전을 실행해주세요.")
            return False
            
    except ImportError:
        print("⚠️ psutil 없음. 프로세스 확인 건너뜀.")
    except Exception as e:
        print(f"⚠️ 프로세스 확인 오류: {e}")
    
    # 3. 카카오톡 기본 연결 테스트 (activate 함수 없으므로 스킵)
    print("\n🪟 카카오톡 연결 테스트...")
    print("✅ pyautokakao 기본 테스트 (창 활성화 스킵)")
    time.sleep(1)
    
    # 4. 채팅방 목록 테스트 (사용자 입력)
    print("\n💬 채팅방 연결 테스트")
    room_name = input("테스트할 채팅방 이름을 입력하세요: ").strip()
    
    if not room_name:
        print("⚠️ 채팅방 이름이 입력되지 않았습니다.")
        return True
    
    try:
        print(f"📖 '{room_name}' 채팅방 메시지 읽기 테스트...")
        messages = pyautokakao.read(room_name)
        
        print(f"📥 메시지 읽기 결과:")
        print(f"   타입: {type(messages)}")
        print(f"   내용: {repr(messages)[:200]}...")
        
        if messages:
            print("✅ 메시지 읽기 성공!")
            
            # 메시지 파싱 테스트
            if isinstance(messages, str):
                message_list = [msg.strip() for msg in messages.split('\n') if msg.strip()]
                print(f"📋 파싱된 메시지 개수: {len(message_list)}")
                if message_list:
                    print(f"📨 최근 메시지 예시: {message_list[-1][:50]}...")
            elif isinstance(messages, list):
                print(f"📋 메시지 리스트 길이: {len(messages)}")
                if messages:
                    print(f"📨 최근 메시지 예시: {messages[-1][:50]}...")
        else:
            print("📭 메시지가 없거나 채팅방을 찾을 수 없습니다.")
            print("💡 확인사항:")
            print("   - 채팅방 이름이 정확한지 확인")
            print("   - 최근에 대화한 채팅방인지 확인")
            print("   - 카카오톡 메인 화면이 열려있는지 확인")
        
    except Exception as e:
        print(f"❌ 채팅방 메시지 읽기 실패: {e}")
        import traceback
        print(f"🔍 상세 오류: {traceback.format_exc()}")
        return False
    
    print("\n🎉 카카오톡 연결 테스트 완료!")
    return True

if __name__ == "__main__":
    test_kakao_connection() 