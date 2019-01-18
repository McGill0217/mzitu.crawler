# /usr/bin/python3
# -*- coding: utf8

import logging
import os
import random
import re
import requests
from urllib import request
import sys
import time
from lxml import etree


# 定义日志处理函数
def logger(
        log_file='',
        log_console=False,
        log_format='%(asctime)s - %(levelname)s - %(message)s',
        log_setlevel=logging.DEBUG,
):
    # 如果未设置日志文件和控制台，返回None，结束运行
    if log_file == '' and log_console is False:
        return None
    else:
        # 日志处理基本设置
        logger = logging.getLogger(__name__)  # 新建一个logging对象
        logger.setLevel(level=log_setlevel)  # 设置日志记录等级
        logging_formatter = logging.Formatter(log_format)
        # 如果定义了日志文件，则设置日志文件
        if log_file != '':
            # 设置日志文件
            logging_file = logging.FileHandler(log_file)
            logging_file.setLevel(level=log_setlevel)
            logging_file.setFormatter(logging_formatter)
            logger.addHandler(logging_file)
        # 如果定义了控制台，则设置控制台
        if log_console is True:
            # 设置控制台
            logging_console = logging.StreamHandler(stream=sys.stdout)
            logging_console.setLevel(level=log_setlevel)
            logging_console.setFormatter(logging_formatter)
            logger.addHandler(logging_console)
        return logger


def model_findout(page_url, page_request_headers, page_xpath_expreesion,
                  logger):
    model_findout = False
    err_status = 0
    while model_findout is False and err_status <= 10:
        try:
            page_request = request.Request(
                page_url, headers=page_request_headers)
            page_http_response = request.urlopen(page_request, timeout=30)
            page_html = page_http_response.read().decode('utf-8')
            page_tree = etree.HTML(page_html)
            model_data = page_tree.xpath(page_xpath_expreesion)
            model_findout = True
            # 返回model_data
            return model_data
        except Exception:
            err_status += 1
            random_int = random.randint(30, 60)
            logger.debug('在网页 ' + page_url + ' 中遍历 台湾妹子 时，出现错误。睡眠 ' +
                         str(random_int) + ' 秒钟。')
            time.sleep(random_int)
    else:
        if model_findout is True:
            logger.info('########################')
            logger.info('网页 ' + page_url + ' 中的 台湾妹子 遍历成功。')
        if err_status == 10:
            logger.debug('异常出现次数 == 10。停止遍历网页 ' + page_url)


def img_findout(picture_page_url, picture_page_request_headers,
                img_xpath_expression, logger):
    img_findout = False
    err_status = 0
    while img_findout is False and err_status <= 10:
        try:
            img_page_request = request.Request(
                picture_page_url, headers=picture_page_request_headers)
            img_page_http_response = request.urlopen(
                img_page_request, timeout=30)
            img_page_html = img_page_http_response.read().decode('utf-8')
            img_page_tree = etree.HTML(img_page_html)
            img_data = img_page_tree.xpath(img_xpath_expression)
            img_findout = True
            # 返回img_data
            return img_data
        except Exception:
            err_status += 1
            random_int = random.randint(30, 60)
            logger.debug('在网页 ' + picture_page_url + ' 中搜索图片时，出现错误。睡眠 ' +
                         str(random_int) + ' 秒钟。')
            time.sleep(random_int)
    else:
        if img_findout is True:
            logger.info('########################')
            logger.info('网页 ' + picture_page_url + ' 中的 图片 搜索成功。')
        if err_status == 10:
            logger.debug('异常出现次数 == 10。停止搜索网页 ' + picture_page_url + ' 中的图片')


def picture_page_num_findout(picture_page_url, picture_page_request_headers,
                             picture_page_num_xpath_expression):
    picture_page_num_findout = False
    err_status = 0
    while picture_page_num_findout is False and err_status <= 10:
        try:
            picture_page_request = request.Request(
                picture_page_url, headers=picture_page_request_headers)
            picture_page_http_response = request.urlopen(
                picture_page_request, timeout=30)
            picture_page_html = picture_page_http_response.read().decode(
                'utf-8')
            picture_page_tree = etree.HTML(picture_page_html)
            picture_page_num_data = picture_page_tree.xpath(
                picture_page_num_xpath_expression)
            picture_page_num_findout = True
            # 返回img_data
            return picture_page_num_data
        except Exception:
            err_status += 1
            random_int = random.randint(30, 60)
            logger.debug('在网页 ' + picture_page_url + ' 中搜索图片总数时，出现错误。睡眠 ' +
                         str(random_int) + ' 秒钟。')
            time.sleep(random_int)
    else:
        if picture_page_num_findout is True:
            logger.info('网页 ' + picture_page_url + ' 中的 图片总数搜索成功。')
        if err_status == 10:
            logger.debug('网页 ' + picture_page_url + ' 中的 图片总数搜索失败。')


def img_download(img_url, img_save_dir, img_request_headers, logger):
    img_url_split = img_url.split('/', -1)
    img_file_name = img_url_split[-1]
    img_downloaded = False
    err_status = 0
    while img_downloaded is False and err_status <= 10:
        try:
            img_html = requests.get(
                img_url, headers=img_request_headers, timeout=30)
            with open(img_save_dir + '/' + img_file_name, 'wb') as img_file:
                img_file.write(img_html.content)
                img_downloaded = True
                logger.info('图片 ' + img_file_name + ' 下载成功。')
        except Exception:
            err_status += 1
            random_int = random.randint(30, 60)
            logger.debug('图片 ' + img_file_name + ' 下载失败。睡眠 ' +
                         str(random_int) + ' 秒钟。')
    else:
        return img_downloaded


if __name__ == '__main__':
    # 定义目录前缀
    dir_prefix = 'E:\\妹子图\\台湾妹子\\'
    # 配置日志
    log_file = dir_prefix + 'log.txt'
    logger = logger(log_file=log_file, log_console=True)

    # 遍历 台湾妹子 的所有页面
    for page_url_index in range(1, 12 + 1):
        page_url_prefix = 'https://www.mzitu.com/taiwan/page/'
        page_url_suffix = '/'
        page_url = page_url_prefix + str(page_url_index) + page_url_suffix
        page_request_headers = {
            'Referer':
            'https://www.mzitu.com/taiwan/',
            'Cookie':
            'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547555739,1547555783; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547735534',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        page_xpath_expreesion = "//ul[@id='pins']/li/span/a"
        err_status1 = 0
        job_finished = False
        model_data = []
        while job_finished is False and err_status1 <= 10:
            try:
                model_data = model_findout(page_url, page_request_headers,
                                           page_xpath_expreesion, logger)
                job_finished = True
            except Exception:
                err_status1 += 1
                random_int = random.randint(30, 60)
                logger.debug('搜索台湾妹子出现异常。睡眠 ' + random_int + ' 秒钟。')
                time.sleep(random_int)
        for each_model_data in model_data:
            # 获取 台湾妹子 URL 和 描述
            model_url = each_model_data.attrib['href']
            model_text = each_model_data.text
            # 去除目录中的特殊字符： \/:*?"<>|
            model_name = re.sub(r'[\/:*?"<>|]', '', model_text)
            model_dir = dir_prefix + model_name + '\\'
            # 建立目录，用于保存图片
            if os.path.exists(model_dir) is False:
                try:
                    os.makedirs(model_dir, 0o777)
                    logger.info('创建目录：' + model_dir)
                except Exception:
                    logger.debug('创建目录 ' + model_dir + ' 出错。')

            # 查找本妹子图片总数
            picture_page_num_xpath_expression = "//div[@class='pagenavi']/a/span"
            picture_page_prefix = model_url + '/'
            picture_page_index = 1
            picture_page_suffix = ''
            picture_page_url = picture_page_prefix + str(
                picture_page_index) + picture_page_suffix
            picture_page_request_preferer = picture_page_url
            picture_page_request_headers = {
                'Referer':
                picture_page_request_preferer,
                'Cookie':
                'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547555739,1547555783; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547735534',
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
            picture_page_num_data = picture_page_num_findout(
                picture_page_url, picture_page_request_headers,
                picture_page_num_xpath_expression)
            picture_page_num = int(picture_page_num_data[-2].text)
            logger.info('本妹子的图片数量：' + str(picture_page_num))

            # 搜索妹子的图片
            while picture_page_index <= picture_page_num:
                picture_page_suffix = ''
                picture_page_url = picture_page_prefix + str(
                    picture_page_index) + picture_page_suffix
                picture_page_request_preferer = picture_page_url
                picture_page_request_headers = {
                    'Referer':
                    picture_page_request_preferer,
                    'Cookie':
                    'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1547555739,1547555783; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1547735534',
                    'User-Agent':
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                }
                img_xpath_expression = "//div[@class='main-image']/p/a/img"
                img_data = img_findout(picture_page_url,
                                       picture_page_request_headers,
                                       img_xpath_expression, logger)

                img_url = img_data[0].attrib['src']
                img_request_headers = picture_page_request_headers
                err_status2 = 0
                img_downloaded = False
                while img_downloaded is False and err_status2 <= 10:
                    try:
                        img_downloaded = img_download(
                            img_url, model_dir, img_request_headers, logger)
                    except Exception:
                        err_status2 += 1
                        random_int = random.randint(30, 60)
                        logger.debug('下载图片 ' + img_url + ' 时出错。 睡眠 ' +
                                     str(random_int) + ' 秒钟。')
                        time.sleep(random_int)
                # 准备查找下一张图片的 url
                picture_page_index += 1

            # 下载完一个妹子的图片，睡眠 30 - 60 秒钟
            random_int = random.randint(30, 60)
            logger.info('本妹子图片下载完成。睡眠 ' + str(random_int) + ' 秒钟。')
            time.sleep(random_int)
    logger.info('恭喜，下载完毕！')
