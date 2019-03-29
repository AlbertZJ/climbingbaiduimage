'''
Created on 2019年3月15日

@author: AlbertZJ
'''
import os
import re
import requests
import urllib.parse


# 获取动态页面返回的文本
def get_page_html(page_url):
    headers = {
        'Referer': r'https://image.baidu.com/search/index?tn=baiduimage',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36 115Browser/6.0.3',
        'Connection': 'keep-alive'
    }
    '''
    urllib.request.Request(url, data=None, headers={}, method=None)
    使用request（）来包装请求，再通过urlopen（）获取页面。
    
    用来包装头部的数据：
    
    -         User-Agent ：这个头部可以携带如下几条信息：浏览器名和版本号、操作系统名和版本号、默认语言
    
    -         Referer：可以用来防止盗链，有一些网站图片显示来源http://***.com，就是检查Referer来鉴定的
    
    -         Connection：表示连接状态，记录Session的状态。
    '''
    try:
        r = requests.get(page_url, headers=headers)
        r.raise_for_status()
        #获取正确的编码格式
        r.encoding = r.apparent_encoding   
        return r.text                                 
    except Exception as e:
        print(e)

# 从文本中提取出真实图片地址
def parse_result(text):
    url_real = re.findall('"thumbURL":"(.*?)",', text)
    return url_real

# 获取图片的content
def get_image_content(url_real):
    headers = {
        'Referer': url_real,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36 115Browser/6.0.3',
        'Connection': 'keep-alive'
    }
    try:
        r = requests.get(url_real, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  #获取正确的编码格式
        return r.content
    except Exception as e:
        print(e)
        
# 将图片的content写入文件
def save_pic(url_real, content):    
        root = r'F://image//'
        path = root + url_real.split('/')[-1]
        if not os.path.exists(root):  #路径存在返回True，不存在就创建目录
            os.mkdir(root)
            print("目录已创建")
        if not os.path.exists(path):  #避免重复下载
            with open(path, 'wb') as f:
                f.write(content)
                print('图片{}下载成功，存放在{}下'.format(url_real, path))             
        else:
            pass
            
# 主函数
def main():
    while(True):
        try: 
            keyword = str(input('请输入你想要爬取的图片的关键字: '))
            break
        except Exception as e:
            print(e)
            print("请正确输入")
    keyword_quote = urllib.parse.quote(keyword)
    while (True):
        try:
            imageNumber = int(input("请输入要爬取的图片数量: "))
            break
        except Exception as e:
            print(e)
            print("请输入数字！")                        
    for i in range(imageNumber):
        #向服务器发送请求的地址
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={}&rn={}&gsm=1e&1541136876386='.format(
            keyword_quote, keyword_quote, i+1)  #设置每页图片数量
        html = get_page_html(url)
        real_urls = parse_result(html)
        for i in  real_urls:
            content = get_image_content(i)
            save_pic(i, content)
    print("图片下载完成！")

if __name__ == '__main__':
    main()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        