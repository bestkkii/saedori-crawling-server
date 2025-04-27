# 크롤링 수행
# 데이터를 json 형식으로 변환
# Gin에 데이터 전달

from typing import Dict, List, Any
from ..crawlers import get_crawler, list_crawlers
from datetime import datetime
import logging
import os
import codecs
from ..utils import send_slack_alert

# 로그 디렉토리 생성
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 로그 파일 경로
log_file = os.path.join(log_dir, 'crawler.log')

# 로그 파일 초기화
def init_log_file():
    """로그 파일을 초기화하고 기본 정보를 기록합니다."""
    with codecs.open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"=== 크롤링 로그 시작 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # 콘솔에도 출력
    ]
)

# 로거 생성
logger = logging.getLogger(__name__)

class DataService:
    def __init__(self):
        """
        DataService 초기화
        크롤러들을 등록하고 초기화합니다.
        """
        # 로그 파일 초기화
        init_log_file()
        logger.info("DataService 초기화 시작")
        
        # 크롤러 등록 확인
        self.crawlers = {
            "music": get_crawler("music"),
            "news_naver": get_crawler("news_naver"),
            "realtime_search_words_google": get_crawler("realtime_search_words_google")
        }
        
        # 등록된 크롤러 확인
        registered_crawlers = list_crawlers()
        logger.info(f"등록된 크롤러: {registered_crawlers}")
        
        # 크롤러가 없는 경우 예외 발생
        if not self.crawlers:
            logger.error("등록된 크롤러가 없습니다.")
            raise ValueError("등록된 크롤러가 없습니다.")

        # 각 크롤러 초기화
        self.crawler_instances = {
            name: crawler_class() 
            for name, crawler_class in self.crawlers.items()
        }
        
        # 타임아웃 설정
        self.timeout = 300  # 5분 타임아웃
        logger.info("DataService 초기화 완료")

    def _run_crawler(self, name: str, crawler) -> Dict[str, Any]:
        """
        개별 크롤러를 실행하는 함수
        
        Args:
            name: 크롤러 이름
            crawler: 크롤러 인스턴스
            
        Returns:
            Dict[str, Any]: 크롤링 결과
        """
        logger.info(f"크롤러 '{name}' 실행 시작")
        
        try:
            result = crawler.crawl()
            logger.info(f"크롤러 '{name}' 실행 성공")
            return {
                "crawling": "Success",
                "result": result
            }
        except Exception as e:
            logger.error(f"크롤러 '{name}' 실행 실패: {str(e)}")
            return {
                "crawling": "Failed",
                "result": {"error": str(e)}
            }

    def crawl_all(self) -> Dict[str, Any]:
        """
        모든 크롤러를 순차적으로 실행하고 결과를 반환
        """
        results = {
            "message": "Success",
            "created_at": int(datetime.now().timestamp()),
            "music_crawl": None,
            "news_crawl": None,
            "realtime_search_words_crawl": None
        }

        # 크롤러 이름과 결과 키 매핑
        crawler_key_mapping = {
            "music": "music_crawl",
            "news_naver": "news_crawl",
            "realtime_search_words_google": "realtime_search_words_crawl"
        }

        # 각 크롤러를 순차적으로 실행
        for name, crawler in self.crawler_instances.items():
            try:
                # 크롤러 실행
                result = self._run_crawler(name, crawler)
                
                # 결과 저장
                results[crawler_key_mapping[name]] = result
                
                # 에러가 있는 경우 로깅
                if result["crawling"] == "Failed":
                    logger.error(f"크롤러 '{name}' 실패: {result['result'].get('error', 'Unknown error')}")
                
            except Exception as e:
                # 예외 처리
                logger.error(f"크롤러 '{name}' 실행 중 예외 발생: {str(e)}")
                results[crawler_key_mapping[name]] = {
                    "crawling": "Failed",
                    "result": {"error": str(e)}
                }
                send_slack_alert(f"크롤러 '{name}' 실패: {str(e)}")

        return results

# 싱글톤 인스턴스 생성
data_service = DataService()
