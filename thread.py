import requests
from baiduspider import BaiduSpider
import threading

page = 0
spider = BaiduSpider()
page_lock = threading.Lock()     # step 1: 创建互斥锁
file_lock = threading.Lock()
threads = []
s = "site:*.edu.cn"
file = "thread1.txt"

def sp(j):
    global page
    global s
    global file
    with page_lock:
        n_start = page
        n_end = page + j
        page = page + j
    i: int
    for i in range(n_start,n_end):
        print('正在爬取第', i, '页')
        dic = spider.search_web(query=s, pn=i)
        results = dic['results']
        r = 0
        for q in results:
            r = r + 1
            if r > 2:
                k = q['url']
                try:
                    headers = requests.head(url=k).headers
                    u = headers.get("Location")
                    with file_lock:
                        with open(file, 'a') as f:
                            f.write(u + '\n')
                except Exception:
                    print("写入异常")
        print('第', i, '页爬取完毕')

if __name__ == "__main__":
    for i in range(0,2):
        threads.append(
            threading.Thread(target=sp,args=(50,))
        )
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("over...")