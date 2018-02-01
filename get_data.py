#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import re
import uuid
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup

logging.basicConfig()


def sdu_get_detail_page(url='http://www.view.sdu.edu.cn/info/1003/99072.htm'):
    p_list = []
    logging.critical('trying %s' % url)
    try:
        resp = requests.get(url)
    except:
        logging.critical('can not reach site, maybe blocked')
        return None
    resp.encoding = 'UTF-8'
    soup = BeautifulSoup(resp.text, 'html5lib')
    for i in soup.find(class_='news_content'):
        try:
            p_list.append(i.getText().strip())
        except:
            p_list.append(i)
    return '\n'.join(p_list)


def sjtu_get_detail_page(url='http://news.sjtu.edu.cn/info/1002/1645175.htm'):
    p_list = []
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
    except:
        logging.critical('can not reach site, maybe blocked')
        return None
    soup = BeautifulSoup(resp.text, 'html5lib')
    for i in soup.find_all(class_=re.compile('vsbcontent_.*?')):
        p_list.append(i.getText().strip())
    return ''.join(p_list)


def sjtu_get_detail_url():
    url = 'http://news.sjtu.edu.cn/jdyw/{page_num}.htm'
    for page_num in range(326):
        try:
            resp = requests.get(url.format(page_num=page_num))
        except requests.RequestException as e:
            logging.critical('can not reach site, maybe blocked')
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html5lib')
        links = soup.find_all(id=re.compile('line\d+_\d+'))
        logging.critical('found %s links' % len(links))
        for i in links:
            try:
                found_url = i.find('a')['href']
            except:
                logging.warning('no url found at %s' % url)
                continue
            result = sjtu_get_detail_page(urljoin('http://news.sjtu.edu.cn', found_url))
            f = open('./data/sjtu/{}'.format(uuid.uuid5(uuid.NAMESPACE_URL, found_url.encode('utf-8'))), 'w+')
            f.write(result.encode('utf-8'))
            f.flush()
            f.close()


def sdu_get_detail_url():
    url = 'http://www.view.sdu.edu.cn/sdyw/{page_num}.htm'
    for page_num in range(430):
        try:
            resp = requests.get(url.format(page_num=page_num))
        except requests.RequestException as e:
            logging.critical('can not reach site, maybe blocked')
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html5lib')
        links = soup.find_all(id=re.compile('line_u\d_\d?'))
        logging.critical('found %s links' % len(links))
        for i in links:
            try:
                found_url = i.find('a')['href']
            except:
                logging.warning('no url found at %s' % url)
                continue
            result = sdu_get_detail_page(urljoin(url, found_url))
            f = open('./data/sdu/{}'.format(uuid.uuid5(uuid.NAMESPACE_URL, found_url.encode('utf-8'))), 'w+')
            f.write(result.encode('utf-8'))
            f.flush()
            f.close()


if __name__ == '__main__':
    sjtu_get_detail_url()
