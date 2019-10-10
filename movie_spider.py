# *_*coding: UTF-8*_*
# Developer： zhouyao
# Dev Time:  2019/10/10 0010 上午 8:13
# File Name: spider.PY
# Dev Tool: PyCharm Community Edition
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        html = response.text.encode('latin1').decode('gbk')  # 源文件先转码成Latin1，再解码成gbk编码
        return html
        # print(data)
    except requests.HTTPError as e:
        print("http error", e)
    except requests.RequestException as e:
        print("requests exception error ", e)

def parse_data(html):
    info = []
    soup = BeautifulSoup(html, 'html.parser')

    movie_list = soup.find_all('table', attrs={'class': 'tbspan'})

    # print(movie_list)
    for list in movie_list:
        movies = []
        # 获取第二个标签
        movie = list.find_all('a')[1]
        # 获取movie的标题
        movie_title = movie['title']
        movies.append(movie_title)
        url_movie = 'https://www.dy2018.com' + movie['href']
        movies.append(url_movie)

        try:
            temp = BeautifulSoup(urlopen(url_movie), 'html.parser')
            tbody = temp.find_all('tbody')
            # print(tbody)
            for i in tbody:
                download = i.a.string
                movies.append(download)
            info.append(movies)
        except Exception as e:
            print(e)
    return info

def save_data(data):
    filename = "movie.csv"
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)

def main():
    for page in range(1,10):
        print("正在爬取：第" + str(page) + '页')
        if page == 1:
            index = 'index'
        else:
            index = 'index_' + str(page)
        url = 'https://www.dy2018.com/0/' + index + '.html'
        html = get_page(url)
        movies = parse_data(html)
        save_data(movies)

    print('爬取完成,共' + str(page) + '页')

if __name__ == '__main__':
    main()





