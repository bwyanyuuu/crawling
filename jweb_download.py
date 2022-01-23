# -*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import time
import os

# 儲存路徑
path = "../johnny's web"

# 預定義
nameMem = [None, "大吾", "流星", "米七", "恭平", "長尾", "丈君", "大橋"]

def getHtml(url, headers):
    req = urllib.request.Request(url, headers = headers)
    page = urllib.request.urlopen(req)
    html = page.read().decode('UTF-8')
    return html

def getDiary(memidx, url, headers):
    # 得到網頁本體
    html = getHtml(url, headers)
    if html == None:
        print("Something Wrong! Check Cookie!")
    soup = BeautifulSoup(html, "html.parser")

    # 判斷此 post 是否有下載過
    content = soup.find(class_="entry__date")
    day = content.text.split(" ")[0].split(".")
    day = [int(d) for d in day]
    filename = "%s/%02d%02d%02d %s.html" % (path, day[0] % 100, day[1], day[2], nameMem[memidx])
    if os.path.isfile(filename):
        print(filename + " already exist!")
        return
    else:
        print(filename + " downloading!")

    # 下載日記中的圖片
    content = soup.find(class_="entry__body")
    img = content.find_all("img")
    for i in img:
        imgurl = "https://www.johnnys-web.com" + i['src']
        imgName = path + "/img" + i['src'][i['src'].rfind('/'):]
        imgfile = urllib.request.urlretrieve(imgurl, imgName)
        
    # 更改網頁 static 檔案路徑到本地
    # 需要創建三個資料夾，並把常駐的檔案下載下來放進去
    content = soup.find_all("link")
    for c in content:
        if c['rel'][0] == "stylesheet":
            html = html.replace(c['href'][:c['href'].rfind("/")], "./css")
        else:
            html = html.replace(c['href'][:c['href'].rfind("/")], "./img")
    content = soup.find_all("img")
    for i in content:
        html = html.replace(i['src'][:i['src'].rfind("/")], "./img")
    content = soup.find_all("script")
    for i in content:
        try:
            html = html.replace(i['src'][:i['src'].rfind("/")], "./js")
        except:
            pass
    # imgFolder = img[0]['src'][:img[0]['src'].rfind('/')]
    # html = re.sub(imgFolder, "./img", html)

    # 儲存網頁
    fd = open(filename, "w", encoding="UTF-8")
    fd.write(html)
    fd.close()

def main():
    # header 填入自己的 cookie
    userAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36 Edg/97.0.1072.69"
    cookies = "_gid=GA1.2.1765809759.1642683819; 2982884DD3255EBE=4c80e77ebd806af72a1790dee5b0120366c46a07; S5SI=vb4uci142qkfn8u0ljqo8vj8ndlkop9u; _gat_UA-138599890-11=1; _ga_HSEHV5RVJR=GS1.1.1642923767.7.0.1642923767.0; _ga=GA1.1.562254130.1641033865"
    headers = {'User-Agent': userAgent, 'Cookie': cookies}

    # 掃所有成員的日記
    for i in range(1, 8):
        url = "https://www.johnnys-web.com/s/jwb/diary/766/list?ct=%s" % i
        getDiary(i, url, headers)
        time.sleep(2)

if __name__ == '__main__':
    main()
