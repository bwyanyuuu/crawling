#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: litreily
# date: 2018.02.05
"""Capture pictures from sina-weibo with user_id."""

import re
import os

import socket
import urllib.request

from bs4 import BeautifulSoup

fp = open('D:/HuaChenYu/sina/error.txt','a')
fpp = open('D:/HuaChenYu/sina/record.txt','a')
def _get_path(user):
    home_path = os.path.expanduser('~')
    #path = os.path.join(home_path, 'Pictures/python/sina', uid)
    path = 'D:/HuaChenYu/sina/' + user
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _get_html(url, headers):
    try:
        req = urllib.request.Request(url, headers = headers)
        page = urllib.request.urlopen(req)
        html = page.read().decode('UTF-8')
    except Exception as e:
        print("get %s failed" % url)
        return None
    return html


def _capture_images(uid, user, headers, path, start):
    filter_mode = 0      # 0-all 1-original 2-pictures
    num_pages = 424
    num_blogs = 0
    num_imgs = start
    wr_flg = 0

    # regular expression of imgList and img
    imglist_reg = r'href="(https://weibo.cn/mblog/picAll/.{9}\?rl=2)"'
    imglist_pattern = re.compile(imglist_reg)
    img_reg = r'src="(http://w.{2}\.sinaimg.cn/(.{6,8})/d61f25de.{24,25}.(jpg|gif))"'
    img_pattern = re.compile(img_reg)
    print('start capture picture of uid:' + uid)
    while True:
        url = 'https://weibo.cn/%s/profile?filter=%s&page=%d' % (uid, filter_mode, num_pages)

        # 1. get html of each page url
        html = _get_html(url, headers)
        if html == None:
            print('\nPlease check your cookies in sina/sina_spider.py!\n')
            break

        # 2. parse the html and find all the imgList Url of each page
        soup = BeautifulSoup(html, "lxml")
        # <div class="c" id="M_G4gb5pY8t"><div>
        blogs = soup.body.find_all(attrs={'id':re.compile(r'^M_')}, recursive=False)
        num_blogs += len(blogs)

        imgurls = []
        times = []
        for blog in blogs:
            blog = str(blog)
            imglist_url = imglist_pattern.findall(blog)
            if not imglist_url:
                # 2.1 get img-url from blog that have only one pic
                imgurls += img_pattern.findall(blog)
            else:
                # 2.2 get img-urls from blog that have group pics
                html = _get_html(imglist_url[0], headers)
                imgurls += img_pattern.findall(html)

        if not imgurls and num_pages > 692:
            print('capture complete!')
            print('captured pages:%d, blogs:%d, imgs:%d' % (num_pages, num_blogs, num_imgs))
            print('directory:' + path)
            fpp.write(str(num_imgs) + '\n')
            break

        # 3. download all the imgs from each imgList
        print('PAGE %d with %d images' % (num_pages, len(imgurls)))
        for img in imgurls:
            imgurl = img[0].replace(img[1], 'large')
            num_imgs += 1
            count = 1

            if wr_flg == 0:
                fpp.write(imgurl + ' ')
                wr_flg = 1

            if num_imgs > start:
                try:
                    urllib.request.urlretrieve(imgurl, '{}/{}-{:0>5d}.{}'.format(path, user, num_imgs, img[2]))
                except Exception as e:
                    print(e)
                    while count <= 3:
                        try:
                            urllib.request.urlretrieve(imgurl, '{}/{}-{:0>5d}.{}'.format(path, user, num_imgs, img[2]))
                            break
                        except Exception as e:
                            print(e)
                            count += 1
                finally:
                    # display the raw url of images
                    print('\t%d\t%s' % (num_imgs, imgurl))
                    if count > 3:
                        print('\t%d\t%s failed' % (num_imgs, imgurl))
                        fp.write(user+'\n')
                        fp.write(str(num_imgs)+'\n')
                        fp.write(str(imgurl)+'\n')
                    pass
        num_pages += 1
        print('')
    


def main():
    user = 'mon'
    uid = '3592365534'  
    path = _get_path(user)
    socket.setdefaulttimeout(20)
    # cookie is form the above url->network->request headers
    cookies = '_T_WM=93812649844; WEIBOCN_FROM=1110006030; SUB=_2A25znA40DeRhGeNL6VYY9SjOzjmIHXVRfpJ8rDV6PUJbkdAKLWLukW1NSQiUQDfX-070Xv84el--8GVn_ZRwFkJw; SUHB=0XDl0_JoNlei04; SCF=AsNt0KRSYuyD9kMrtk_Kip0FW9SzA-2SlWcGl9I6bAifo2l-NBVm3h2TKqSzkZ3OZg8TzUCX08eMg3zKE2DVkl0.; SSOLoginState=1587052132; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174; XSRF-TOKEN=837baf'
    #cookies = 'ALF=1589592746; _T_WM=93812649844; XSRF-TOKEN=e56f0f; WEIBOCN_FROM=1110006030; SCF=AlO2RfmUpkrpNUmXXgHOT6xvadMEvjQ7kiGTc6hLslFmV7J5SYdek1kDpX3FjLp5NqAS7NpX-WUyXfnALuQ88_E.; SUB=_2A25zk7FIDeRhGeNL6VYY9SjOzjmIHXVRf98ArDV6PUJbktAKLXPDkW1NSQiUQCvHR5QYvtTTFsYbhYJE5q_39J1w; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpIrLebwvvgaLmZF4aOcdf5JpX5K-hUgL.Fo-feoB4SKqESK-2dJLoI0qLxK.L1hzL1hzLxK.L1h5L1h-LxKBLBonL1h5LxK-LBK5LBoBLxKML1h-L1K.LxK.L1-zLBKnt; SUHB=0QS5jT-J78WnUb; SSOLoginState=1587003672'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Cookie': cookies}

    # record
    fpp.write(user + ' ' + uid + ' ')

    # capture imgs from sina
    _capture_images(uid, user, headers, path, 349)

    fp.close()
    fpp.close()


if __name__ == '__main__':
    main()