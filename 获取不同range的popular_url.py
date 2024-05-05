import requests
from bs4 import BeautifulSoup
import re
import time

def get_download_link(url):

    cont_id = url.split("_")[-1]

    #获取请求地址
    video_status_url = f"https://www.pearvideo.com/videoStatus.jsp?contId={cont_id}&mrd=0.6337344032061352"



    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        ,"Referer": url
    }

    resp = requests.get(video_status_url, headers=headers)


    #根据原始url和请求内容构造down_load_link

    hd_foreID = resp.json()["videoInfo"]["videos"]["srcUrl"].split("-")[1]
    time_id = resp.json()["videoInfo"]["videos"]["srcUrl"].split("/")[-2]

    down_load_link = f"https://video.pearvideo.com/mp4/short/{time_id}/cont-{cont_id}-{hd_foreID}-hd.mp4"


    #get video_name from url
    raw_resp = requests.get(url)
    obj = re.compile(r'Description.*?<title>(?P<name>.*?)</title>',re.S)
    results = obj.finditer(raw_resp.text)
    #把名字和down_load_link的content黏起来
    for result in results:
        name = result.group("name")
        #获得video_resp
        video_resp = requests.get(down_load_link)
        with open(f"{name}.mp4",mode="wb") as f:
            f.write(video_resp.content)

def get_top_urldic(popular_url):
    # heards = {
    #     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    #     ,"Referer": "https://www.pearvideo.com/popular"
    # }
    resp = requests.get(popular_url)
    popular_page = BeautifulSoup(resp.text, "html.parser")
    # 解决一个抽象问题，class 匹配错误
    tops_list_rembd = popular_page.find_all("a", class_="popularembd actplay")
    tops_list_wrong = popular_page.find_all("a", class_="actplay")
    for rembd in tops_list_rembd:
        tops_list_wrong.remove(rembd)
    tops_list = tops_list_wrong # 正确的tops_url
    top_name_list  = popular_page.find_all("h2",class_="popularem-title")  #top_name列表
    dic = {
        "top_name":[],
        "top_url":[]
    }


    for top_name in top_name_list:

        dic["top_name"].append(top_name.text)
    for top in tops_list:
        rear_url = top.get("href")
        dic["top_url"].append(f"https://www.pearvideo.com/{rear_url}")
    return dic



# url = "https://www.pearvideo.com/popular_loading.jsp?reqType=41&categoryId=&start=29&sort=30&mrd=0.9379928353440619"

#
# resp  = requests.get(url)
#
# print(resp.text)



for i in range(10):
    popular_url = f"https://www.pearvideo.com/popular_loading.jsp?reqType=41&categoryId=&start={10*(i+1)-1}&sort={10*(i+1)}&mrd=0.42719016015674915"
    url_dic = get_top_urldic(popular_url)
    url_list = url_dic["top_url"]
    for url in url_list:
        get_download_link(url)
        time.sleep(1)