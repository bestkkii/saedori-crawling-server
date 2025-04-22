# 네이버 뉴스 크롤링 수행

from bs4 import BeautifulSoup
from .base import BaseCrawler

class NaverHeadlineNewsCrawler(BaseCrawler):
    URL = "https://news.naver.com/main/ranking/popularDay.naver"

    async def crawl(self) -> dict:
        html = await self.fetch(self.URL)
        soup = BeautifulSoup(html, "html.parser")

        results = []

        # 인기 뉴스 섹션에서 기사 제목과 링크 수집
        for headline in soup.select(".rankingnews_box .list_title a")[:10]:  # 상위 10개만
            title = headline.get_text(strip=True)
            link = headline.get("href")
            if link and link.startswith("/"):
                link = "https://news.naver.com" + link

            results.append({
                "title": title,
                "url": link
            })

        return {
            "source": "naver_news",
            "count": len(results),
            "articles": results
        }
