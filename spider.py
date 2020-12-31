import re
import requests
from lxml import etree
from ip_pool import proxies
from User_Agent import USER_AGENT


# TODO 所有爬取工作在这里进行


# 总类 所有派生类的父类
class ManKeZhanPro(object):

    # 初始化数据
    def __init__(self):
        self.BASIC_URL = 'https://www.mkzhan.com'  # 总站url
        self.COLUMN_URLS = []
        self.DESCRIPTION = {}
        self.MIX_CELL = []
        self.IMAGE_NUM = 1

    # 定义一个方法用于请求数据和实例化etree
    # 重复性太高了 靠
    def Requests(self, url):
        res = requests.get(url, headers=USER_AGENT, proxies=proxies).content.decode()
        return etree.HTML(res)

    # TODO over--->分专栏
    def Columns_Spider(self, URL):
        # TODO 第一次循环
        """
        爬取专栏url
        作用：爬取总专栏下属所有专栏url和name
        :param URL: 总专栏url
        :return：分专栏名字和url 字典
        """
        DICT_COLUMN= {}
        tree = self.Requests(URL)
        li_list = tree.xpath('//ul[@class="cate-list clearfix"][1]/li[@class="cate-item "]')
        for li in li_list:
            n = 0
            column_url = self.BASIC_URL + li.xpath('./a/@href')[0]  # 专栏url
            column_name = li.xpath('./a//text()')[0]  # 专栏name
            self.COLUMN_URLS.append(column_url)  # url
            DICT_COLUMN[column_name] = column_url
            if column_name == '真人':
                break
        return DICT_COLUMN

    # TODO over--->专栏下所有漫画
    # 漫画爬取
    # 负责爬取单个专栏下的漫画 名字 url
    def Comics_Spider(self, Column_Url):
        # TODO 第二次循环
        """
        爬取一个专栏下的所有漫画url和name
        :param Column_Url: 类别url
        :return:
        """
        DICT_COMIC = {}
        while (1 == 1):
            tree = self.Requests(Column_Url)
            div_list = tree.xpath('//div[@class="cate-comic-list clearfix"]/div')
            for div in div_list:
                comic_url = self.BASIC_URL + div.xpath('./p[1]/a/@href')[0]  # 漫画主页url
                comic_name = div.xpath('./p[1]/a//text()')[0]  # 漫画名字
                DICT_COMIC[comic_name] = comic_url
            # 实现翻页功能
            try:
                Column_Url = self.BASIC_URL + tree.xpath('//a[@class="next"]/@href')[0]
            except Exception as e:
                return DICT_COMIC

    # TODO over--->单个漫画的所有描述数据
    # 章节爬虫
    # 负责爬取单个漫画的所有章节集合url
    def Comic_Des_Spider(self, Comic_Url):
        """
        负责爬取单个漫画的详细信息和章节url
        :param Comic_Url:单个漫画url
        :return: 详细描述信息 漫画名字
        """
        self.DESCRIPTION = {}
        tree = self.Requests(Comic_Url)
        comic_name = tree.xpath('//p[@class="comic-title j-comic-title"]//text()')[0]  # 本章名字
        # 获取详细描述
        self.DESCRIPTION['作者'] = tree.xpath('//span[@class="name"]//text()')[0]  # 作者
        self.DESCRIPTION['题材'] = tree.xpath('//span[@class="text"][1]/b//text()')[0]  # 题材
        self.DESCRIPTION['收藏'] = tree.xpath('//span[@class="text"][2]/b//text()')[0]  # 收藏
        self.DESCRIPTION['人气'] = tree.xpath('//span[@class="text"][3]/b//text()')[0]  # 人气
        self.DESCRIPTION['作品简介'] = tree.xpath('//p[@class="intro-total"]//text()')[0]  # 作品简介
        return self.DESCRIPTION

    # TODO over--->单个漫画的所有章节url
    def Chapter_Urls_Spider(self, Comic_Url):
        """
        获取单个漫画所有章节 名字和url
        :param Comic_Url: 单个漫画的url
        :return: 所有章节的url
        """
        CHAPTER_URLS = []
        res = requests.get(Comic_Url, headers=USER_AGENT).content.decode()
        pattern_url = '<a class="j-chapter-link" data-hreflink="(.*?)" data-chapterid'
        chapters_url = re.findall(pattern_url, res, re.M)
        for chapter_url in chapters_url:
            chapter_url = self.BASIC_URL + chapter_url
            CHAPTER_URLS.append(chapter_url)
        return CHAPTER_URLS

    # TODO over--->单个章节的所有图片
    # 图片爬虫
    # 负责爬取单个章节的所有图片集合url
    def Image_Spider(self, Chapter_Url):
        """
        章节名称和图片url,这是存储的最小单位
        :param Chapter_Url: 章节url
        :return:
        """
        self.IMAGE_URLS = []
        self.MIX_DICT = {}
        tree = self.Requests(Chapter_Url)
        self.chapter_name = tree.xpath('//h1[@class="comic-title"]/a/text()')[0]
        div_list = tree.xpath('//div[@class="rd-article-wr clearfix"]/div')
        try:
            for div in div_list:
                image_url = div.xpath('./img/@data-src')[0] # 漫画图片
                self.IMAGE_URLS.append(image_url)
                self.IMAGE_NUM += 1

        except Exception as e:
            self.MIX_DICT[self.chapter_name] = self.IMAGE_URLS
            NUM = 0 + self.IMAGE_NUM
            return self.MIX_DICT, NUM


if __name__ == '__main__':
    MK = ManKeZhanPro()
