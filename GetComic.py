import requests
import os
import re
from bs4 import  BeautifulSoup
import time
import urllib3
import urllib
import urllib.request
##Comic MainPage
comic_link = 'http://www.gufengmh.com/manhua/xinwangqiuwangzi/'

## Chapeters
chapter_list_link = []
chapter_dir = []
each_img_page = []

header = {
    'User-Agengt': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
    'Cookie': 'gidinf=x099980109ee0d6c7e1232437000190d741919c56878'
}

response = requests.get(comic_link, headers=header)

if response.status_code != 200:
    print ('Page Load Failed')
    exit(1)
else:
    #中文乱码编码
    soup = BeautifulSoup(response.text.encode(response.encoding), 'html.parser')
    chapter_list = soup.find('div', class_='chapter-body clearfix')
    for li in chapter_list.contents[1].find_all('li'):
        chapter_list_link.append(li.a['href'])
        chapter_dir.append(li.a.span.string)

##每一话的页面链接
for index in range(197, len(chapter_list_link)):
    if not os.path.exists('c:\\comic\\'+chapter_dir[index]):
        os.makedirs('c:\\comic\\'+chapter_dir[index])
        print ("创建文件夹: %s\n" % chapter_dir[index])
    pageRes = requests.get('http://www.gufengmh.com'+chapter_list_link[index],headers=header)
    if pageRes.status_code != 200:
        print('SubPage Load Failed')
        exit(1)
    else:
        sp = BeautifulSoup(pageRes.text.encode(pageRes.encoding), 'html.parser')
        images_scripts = sp.find_all('script')[2].contents
        img_script = sp.find_all('script')[2].contents[0]
        matchImgObj = re.match(r'.*?var chapterImages = \[(.*?)\].*?', img_script)
        matchChapterPathObj = re.match(r'.*?var chapterPath = "(.*?)".*?', img_script)
        ##获取图像名称
        imgs = re.split(',', matchImgObj.group(1))
        ##获取图像路径
        chapter_path = matchChapterPathObj.group(1)
        ##获取页码
        page_num = int((sp.span.contents[2])[:-1])

        print('下载第 %d 话，共 %d 张图 ---\n' % (index+1, page_num))

        for i in range(0, page_num):
            img_url = 'http://res.gufengmh.com/' + chapter_path + (imgs[i])[1:-1]
            img_name = 'c:\\comic\\'+chapter_dir[index]+'\\' + str(i+1) + '.jpg'

            html = requests.get(img_url, headers=header)
            with open(img_name, 'wb') as file:
                file.write(html.content)
                file.flush()
            file.close()
            ##time.sleep(1)
            print('--- 下载第 %d 张图完成 ---\n' % (i+1))
        print('第 %d 话下载完成\n' % (index+1))














