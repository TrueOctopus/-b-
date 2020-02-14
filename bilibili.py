import requests
import re
from bs4 import BeautifulSoup
import os
import sys
import jieba
from wordcloud import WordCloud


def get_cid(av):
    url = 'https://api.bilibili.com/x/player/pagelist?aid='+av+'&jsonp=jsonp'
    res = requests.get(url)
    cid = re.findall(r'"cid":(\d+)', str(res.content))
    if cid:
        return cid[0]
    else:
        print("未找到oid！")
        sys.exit(0)


def get_barrage(oid, aid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+oid
    res = requests.get(url)
    html = res.content
    soup = BeautifulSoup(html, features='lxml')
    barrages = soup.find_all('d')
    with open('./barrages/av'+aid+'.txt', 'w', encoding="utf-8") as f:
        for barrage in barrages:
            f.write(barrage.get_text())
            f.write('\n')
    if f:
        print("弹幕保存成功！")
    else:
        print("弹幕保存失败！")
        sys.exit(0)


def cloud_word(av):
    with open('./barrages/av'+av+'.txt', 'r', encoding='UTF-8') as f:
        words = f.read()
    if words:
        words_list = jieba.lcut(words)
        word_str = ''.join(words_list)
        word_cloud = WordCloud(font_path='msyhbd.ttc',
                               background_color='white',
                               width=1600, height=800).generate(word_str)
        word_cloud.to_file('./wordcloud/av'+av+'.png')
        print("词云生成成功！")
    else:
        print("词云生成失败！")
        sys.exit(0)


if __name__ == "__main__":
    os.makedirs('./barrages/', exist_ok=True)
    os.makedirs('./wordcloud/', exist_ok=True)
    print('请输入视频av号：AV')
    av = input()
    oid = get_cid(av)
    get_barrage(oid, av)
    cloud_word(av)
