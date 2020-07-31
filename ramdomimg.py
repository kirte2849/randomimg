import requests
from lxml import etree
import random
import uuid
import os

def get_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid

start_url = 'http://www.netbian.com/dongman/'
all_pages_num = 12 #max is 142 now
all_pages = [f'http://www.netbian.com/dongman/index_{i + 2}.htm' for i in range(all_pages_num)]
all_pages.append(start_url)

def repaire_img(url):
    if 'newc' in url:
        return url
    url = url.replace('small', '')
    url = url[:-14]
    url += '.jpg'
    return url

def get_next_img():
    try:
        this_page = random.choice(all_pages)
        response = requests.get(this_page)
        response.encoding = 'gbk'
        html = etree.HTML(response.text)
        li = list(range(18))
        li.remove(2)
        num = random.choice(li) + 1
        a = html.xpath(f"//body//li[{num}]")[0][0]
        img, b = a.getchildren()

        img_url = repaire_img(img.attrib['src'])
        discription = b.text
        return this_page, img_url, discription
    except:
        return get_next_img()

root = 'imgs/'
def down_img(img_url):
    fname = get_uuid() + '.jpg'
    with open(root + fname, 'wb') as f:
        f.write(requests.get(img_url).content)
    return root + fname

# ipt = ''
# while ipt != 'q':
#     this_page, img_url, discription = get_next_img()
#
#     print(f'this_page: {this_page}\ndiscripton: {discription}\nimg_url: {img_url}')
#
#     fname = get_uuid() + '.jpg'
#     with open(fname, 'wb') as f:
#         f.write(requests.get(img_url).content)
#
#
#     os.system(f'start {fname}')
#     ipt = input('输入任意键下一个，输入q退出')
