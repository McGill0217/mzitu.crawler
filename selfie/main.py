# /usr/bin/python3
# -*- coding: utf-8
import logging  # 日志处理
import random
import requests
import sys
import time
from urllib import request
from lxml import etree


def logging_display(log_file_name="", log_file_dir="", console=False):
    # 日志格式：日期 - 时间 - 日志
    LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # 日志处理基本设置
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    logging_formatter = logging.Formatter(LOGGING_FORMAT)
    if log_file_name != "":
        # 设置日志文件
        log_file = logging.FileHandler(log_file_dir + log_file_name)
        log_file.setLevel(level=logging.DEBUG)
        log_file.setFormatter(logging_formatter)
    if console is True:
        # 设置控制台
        console = logging.StreamHandler(stream=sys.stdout)
        console.setLevel(level=logging.DEBUG)
        console.setFormatter(logging_formatter)
    logger.addHandler(log_file)
    logger.addHandler(console)
    return logger


def sleep_random_time(lower_time, longer_time, logger):
    random_int = random.randint(lower_time, longer_time)
    time.sleep(random_int)  # 出现异常时，随机睡眠30-60秒钟
    logger.debug("出现异常！睡眠 " + str(random_int) + " 秒钟后重启！")


def page_findout(page_url_prefix, page_url_index, page_url_suffix,
                 page_url_headers, logger):
    page_url = page_url_prefix + str(page_url_index) + page_url_suffix
    picture_findout = False
    err_status = 0

    while picture_findout is False and err_status < 10:
        try:
            page_request = request.Request(page_url, headers=page_url_headers)
            page_http_response = request.urlopen(page_request, timeout=30)
            page_html = page_http_response.read().decode("utf-8")
            page_tree = etree.HTML(page_html)
            picture_data = page_tree.xpath("//img[@class='lazy']")
            logger.info("##############################")
            logger.info("网址：" + page_url)  # 记录网页地址
            picture_findout = True
            # 返回 picture_data
            return picture_data
        except Exception:  # 处理异常
            err_status += 1  # 异常出现次数自增1
            sleep_random_time(30, 60, logger)
    else:
        if picture_findout is True:
            logger.info("本网页图片搜索完毕！")
        if err_status == 10:
            logger.debug("异常出现次数 = 10！停止遍历本页网页！")


def picture_download(picture_url, picture_save_dir, picture_url_headers):
    picture_url_split = picture_url.split('/', -1)
    picture_file_name = picture_url_split[-1]
    picture_downloaded = False
    err_status = 0
    while picture_downloaded is False and err_status <= 10:
        try:
            picture_html = requests.get(
                picture_url, headers=picture_url_headers, timeout=30)
            with open(picture_save_dir + picture_file_name,
                      'wb') as picture_file:
                picture_file.write(picture_html.content)
                picture_downloaded = True
                logger.info('下载成功。图片 = ' + picture_url)
        except Exception:
            err_status += 1
            sleep_random_time(30, 60, logger)


if __name__ == "__main__":
    picture_save_dir = 'E:/妹子图/妹子自拍/'
    # 日志设置
    logger = logging_display(
        log_file_name="妹子自拍_log.txt",
        log_file_dir=picture_save_dir,
        console=True)
    # 遍历网页页面，搜索出所有图片链接
    for page_url_index in range(1, 377 + 1):  # 遍历所有网页页面
        page_url_prefix = 'https://www.mzitu.com/zipai/comment-page-'
        page_url_suffix = '/#comments'
        if page_url_index == 1:
            page_request_referer = page_url_prefix + str(377) + page_url_suffix
        else:
            page_request_referer = page_url_prefix + str(page_url_index -
                                                         1) + page_url_suffix
        page_url_headers = {
            'Cookie':
            'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547555739,1547555783; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547556251',
            'Referer':
            page_request_referer,
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        picture_data = page_findout(page_url_prefix, page_url_index,
                                    page_url_suffix, page_url_headers, logger)
        # 处理数据并保存图片
        for each_picture_data in picture_data:
            # 获取图片 URL
            picture_url = each_picture_data.attrib['data-original']
            # 保存图片
            picture_download(picture_url, picture_save_dir, page_url_headers)
        if page_url_index % 5 == 0:
            logger.info('网页页面 ' + page_url_prefix + str(page_url_index) +
                        page_url_suffix + ' 处理完成。暂停 180 秒。')
            time.sleep(180)
