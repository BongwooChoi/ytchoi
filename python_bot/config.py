import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

class Config:
    """봇 설정 클래스"""
    
    # API Keys
    APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Bot Settings
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '2'))
    MAX_TRANSCRIPT_LENGTH = int(os.getenv('MAX_TRANSCRIPT_LENGTH', '10000'))
    
    # Gemini Settings
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # Apify Settings
    APIFY_ACTOR_ID = os.getenv('APIFY_ACTOR_ID', 'dB9f4B02ocpTICIEY')
    
    @classmethod
    def validate(cls):
        """설정 유효성 검사"""
        missing_keys = []
        
        if not cls.APIFY_API_TOKEN:
            missing_keys.append('APIFY_API_TOKEN')
        
        if not cls.GEMINI_API_KEY:
            missing_keys.append('GEMINI_API_KEY')
        
        if missing_keys:
            raise ValueError(f"다음 환경변수가 필요합니다: {', '.join(missing_keys)}")
        
        return True
    
    @classmethod
    def get_info(cls):
        """설정 정보 출력"""
        return {
            'check_interval': cls.CHECK_INTERVAL,
            'max_transcript_length': cls.MAX_TRANSCRIPT_LENGTH,
            'gemini_model': cls.GEMINI_MODEL,
            'apify_actor_id': cls.APIFY_ACTOR_ID,
            'has_apify_token': bool(cls.APIFY_API_TOKEN),
            'has_gemini_key': bool(cls.GEMINI_API_KEY)
        }

# 설정 인스턴스
config = Config() 