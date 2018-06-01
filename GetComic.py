import  requests
import  os
import urllib
from bs4 import  BeautifulSoup

##Comic MainPage
comic_link='http://www.gufengmh.com/manhua/xinwangqiuwangzi/'

## Chapeters
chapter_list_link=[]
chapter_dir=[]
each_img_page=[]

response=requests.get(comic_link)

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
for index in range(len(chapter_list_link)):
    if not os.path.exists('d:\\comic\\'+chapter_dir[index]):
        os.makedirs('d:\\comic\\'+chapter_dir[index])
        print ("创建文件夹: %s\n" % chapter_dir[index])
    pageRes = requests.get('http://www.gufengmh.com'+chapter_list_link[index])
    if pageRes.status_code != 200:
        print('SubPage Load Failed')
        exit(1)
    else:
        sp = BeautifulSoup(pageRes.text.encode(pageRes.encoding), 'html.parser')
        page_num=int((sp.span.contents[2])[:-1])
        ##imgage_block = sp.find('div', id='images')
        ##页码数 (1/64)
        ##page_num=int((imgage_block.p.string.partition('/')[2])[:-1])
        for i in range(1,page_num):
            each_img_page = 'http://www.gufengmh.com' + chapter_list_link[index]+'#p='+str(i)
            imgRes=requests.get(each_img_page)
            if imgRes.status_code != 200:
                print('SubImgPage Load Failed')
                exit(1)
            else:
                img_sp=BeautifulSoup(imgRes.text, 'html.parser')
                img_url=img_sp.find('div', id='images').img['src']
                urllib.urlretrieve(img_url, 'd:\\comic\\'+chapter_dir[index]+'\\'+'%s.jpg' % i)














