import requests
import time
import parsel
import csv
import re

baidu_url = 'https://top.baidu.com/board?tab=realtime'
baidu_headers = {
    'cookie':  请键入您的cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37'
}


weibo_url = 'https://s.weibo.com/top/summary/summary?cate=realtimehot'
weibo_headers = {
    'cookie':  请键入您的cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48'
}


zhihu_url = 'https://www.zhihu.com/billboard'
zhihu_headers = {
    'cookie':  请键入您的cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


def crawler():
    def baidu_crawler(timeReform):
        baidu_response = requests.get(url=baidu_url, headers=baidu_headers)
        f = open('./data/BD/' + timeReform + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=['排名', '标题', '热度'])
        csv_writer.writeheader()

        selector = parsel.Selector(baidu_response.text)
        trs = selector.css(
            '#sanRoot.wrapper.c-font-normal.rel main.rel.container_2VTvm div.container.right-container_2EFJr div.container-bg_lQ801 div div.category-wrap_iQLoo.horizontal_1eKyQ')
        num = 0
        for tr in trs:
            title = tr.css('div.content_1YWBm a.title_dIF3B div.c-single-text-ellipsis::text').get()
            hot = tr.css('div.trend_2RttY.hide-icon div.hot-index_1Bl1a::text').get()
            dit = {'排名': num, '标题': title, '热度': hot}
            csv_writer.writerow(dit)
            num += 1

    def weibo_crawler(timeReform):
        weibo_response = requests.get(url=weibo_url, headers=weibo_headers)
        f = open('./data/WB/' + timeReform + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=['排名', '标题', '热度'])
        csv_writer.writeheader()

        selector = parsel.Selector(weibo_response.text)
        trs = selector.css('#pl_top_realtimehot tbody tr')
        num = 1
        for tr in trs:
            title = tr.css('.td-02 a::text').get()
            hot = tr.css('.td-02 span::text').get()
            if hot is not None:
                if hot != ' ':
                    hot = list(hot)
                    for i in range(len(hot)):
                        # 利用正则表达式替换所有非数字部分
                        hot[i] = re.sub(r'\D', '', hot[i])
                    hot = ''.join(hot)
                    dit = {'排名': num, '标题': title, '热度': hot}
                    csv_writer.writerow(dit)
                    num += 1
            else:
                pass

    def zhihu_crawler(timeReform):
        zhihu_response = requests.get(url=zhihu_url, headers=zhihu_headers)
        f = open('./data/ZH/' + timeReform + '.csv', mode='w', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=['排名', '标题', '热度'])
        csv_writer.writeheader()

        selector = parsel.Selector(zhihu_response.text)
        trs = selector.css('#root div.App main.App-main div.Card a.HotList-item div.HotList-itemBody')
        num = 1
        for tr in trs:
            title = tr.css('.HotList-itemTitle::text').get()
            hot = tr.css('.HotList-itemMetrics::text').get()
            if hot is not None:
                hot = list(hot)
                for i in range(len(hot)):
                    # 利用正则表达式替换所有非数字部分
                    hot[i] = re.sub(r'\D', '', hot[i])
                hot = ''.join(hot)
                if hot != '':
                    dit = {'排名': num, '标题': title, '热度': hot}
                    csv_writer.writerow(dit)
                    num += 1
            else:
                pass
            num += 1

    print("欢迎使用bwz_crawler程序！该程序每10分钟爬取一次数据。")
    while True:
        timeStamp = time.time()
        timeArray = time.localtime(timeStamp)
        timeReform = time.strftime("%m%d%H%M", timeArray)
        time_demo = time.strftime("%m月%d日%H时%M分")
        timeReform = timeReform[0:7]
        print(f"-----现在是{time_demo} 正在爬取数据-----")
        baidu_crawler(timeReform)
        weibo_crawler(timeReform)
        zhihu_crawler(timeReform)
        time.sleep(600)


if __name__ == '__main__':
    crawler()
