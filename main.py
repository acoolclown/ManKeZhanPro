# TODO 启动这里运行爬虫
# TODO 负责有序调度函数

"""
Columns_Spider(self, URL)--------------- 爬取分专栏函数-------------- 
Comic_Spider(self, Column_Url)---------- 爬取单个专栏的所有漫画函数---- 
Chapter_Spider(self, Column_Url)-------- 爬取单个漫画所有章节函数------ 
Image_Spider(self, Chapter_Url)--------- 爬取单个章节所有图片函数------ 
"""
import time
from main import *
from threading import Thread

# 初始化
MKZ = ManKeZhanPro()
URL = 'http://www.mkzhan.com/category/'
MIX_CELL = []  # 数据存储的最小 块单位 结构为:单个漫画的所有 章节名称和图片字典的列表
MIDDLE_CELL = []  # 数据存储的最中 块单位 结构为:单个专栏的所有
MAX_CELL = []  # 数据存储的最大 块单位 结构为:单个总专栏的所有
DICT_COMIC = {}

# 计数器
COLUMN_NUM = 1  # 专栏计数
COMIC_NUM = 1  # 漫画计数
CHAPTER_NUM = 1  # 章节计数
IMAGE_NUM = 1  # 图片计数
NUM_DATA = {'累计爬取专栏': COLUMN_NUM, '累计爬取漫画': COMIC_NUM, '累计爬取图片': IMAGE_NUM}  # 统计数量

print('--------------------------------------漫客栈正在爬取-----------------------------------------')
# 开始计时
START_TIME = time.time()

COLUMNS = MKZ.Columns_Spider(URL)
for COLUMN_NAME, COLUMN_URL in COLUMNS.items():
    """
    COLUMN_NAME:专栏名
    COLUMN_URL:专栏url
    """
    print(f'×××××正在爬取 第 {COLUMN_NUM} 个 {COLUMN_NAME}专栏，url:{COLUMN_URL} ')
    COMICS = MKZ.Comics_Spider(COLUMN_URL)
    COLUMN_NUM += 1
    for COMIC_NAME, COMIC_URL in COMICS.items():
        """
        COMIC_NAME:漫画名字
        COMIC_URL:漫画url
        """
        print(f'××××××××××正在爬取 第 {COMIC_NUM} {COMIC_NAME} 漫画，url:{COMIC_URL}')
        DICT_FOLLOW = {COMIC_NAME: COMIC_URL}
        DESCRIOTION = MKZ.Comic_Des_Spider(COMIC_URL)
        CHAPTER_URLS = MKZ.Chapter_Urls_Spider(COMIC_URL)
        DICT_FOLLOW.update(DESCRIOTION)
        MIX_CELL.append(DICT_FOLLOW)
        for CHAPTER_URL in CHAPTER_URLS:
            MIX_DICT = MKZ.Image_Spider(CHAPTER_URL)[0]
            IMAGE_NUM = MKZ.Image_Spider(CHAPTER_URL)[1]
            print(f'××××××××××××××××正在爬取漫画 {COMIC_NAME} 的 {CHAPTER_URL} 章节 已爬取图片 {IMAGE_NUM}')
            MIX_CELL.append(MIX_DICT)
            DICT_COMIC[COMIC_NAME] = MIX_CELL
            MIX_CELL = []

            # 统计数量
            NUM_DATA = {'累计爬取专栏': COLUMN_NUM, '累计爬取漫画': COMIC_NUM, '累计爬取图片': IMAGE_NUM}

        print(f'××××××××××爬取结束 第{COMIC_NUM} {COMIC_NAME} 漫画，url:{COMIC_URL}')
        print(f'已成功爬取漫画{COMIC_NUM}个 累计爬取图片数量:{IMAGE_NUM}')

        # 统计数量
        NUM_DATA = {'累计爬取专栏': COLUMN_NUM, '累计爬取漫画': COMIC_NUM, '累计爬取图片': IMAGE_NUM}

        with open(f'/home/jiahuan/PyPr/MKZ_DATA/{COLUMN_NAME} {COMIC_NAME}.json', 'w', encoding='utf-8') as fp:
            fp.write(str(DICT_COMIC))

        COMIC_NUM += 1  # 漫画计数器

    print(f'已成功爬取 专栏 {COLUMN_NAME} 累计漫画{COMIC_NUM}个 累计爬取图片数量:{IMAGE_NUM}')
    MIDDLE_CELL.append(DICT_COMIC)
    DICT_COLUMN = {"专栏 " + COLUMN_NAME: MIDDLE_CELL}

    with open(f'/home/jiahuan/PyPr/MKZ_DATA/{COLUMN_NAME}.json', 'w', encoding='utf-8') as fp:
        fp.write(str(DICT_COLUMN))
    print(MIDDLE_CELL)

    MAX_CELL.append(DICT_COLUMN)

    # 统计数量
    NUM_DATA = {'已爬取专栏': COLUMN_NUM, '累计爬取漫画': COMIC_NUM, '累计爬取图片': IMAGE_NUM}
    COLUMN_NUM += 1
    
DATA = {'MKZ': MAX_CELL}

print('--------------------------------------漫客栈爬取结束-----------------------------------------')

END_TIME = time.time()
PASET_TIME = START_TIME - END_TIME
print(f'总用时 {PASET_TIME/3600} h ')
print(NUM_DATA)
