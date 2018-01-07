import threading, queue
import html_parser, html_outputer, html_downloader
import time
import webbrowser


class Spider(object):
    def __init__(self, tp, seed):
        self.tp = tp
        self.seed = seed
        self.visited = set()
        self.html_outputer = html_outputer.HtmlOutputer()
        self.html_parser = html_parser.HtmlParser()
        self.html_downloader = html_downloader.HtmlDownloader()

    def parser(self, url):
        if url in self.visited:
            return
        if len(self.visited) >= m:
            return
        print(url, threading.current_thread())
        try:
            self.visited.add(url)
            content = self.html_downloader.download(url)
            urls, data = self.html_parser.parse(url, content)
            self.html_outputer.collect_data(data)
            for url in urls:
                if url is None:
                    continue
                self.tp.add_job(self.parser, url)  # 添加一个任务
        except Exception as e:
            print(e)

    def work(self):
        self.tp.add_job(self.parser, self.seed)
        self.tp.wait_all_complete()


class ThreadingPool(object):
    def __init__(self, num):
        self.work_queue = queue.Queue()
        self.threads = []
        self.thread_num = num
        self._init_pool(num)

    # 初始化线程池
    def _init_pool(self, num):
        for i in range(num):
            self.threads.append(Work(self.work_queue))

    # 添加一项任务入队
    def add_job(self, func, *args):
        self.work_queue.put((func, args))

    # 等待所有线程运行结束
    def wait_all_complete(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.join()


class Work(threading.Thread):
    def __init__(self, work_queue, timeout=2):
        super(Work, self).__init__()
        self.work_queue = work_queue
        self.timeout = timeout  # 等待任务队列多长时间
        self.start()

    def run(self):
        while True:
            # 死循环，直到没有任务
            try:
                func, args = self.work_queue.get(timeout=self.timeout)  # 任务出队列,Queue内部实现了同步机制
                func(*args)  # 执行任务
                self.work_queue.task_done()  # 任务结束
            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    seed = str(input('输入要爬取的百度百科词条链接：'))
    m = int(input('输入要爬取的相关词条信息数量：'))
    start = time.time()
    tp = ThreadingPool(3)
    spider = Spider(tp, seed)
    spider.work()
    spider.html_outputer.output_html()
    end = time.time()
    print('爬取完毕，用时%f秒' % (end-start))
    if input('是否打开爬取结果？<Y/N>:') == 'Y':
        webbrowser.open('output.html')
