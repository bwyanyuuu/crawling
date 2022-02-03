#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2018.02.05
"""Capture pictures from sina-weibo with user_id."""

from cgitb import html
import re
import os
import sys

import socket
import urllib.request

from bs4 import BeautifulSoup

fd_error = open('D:/chiao6673/error.txt','a')
fd_record = open('D:/chiao6673/record.txt','a')
def get_path(user):
    home_path = os.path.expanduser('~')
    #path = os.path.join(home_path, 'Pictures/python/sina', uid)
    path = 'D:/chiao6673/michieda'# + user
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_html(url, headers):
    try:
        req = urllib.request.Request(url, headers = headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')
    except Exception as e:
        print("get %s failed" % url)
        return None
    return html

def get(url, headers):
    cnt = 0
    html = get_html(url, headers)
    while html == None and cnt < 3:
        cnt += 1
        html = get_html(url, headers)
    if html == None:
        exit()
    return html


def capture_images(uid, user, headers, path, start_page, start_idx):
    filter_mode = 0      # 0-all 1-original 2-pictures
    num_pages = start_page
    num_imgs = start_idx

    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imglist_pattern = re.compile(imglist_reg)
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/006zy5.{26,29}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)
    print('start capture picture of uid:' + uid)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (uid, filter_mode, num_pages)

        # 1. get html of each page url
        html = get(url, headers)

        # 2. parse the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "lxml")
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False)

        imgurls = []
        for blog in blogs:
            blog = str(blog)
            imglist_url = imglist_pattern.findall(blog)
            if not imglist_url:
                # 2.1 get img-url from blog that have only one pic
                imgurls += img_pattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = get(imglist_url[0], headers)
                imgurls += img_pattern.findall(html)

        if num_pages <= 0:
            break

        # 3. download all the imgs from each imgList
        print('PAGE %d with %d images' % (num_pages, len(imgurls)))
        imgurls.reverse()
        for img in imgurls:
            imgurl = img[0].replace(img[1], 'large')
            count = 1

            if num_imgs >= start_idx:
                try:
                    urllib.request.urlretrieve(imgurl, '{}/{}_{:0>5d}.{}'.format(path, user, num_imgs, img[2]))
                except Exception as e:
                    print(e)
                    while count <= 3:
                        try:
                            urllib.request.urlretrieve(imgurl, '{}/{}_{:0>5d}.{}'.format(path, user, num_imgs, img[2]))
                            break
                        except Exception as e:
                            print(e)
                            count += 1
                finally:
                    # display the raw url of images
                    txt = '\t%5d\t%s\n' % (num_imgs, imgurl)
                    fd_record.write(txt)
                    print('\t%5d\t%s' % (num_imgs, imgurl))
                    if count > 3:
                        print('\t%d\t%s failed' % (num_imgs, imgurl))
                        errtxt = "%s %d %s\n" % (user, num_imgs, imgurl)
                        fd_error.write(errtxt)
                    pass
            num_imgs += 1
        num_pages -= 1
        print('')
    


def main():
    if len(sys.argv) < 3:
        print("Usage: python sina_image_download.py [page] [idx]")
        exit()
    # http://ww3.sinaimg.cn/large/006zy5lRgy1gyyvubevxhj30yi1mkgsx.jpg
    start_page = int(sys.argv[1])
    start_idx = int(sys.argv[2])

    user = 'michieda_oo'
    uid = '6022092479'  
    path = get_path(user)
    socket.setdefaulttimeout(20)
    # cookie is form the above url->network->request headers
    cookies = 'SUB=_2A25M_TjIDeRhGeNL6VYY9SjOzjmIHXVsHliArDV6PUJbktCOLWTxkW1NSQiUQEvDf4C19glwttm1maPME6bDl1HF; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpIrLebwvvgaLmZF4aOcdf5NHD95QfSKzX1K-ceo-fWs4Dqcjci--4iKnEiKnEi--4iKn7iKnfi--Xi-zRiKn7i--fi-27i-zXi--NiKnfiK.4i--4iKLFi-2R; _T_WM=65efd5bdc643adf50303a979d58f0164'
    #cookies = 'ALF=1589592746; _T_WM=93812649844; XSRF-TOKEN=e56f0f; WEIBOCN_FROM=1110006030; SCF=AlO2RfmUpkrpNUmXXgHOT6xvadMEvjQ7kiGTc6hLslFmV7J5SYdek1kDpX3FjLp5NqAS7NpX-WUyXfnALuQ88_E.; SUB=_2A25zk7FIDeRhGeNL6VYY9SjOzjmIHXVRf98ArDV6PUJbktAKLXPDkW1NSQiUQCvHR5QYvtTTFsYbhYJE5q_39J1w; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpIrLebwvvgaLmZF4aOcdf5JpX5K-hUgL.Fo-feoB4SKqESK-2dJLoI0qLxK.L1hzL1hzLxK.L1h5L1h-LxKBLBonL1h5LxK-LBK5LBoBLxKML1h-L1K.LxK.L1-zLBKnt; SUHB=0QS5jT-J78WnUb; SSOLoginState=1587003672'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}

    # record
    fd_record.write(user + ' ' + uid + '\n')

    # capture imgs from sina
    capture_images(uid, user, headers, path, start_page, start_idx)

    fd_error.close()
    fd_record.close()


if __name__ == '__main__':
    main()