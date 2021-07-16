import requests
from baiduspider import BaiduSpider

spider = BaiduSpider()

for n in range(0,100):
    print('正在爬取第',n,'页')
    dic = spider.search_web(query='site:*.edu.cn', pn=n)
    results = dic['results']
    j = 0
    for i in results:
        j = j + 1
        if j > 2:
            k = i['url']
            try:
                headers = requests.head(url=k).headers
                u = headers.get("Location")
                #print(u)
                with open('target0_100.txt', 'a') as f:
                    f.write(u+'\n')
            except Exception:
                print("写入异常")
    print('第',n,'页爬取完毕')