# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os
import re

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)

def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

def addDiarylist(date, soup):
    ne = soup.new_tag('li')
    new = soup.new_tag('a')
    new.string="20%s.%s.%s" % (date[:2], date[2:4], date[4:])
    ne['id'] = date
    ne.append(new)
    soup.find('div', class_='diary-list').find('ul').insert(0, ne)

def contentFile(path, date, memidx, soup):
    content = str(soup.find('div', class_='entry__body'))
    content = content.replace('./images', './images/content')
    content = content.replace('<div class="entry__body wysiwyg">\n', '')
    ret = '<img src="./images/diary/%d_top.png"/>\n' % memidx
    ret += content[:-6]

    outname = path + '/content/%s-nnw%d' % (date, memidx)
    ff = open(outname, 'w', encoding='utf-8')
    ff.write(ret)

def main():
    nameMem = [None, "大吾", "流星", "米七", "恭平", "長尾", "丈君", "大橋"]
    directory = os.fsencode('./diary-resource')
    dir = './diary-resource/'
    fli = []
    fli.append(None)

    for i in range(1, 8):
        n = './diarya%d.html' % i
        d = open(n, 'r', encoding='utf-8')
        h = d.read()
        sd = BeautifulSoup(h, "html.parser")
        fli.append(sd)
        d.close()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".html"): 
            li = filename.split(' ')
            date = li[0]
            memidx = nameMem.index(li[1][:2])

            # new file
            filepath = dir + filename
            f = open(filepath, 'r', encoding="utf-8")
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")

            contentFile('.', date, memidx, soup)
            # content = str(soup.find('div', class_='entry__body'))
            # content = content.replace('./images', './images/content')
            # content = content.replace('<div class="entry__body wysiwyg">\n', '')
            # ret = '<img src="./images/diary/%d_top.png"/>\n' % memidx
            # ret += content[:-6]

            # outname = './content/%s-nnw%d' % (date, memidx)
            # ff = open(outname, 'w', encoding='utf-8')
            # ff.write(ret)

            # add list
            addDiarylist(date, fli[memidx])
            # ne = soup.new_tag('li')
            # new = soup.new_tag('a')
            # new.string="20%s.%s.%s" % (date[:2], date[2:4], date[4:])
            # ne['id'] = date
            # ne.append(new)
            # fli[memidx].find('div', class_='diary-list').find('ul').insert(0, ne)

    for i in range(1, 8):
        n = './diarya%d.html' % i
        d = open(n, 'w', encoding='utf-8')
        d.write(fli[i].prettify(indent_width=4))      
        d.close()

if __name__ == '__main__':
    main()