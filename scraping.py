from requests_html import HTMLSession
from time import sleep
import datetime
import csv
import re

format_url = "https://www.nikon.co.jp/search/index.htm?q={}&r=1%3Anikonjp&c=30"
query = "ヘルスケア"


def has_next_page(html):
    class_ = html.find("._next", first=True).attrs["class"]
    if "_noanc" in class_:
        return False
    else:
        return True


def extract_urls(target_url, extracted_urls):
    # htmlを取得
    session = HTMLSession()
    r = session.get(target_url)
    r.html.render()

    # 検索結果のURLを抽出
    result_divs = r.html.find("._records", first=True)
    result_urls = result_divs.absolute_links
    for url in result_urls:
        if "www.nikon.co.jp/news/" in url:
            extracted_urls.append(url)

    if has_next_page(r.html):
        next_page_url = r.html.find("._next", first=True).absolute_links.pop()
        print("*", end="")
        return extract_urls(next_page_url, extracted_urls)
    else:
        # サーバーに負荷をかけないために２秒停止
        sleep(2)
        return extracted_urls


# クエリとURLを組み合わせて完全なURLを生成
filled_url = format_url.format(query)

# スクレイピング
result_urls = extract_urls(filled_url, [])

domein = re.search(r"(?<=//)[a-z\.]+", filled_url).group()
time = datetime.datetime.now().strftime("%Y%m%d")
filename = "{}_{}_urls.csv".format(time, domein)

# csv形式でファイルに書き込み
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    for i in result_urls:
        writer.writerow([i])

print("\nFinished!!")
