# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 14:50
# @Author  : Bridge
# @Email   : 13722450120@163.com
# @File    : paper_lianxi.py
# @Software: PyCharm
import requests #pip3 install requests
import re
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(50)
movie_path = r'E:\mp466\\'


def get_page(url):
    try:
        response=requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass


def parse_index(index_page):
    index_page=index_page.result()
    urls=re.findall('class="items".*?href="(.*?)"', index_page, re.S)
    for detail_url in urls:
        if not detail_url.startswith('http'):
            detail_url='http://www.xiaohuar.com'+detail_url
        pool.submit(get_page,detail_url).add_done_callback(parse_detail)


def parse_detail(detail_page):
    detail_page=detail_page.result()
    l=re.findall('id="media".*?src="(.*?)"',detail_page,re.S)
    if l:
        movie_url=l[0]
        if movie_url.endswith('mp4'):
            # print('***********'+movie_url)
            pool.submit(get_movie, movie_url)


def get_movie(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            m=hashlib.md5()
            m.update(str(time.time()).encode('utf-8'))
            m.update(url.encode('utf-8'))
            filepath='%s\%s.mp4' % (movie_path, m.hexdigest())
            with open(filepath, 'wb') as f:
                f.write(response.content)
                print('%s 下载成功' %url)
    except Exception:
        pass


def main():
    base_url = 'http://www.xiaohuar.com/list-3-{page_num}.html'
    for i in range(5):
        url = base_url.format(page_num=i)
        print(url)
        pool.submit(get_page, url).add_done_callback(parse_index)

if __name__ == '__main__':
    main()













# 简易版爬取校花网视频




# import requests
# import re
# import hashlib
# import time

# movie_path = "E:\mp4\\"     #视频存储目录
#
#
# def get_page(url):
#     '''
#     返回一个字符串的网页页面
#     :param url:
#     :return:
#     '''
#     try:
#         response = requests.get(url)      # 请求传入的url
#         if response.status_code == 200:   # 如果页面返回200：正常返回text字符串
#             return response.text
#     except Exception:
#         pass
#
# def parse_index(index_page):
#     '''
#     正则匹配到页面中的每个视频链接[],[],[],[],[],[],[]...
#     :param index_page:
#     :return: 每次返回一个列表，也就是一个url
#     '''
#     urls = re.findall('class="items".*?href="(.*?)"', index_page, re.S)   #查找匹配的url
#     for url in urls:
#         if not url.startswith("http"):
#             '''
#             因为某些链接不知只是域名后边的字符串，所以加判断，
#             '''
#             url = "http://www.xiaohuar.com"+url
#         yield url
#
#
# def parse_detail(detail_page):
#     '''
#     接收上面函数传入的url，正则匹配查到视频的url链接
#     :param detail_page:
#     :return: 返回视频的url链接
#     '''
#     l = re.findall('id="media".*?src="(.*?)"',detail_page, re.S)
#     if l:
#         movie_url = l[0]
#         if movie_url.endswith("mp4"):
#             yield movie_url
#
#
# def get_movie(url):
#     '''
#     接收一个视频的url
#     :param url:
#     :return:
#     '''
#     try:
#         response = requests.get(url)
#         # response：请求到的资源
#         if response.status_code == 200:
#             m = hashlib.md5()
#             m.update(str(time.time()).encode("utf-8"))
#             m.update(url.encode("utf-8"))
#             filepath = "%s\%s.mp4" % (movie_path, m.hexdigest())   # 视频名字是movie_path/时间字符串的哈希值的加密字符串
#             with open(filepath, "wb") as f:
#                 f.write(response.content)                #文件是以wb模式打开，所以用content的方式写入
#                 print("%s 下载成功" % url)
#     except Exception:
#         pass
#
#
# def main():
#     '''
#     url：格式化后的url字符串；
#     index_page:第一次请求到的页面；
#     detail_urls：页面中的url列表
#     detail_page：上边列表中的url每个发送一次get请求
#     movie_urls：解析后的视频地址
#     :return: 文件写入硬盘
#     '''
#     base_url = 'http://www.xiaohuar.com/list-3-{page_num}.html'     # 请求地址
#     for i in range(5):                                              # 视频总共有五页
#         url = base_url.format(page_num=i)
#         print(url)
#         index_page = get_page(url)
#         detail_urls = parse_index(index_page)
#         for detail_url in detail_urls:
#             print(detail_url)
#             detail_page = get_page(detail_url)
#             movie_urls = parse_detail(detail_page)
#             for movie_url in movie_urls:
#                 get_movie(movie_url)
#
# if __name__ == '__main__':
#     main()