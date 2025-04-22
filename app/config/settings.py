from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API 설정
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "SaeDoRi Crawling"
    
    # Gin 서버 설정
    GIN_SERVER_URL: str = "http://localhost:8080"  # Gin 서버 URL
    
    # 크롤링 설정
    CRAWLING_TIMEOUT: int = 30  # 크롤링 타임아웃 (초)
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
      # 크롤링할 때 봇처럼 보이지 않게 하는 설정

    class Config:
        case_sensitive = True # 대소문자 구분

settings = Settings()
