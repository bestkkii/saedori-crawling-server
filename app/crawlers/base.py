from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..config.settings import settings
from typing import Dict, Any

class BaseCrawler(ABC):
    def __init__(self):
        self.headers = {
            "User-Agent": settings.USER_AGENT
        }
        self.timeout = settings.CRAWLING_TIMEOUT

    def _setup_chrome_options(self) -> Options:
        """
        Chrome 옵션 설정
        """
        chrome_options = Options()
        
        # 메모리 최적화 설정
        chrome_options.add_argument("--headless=new")  # 메모리 최적화된 headless 모드 (Chrome 109+)
        chrome_options.add_argument("--disable-gpu")  # GPU 렌더링 비활성화
        chrome_options.add_argument("--no-sandbox")  # 보안 샌드박스 제거
        chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 안 함
        # chrome_options.add_argument("--single-process")  # 하나의 프로세스로 실행
        chrome_options.add_argument("--disable-extensions")  # 확장기능 비활성화
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--mute-audio")  # 음소거
        chrome_options.add_argument("--remote-debugging-port=9222")  # headless 안정화
        
        # SwiftShader 관련 경고 해결
        chrome_options.add_argument("--enable-unsafe-swiftshader")  # SwiftShader 경고 해결
        
        # 추가 메모리 최적화 설정
        # chrome_options.add_argument("--disable-javascript")  # JavaScript 비활성화 (필요한 경우 주석 처리)
        chrome_options.add_argument("--disable-images")  # 이미지 로딩 비활성화
        chrome_options.add_argument("--disable-plugins")  # 플러그인 비활성화
        chrome_options.add_argument("--disable-popup-blocking")  # 팝업 차단 비활성화
        chrome_options.add_argument("--disable-notifications")  # 알림 비활성화
        chrome_options.add_argument("--disable-web-security")  # 웹 보안 비활성화 (필요한 경우 주석 처리)
        chrome_options.add_argument("--disable-features=site-per-process")  # 사이트 격리 비활성화
        chrome_options.add_argument("--disable-features=IsolateOrigins")  # 출처 격리 비활성화
        chrome_options.add_argument("--disable-features=NetworkService")  # 네트워크 서비스 비활성화
        chrome_options.add_argument("--disable-features=NetworkServiceInProcess")  # 프로세스 내 네트워크 서비스 비활성화
        chrome_options.add_argument("--disable-features=Translate")  # 번역 기능 비활성화
        chrome_options.add_argument("--disable-features=TranslateScriptURL")  # 번역 스크립트 비활성화
        
        # 메모리 제한 설정
        chrome_options.add_argument("--memory-pressure-off")  # 메모리 압력 감지 비활성화
        # chrome_options.add_argument("--js-flags=--max-old-space-size=128")  # V8 힙 크기 제한 (MB)
        
        # 사용자 에이전트 설정
        chrome_options.add_argument(f'user-agent={settings.USER_AGENT}')
        
        return chrome_options

    def _get_driver(self) -> webdriver.Chrome:
        """
        GCP / Local PC에 따라 적절한 ChromeDriver를 설정하여 드라이버를 반환하는 메서드
        
        Returns:
            webdriver.Chrome: 설정된 ChromeDriver 인스턴스
        """
        chrome_options = self._setup_chrome_options()
        
        # GCP 환경의 ChromeDriver 경로
        import os
        gcp_chromedriver_path = "/usr/bin/chromedriver"
        # GCP 환경 확인 (GCP의 ChromeDriver가 존재하는지 확인)
        if os.path.exists(gcp_chromedriver_path):
            service = Service(executable_path=gcp_chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        # 타임아웃 설정
        driver.set_page_load_timeout(self.timeout)
        return driver
        
    @abstractmethod
    def crawl(self) -> Dict[str, Any]:
        """
        크롤링을 수행하고 결과를 반환하는 메서드
        Returns:
            Dict[str, Any]: 크롤링 결과 데이터
        """
        driver = self._get_driver()

        try:
            driver.get(url)
            
            # 페이지 로딩 대기
            WebDriverWait(driver, self.timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            
            # 크롤링 수행
            # result = self._crawl(driver)
            # return result
        except Exception as e:
            raise Exception(f"Selenium 크롤링 실패: {str(e)}")
        finally:
            driver.quit()