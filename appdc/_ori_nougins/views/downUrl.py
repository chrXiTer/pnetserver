#coding: utf-8
import requests
import re
import os
import urllib
import json
import shutil

def getHtml(url):
    req = requests.get(url, stream = True, timeout = 3)
    req.raise_for_status()    # 失败请求(非200响应)则抛出异常
    req.encoding = req.apparent_encoding
    return req.text

def getFile(url, filename):
    try:
        req = requests.get(url, stream = True, timeout = 60)
    except:
        return False
    if req.status_code == 200:
        with open(filename, "wb") as fd:
            #req.raw.decode_content = True
            #shutil.copyfileobj(req.raw, fd)
            fd.write(req.content)
            return True
    return False


def getImgUrlFromHtml(html):
    imgDic = {}
    n = [1]
    def func(m):
        url = m.group(1)
        n2 = imgDic.get(url)
        if not n2 :
            n[0] = n[0] + 1
            imgDic[url] = n[0]
            n2 = n[0]
        url2 = "imge" + str(n2)
        return 'src="' + url2 + '"'

    reg = r'data-src="(.+?)"' 
    imgre = re.compile(reg)
    html2 = imgre.sub(func, html)
    return imgDic, html2

def getTitleFromHtml(html):
    reg = r'<title>([\s\S]*?)<\/title>'
    titleRe = re.compile(reg)
    result = titleRe.search(html)
    g = result.group(1) 
    return g.strip()



def downUrl(url, dirName):  
    html = getHtml(url)
    imgUrlList, html2 = getImgUrlFromHtml(html)
    with open(dirName + "/html.html", "w") as fd:
        fd.write(html2)
    info = {}
    info['title'] = getTitleFromHtml(html) or "123"
    infoStr = json.dumps(info, ensure_ascii=False, indent=4)
    with open(dirName + "/info.json", "w") as fd:
        fd.write(infoStr)
    for url in imgUrlList:
        imgName = dirName + "/imge" + str(imgUrlList[url])
        getFile(url, imgName)
    
    

if __name__=='__main__':
    #url = "https://mp.weixin.qq.com/s/0ccts-hT7Up6WRhXnVPVKw"
    #url = "https://mp.weixin.qq.com/s/RtUynDuUWmSFXc7KznxLCw"
    #
    url = "https://mp.weixin.qq.com/s/IBIN8o3YIU-DztnLQ3SVZw"
    path = urllib.parse.urlparse(url).path
    dirName = path.strip("/").replace("/", "_")
    if not os.path.exists("bak"):
        os.mkdir("bak")
    if os.path.exists(dirName):
        shutil.move(dirName, "bak/" + dirName)
    os.mkdir(dirName)
    downUrl(url, dirName) 
    
    