from baiduspider import BaiduSpider
import threading
import requests
import argparse
import time
import concurrent.futures

spider = BaiduSpider()
page_lock = threading.Lock()
file_lock = threading.Lock()

start = 0
content = ""
file = "result.txt"

def sp(j):
    global start
    global content
    global file
    with page_lock:
        n_start = start
        n_end = start + j
        start = start + j
    for i in range(n_start,n_end):
        print('正在爬取第', i, '页')
        dic = spider.search_web(query=content, pn=i)
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help="The content which you want to search", required=True)
    parser.add_argument('--start', help="The page which you want to start", required=True)
    parser.add_argument('--end', help="The page which you want to end", required=True)
    args = parser.parse_args()
    args_dict = args.__dict__
    try:
        content = args_dict['c']
        start = int(args_dict['start'])
        end = int(args_dict['end'])
        num = end - start
        if num < 0:
            raise Exception(print("输入错误。"))
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            for i in range(0, num):
                future = pool.submit(sp, 1)
        end_time = time.time()
        print('任务执行完毕，耗时',end_time-start_time,'S,任务结果已经输出到了result.txt中')
    except Exception:
        print(Exception)