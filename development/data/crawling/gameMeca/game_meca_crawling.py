import requests
from bs4 import BeautifulSoup, Comment
import json
import time


def fetch_news_content(news_url):
    """뉴스 URL에서 본문 콘텐츠, 게시판(board), 작가(author)를 가져오는 함수"""
    response = requests.get(news_url)
    if response.status_code != 200:
        print(f"Failed to fetch content from {news_url}")
        return None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')

    article_div = soup.select_one('#content > div.news-view > div.content-left > div.article')

    direct_text_divs = [div.get_text(strip=True) for div in article_div.find_all('div', recursive=False) if div.get_text(strip=True)]

    # 게시판 이름 추출
    board = None
    board_li = soup.select_one(".section >ul.lnb-sub-left > li.on > a")
    if board_li:
        comments = board_li.find_all(string=lambda text: isinstance(text, Comment))
        board = "".join(comments).strip() if comments else None

    # 작가 이름 추출
    author_div = soup.select_one("#content > div.article-title > div.article-info > span.writer")
    author = author_div.get_text(strip=True) if author_div else "(이름)"

    return direct_text_divs, board, author


def save_news_to_json(filename="news_data.json", news_data=[]):
    """Save news data as JSON"""
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)

    print(f"News data saved to {filename} with {len(news_data)} articles")


def get_news(max_news=180000):
    url = f"https://www.gamemeca.com/news.php"
    news_data = []
    page_index = 0
    index = 0
    file_name_index = 0
    while index < max_news:
        page_index += 1

        if len(news_data) > 10000:
            save_news_to_json(filename='news_data_' + str(file_name_index) + '.json', news_data=news_data)
            file_name_index += 1
            index += len(news_data)
            news_data = []

        print(len(news_data), page_index)
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to retrieve the page")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.select("#content > div.news-list > div > ul > li")

        for item in news_list:
            if len(news_data) >= max_news:
                break

            a_tag = item.select_one("a")
            path = a_tag["href"]
            news_url = f"https://www.gamemeca.com/{path}"

            title = item.select_one("div > strong > a").text.strip() if item.select_one("div > strong > a") else None
            date = item.select_one(".day_news").text.strip() if item.select_one(".day_news") else None
            content, board, author = fetch_news_content(news_url)
            news_data.append(
                {"url": news_url, "title": title, "source_site": "게임메카", "write_date": date,
                 "content": content, "writer": author})

        next_page = soup.select_one("#content > div.news-list > div.content-left > div > a.num_next")
        if next_page and next_page.get('href'):
            next_page_url = "https://www.gamemeca.com/" + next_page["href"]
            url = next_page_url
            time.sleep(1)
        else:
            break

    # Final save after all pages are processed
    save_news_to_json(filename='news_data_'+str(file_name_index)+'.json', news_data=news_data)

# Start the data collection
get_news()
