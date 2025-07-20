import re
from urllib.parse import urlparse, parse_qs

class YouTubeDetector:
    """YouTube URL 감지 및 비디오 ID 추출 클래스"""
    
    def __init__(self):
        # YouTube URL 패턴들
        self.youtube_patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([\w-]+)',
            r'youtube\.com\/watch\?.*v=([\w-]+)',
            r'youtu\.be\/([\w-]+)',
            r'youtube\.com\/embed\/([\w-]+)',
            r'youtube\.com\/v\/([\w-]+)'
        ]
    
    def detect_youtube_url(self, text):
        """텍스트에서 YouTube URL 감지"""
        for pattern in self.youtube_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def extract_video_id(self, url):
        """YouTube URL에서 비디오 ID 추출"""
        for pattern in self.youtube_patterns:
            match = re.search(pattern, url, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def is_youtube_url(self, text):
        """YouTube URL인지 확인"""
        return self.detect_youtube_url(text) is not None
    
    def get_video_title_url(self, video_id):
        """비디오 ID로 YouTube URL 생성"""
        return f"https://www.youtube.com/watch?v={video_id}"

# 사용 예제
if __name__ == "__main__":
    detector = YouTubeDetector()
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "Check this out: https://www.youtube.com/watch?v=dQw4w9WgXcQ awesome video!"
    ]
    
    for url in test_urls:
        if detector.is_youtube_url(url):
            video_id = detector.extract_video_id(url)
            print(f"Found YouTube URL: {url}")
            print(f"Video ID: {video_id}")
            print(f"Clean URL: {detector.get_video_title_url(video_id)}")
            print("---") 