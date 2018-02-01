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
            continue
    return '\n'.join(p_list)


def sdu_get_detail_url():
    url = 'http://www.view.sdu.edu.cn/sdyw/{page_num}.htm'
    for page_num in range(430):
        try:
            resp = requests.get(url.format(page_num=page_num))
        except requests.RequestException:
            logging.critical('can not reach site, maybe blocked')
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html5lib')
        for i in soup.find_all(id=re.compile('line_u7_\d?')):
            try:
                found_url = i.find('a')['href']
            except:
                logging.warning('no url found at %s' % url)
                continue
            result = sdu_get_detail_page(urljoin(url, found_url))
            f = open('./data/sdu/{}'.format(uuid.uuid5(uuid.NAMESPACE_URL, found_url)), 'w+')
            f.write(result)
            f.flush()
            f.close()


if __name__ == '__main__':
    sdu_get_detail_page()
