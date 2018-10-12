import urllib.request
from bs4 import BeautifulSoup
from urllib import error
import os

novel_url = "http://www.biqukan.com/2_2675/"   #小说地址
novel_base_url = "http://www.biqukan.com/"     #小说首页地址，拼接使用
save_dir = "Novel/"                            #下载小说的存放目录

#获取所有章节的url信息
def get_download_url():
    # get
    download_req = urllib.request.Request(novel_url)
    # open
    download_res = urllib.request.urlopen(download_req,timeout=20)
    # read
    download_content = download_res.read()
    # parse
    download_soup = BeautifulSoup(download_content,"html.parser")

    listmain = download_soup.find_all(attrs={'class':'listmain'})
    a_list = []

    for i in listmain:
        # 把非a标签无关的过滤掉
        # if 'a' not in str(i), continue next loop.
        if 'a' not in str(i):
            continue
        for d in i.findAll('a'):
            a_list.append(d)
    #result_list = a_list[12:]
    # return result_list
    return a_list

#获取正文内容并且开始下载
# c = return_list
def get_download_content(c):
    download_url = novel_base_url + c.attrs.get('href')
    download_name = c.string
    download_req = urllib.request.Request(download_url)
    download_response = urllib.request.urlopen(download_req,timeout=20)
    download_content = download_response.read()
    download_soup = BeautifulSoup(download_content,'html.parser')

    showtxt = download_soup.find_all(attrs={'class':'showtxt'})
    for txt in showtxt:
        save_novel(txt,save_dir+download_name+".txt")



#get_text()方法：用来获取标签里面的文本内容，在括号里面加"strip=True"可以去除文本前后多余的空格
#保存小说到本地
def save_novel(txt,path):
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        with open(path,"w",encoding="utf-8") as f:
            f.write(txt.get_text(strip=True))
    except (error.HTTPError,OSError) as e:
        print(str(e))
    else:
        print('download success :'+path)


if __name__ == '__main__':
    novel_list = get_download_url()
    for content in novel_list:
        get_download_content(content)


