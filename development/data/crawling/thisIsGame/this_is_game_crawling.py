import requests
from bs4 import BeautifulSoup, Comment
import json
import time


def fetch_news_content(news_url):

    response = requests.get(news_url)
    if response.status_code != 200:
        print(f"Failed to fetch content from {news_url}")
        return None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    article_div = soup.select_one('div.m-news-view-title-text > h2')
    author = article_div.text.split('(')[-1].split(')')[0]
    date = article_div.find('span').text

    # 게시판 이름 추출
    board = None
    board_li = soup.select_one("div.article-content > div.tig-album-news-contents-1")
    content = board_li.get_text(strip=True)


    return author, content, date


def save_news_to_json(filename="news_data.json", news_data=[]):
    """Save news data as JSON"""
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)

    print(f"News data saved to {filename} with {len(news_data)} articles")


def get_news(max_page=700):
    url = f"https://m.thisisgame.com/webzine/news/nboard/263/?page=1"
    news_data = []
    page_index = 0
    index = 0
    file_name_index = 0
    while page_index < max_page:
        page_index += 1

        if len(news_data) > 5000:
            save_news_to_json(filename='news_data_this_is_game_' + str(file_name_index) + '.json', news_data=news_data)
            file_name_index += 1
            index += len(news_data)
            news_data = []

        print(len(news_data), page_index)
        response = requests.get(url)

        if response.status_code != 200:
            print("Failed to retrieve the page")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.select("div.article-list-part > div.board-list > ul > li")

        for item in news_list:

            a_tag = item.select_one("a")
            path = a_tag["href"]
            news_url = f"https://m.thisisgame.com/webzine/news/nboard/263/{path}"

            title_all = item.select_one("a.subject-info > span > span.subject") if item.select_one("a.subject-info > span > span.subject") else None
            title = title_all.find_all(string=True, recursive=False)[-1].strip()


            author, content, date = fetch_news_content(news_url)
            
            news_data.append(
                {"url": news_url, "title": title, "source_site": "디스 이즈 게임", "write_date": date,
                 "content": content, "writer": author})

        # next_page = soup.select_one("#content > div.news-list > div.content-left > div > a.num_next")
        if page_index <= 654:
            next_page_url = "https://m.thisisgame.com/webzine/news/nboard/263/?page=" + str(page_index)
            url = next_page_url
            time.sleep(1)
        else:
            break

    # Final save after all pages are processed
    save_news_to_json(filename='news_data_this_is_game_'+str(file_name_index)+'.json', news_data=news_data)

# Start the data collection
get_news()