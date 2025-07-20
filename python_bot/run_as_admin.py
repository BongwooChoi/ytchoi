#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
관리자 권한으로 봇 실행
"""

import sys
import os
import ctypes

def is_admin():
    """관리자 권한 확인"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """관리자 권한으로 실행"""
    if is_admin():
        print("✅ 이미 관리자 권한으로 실행 중입니다.")
        return True
    else:
        print("🔐 관리자 권한이 필요합니다. 권한 상승을 시도합니다...")
        # 관리자 권한으로 재실행
        ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(['"' + arg + '"' for arg in sys.argv]), 
            None, 
            1
        )
        return False

if __name__ == "__main__":
    print("🚀 관리자 권한 봇 실행기")
    print("=" * 40)
    
    if run_as_admin():
        # 관리자 권한으로 실행 중이면 실제 봇 실행
        try:
            print("🤖 봇을 관리자 권한으로 실행합니다...")
            exec(open('quick_start.py', 'r', encoding='utf-8').read())
        except FileNotFoundError:
            print("❌ quick_start.py 파일을 찾을 수 없습니다.")
            print("💡 python_bot 폴더에서 실행하세요.")
        except Exception as e:
            print(f"❌ 봇 실행 오류: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("👋 관리자 권한 상승 대화상자를 확인하세요.") 