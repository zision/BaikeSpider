import url_manager, html_downloader, html_parser, html_outputer
import time
import webbrowser


class SpiderMain(object):
    def __init__(self):  # 初始化
        self.urls = url_manager.UrlManager()  # url管理器
        self.downloader = html_downloader.HtmlDownloader()  # 下载器
        self.parser = html_parser.HtmlParser()  # 解析器
        self.outputer = html_outputer.HtmlOutputer()  # 输出器

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw %d : %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count >= m:
                    break

                count += 1

            except Exception as e:
                print(str(e))
                # 根据报错信息提示错误

            self.outputer.output_html()


if __name__ == '__main__':
    root_url = str(input('输入要爬取的百度百科词条链接：'))
    m = int(input('输入要爬取的相关词条信息数量：'))
    start = time.time()
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
    end = time.time()
    print('爬取完毕，用时%f秒' % (end-start))
    if input('是否打开爬取结果？<Y/N>:') == 'Y':
        webbrowser.open('output.html')
