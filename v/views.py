# coding=utf-8
import urllib

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse
from bs4 import BeautifulSoup
from v.data import *
import requests
import js2py
import json
import time
import re
import os





# from urllib.request import urlretrieve
# from pypinyin import lazy_pinyin
# from Crypto.Cipher import AES
# import base64
# import codecs


# Create your views here.



def get_background(request):
    try:
        background = request.session["background"]
    except:
        background = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/169/169-bigskin-4.jpg'
    background_img = background
    return background_img


def home(request):
    result = ""
    background_img = get_background(request)
    if request.method == "POST":
        url_p = request.POST.get('url')
        password = request.POST.get('password')
        request.session['password'] = password
        if str(password) in password_list:
            request.session['url'] = url_p
            if not url_p:
                return render(request, 'home.html', locals())
            try:
                title = get_title(url_p)
            except:
                title = "ToolTool带你探索新世界"
            request.session['title'] = title
            return redirect('v:movie')
        else:
            result = "解析密码错误,谢谢您对我们的支持"
            return render(request, 'home.html', locals())
    return render(request, 'home.html', locals())


def vip_user(func):
    def wrapper(request, *args, **kwargs):
        password = request.session.get('password')
        if password and str(password) in password_list:
            setattr(request, 'user', password)
            result = func(request, *args, **kwargs)
            return result
        else:
            background_img = get_background(request)
            result = "本站所有内容，请输入解析密码后查看使用"
            return render(request, 'home.html', locals())
    return wrapper


def get_title(url):
    resp = requests.get(url, headers=headers)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    head = soup.head
    title = head.find("title").text
    return title


@vip_user
def movie(request):
    background_img = get_background(request)
    if request.method == "POST":
        url_p = request.POST.get('url')
        request.session['url'] = url_p
        try:
            title = get_title(url_p)
        except:
            title = "ToolTool带你探索新世界"
        request.session['title'] = title
        return redirect('v:movie')
    url = request.session.get('url')
    title = request.session.get('title')
    p = url.split('/')
    if p[0] == "http:":
        url = "http://api.6uzi.com/?url=" + str(url)
    else:
        url = "https://api.6uzi.com/?url=" + str(url)
    if p[2] in list_url and len(p) > 3:
        url = url
    else:
        url = " "
    return render(request, 'v.html', locals())


def set_background(request):
    page = None
    list_bg = []
    background_img = get_background(request)
    if request.method == "GET":
        page = request.GET.get('page')
        bg = request.GET.get('set')
        if bg:
            if page:
                page = int(page)
            else:
                page = 1
            request.session["background"] = bg
            return redirect('/vip/background?page=%d' % page)
        else:
            list_bg = background_list
    else:
        list_bg = background_list

    # 设置分页,页码,分页内容
    if page:
        page = int(page)
    else:
        page = 1
    paginator = Paginator(list_bg, 12)
    page_num = paginator.num_pages
    if page > page_num:
        page = page_num
    page_bg = paginator.page(page)
    if page_bg.has_next():
        page_next = page + 1
    else:
        page_next = page
    if page_bg.has_previous():
        page_pre = page - 1
    else:
        page_pre = page
    page_num_1 = page_num - 1
    page_num_2 = page_num - 2
    page_num_3 = page_num - 3
    page_num_4 = page_num - 4
    page_2 = page - 2
    page__2 = page + 2
    return render(request, 'background.html', locals())


def help_page(request):
    photo = "wx1"
    background_img = get_background(request)
    if request.method == "POST":
        photo = request.POST.get('photo')
    return render(request, 'help.html', locals())


class QQmusic:
    def __init__(self):
        self.sl = []
        self.musicList = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                                      'AppleWebKit/537.36 (KHTML,like Gecko) '
                                      'Chrome/74.0.3729.131 Safari/537.36'}

    # 获取页面
    def getPage(self, url, headers):
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        return res

    # 获取音乐songmid
    def getSongmid(self, page, search):
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p={page}&n=6&w={search}'
        # 搜索音乐
        res = self.getPage(url, headers=self.headers)
        html = res.text
        html = html[9:]
        html = html[:-1]
        # 获取songmid
        js = json.loads(html)
        songlist = js['data']['song']['list']
        for song in songlist:
            songmid = song['songmid']
            name = song['songname']
            if len(name) > 11:
                name = name[0:11]
            peoplename = song["singer"][0]['name']
            if len(peoplename) > 11:
                peoplename = peoplename[0:11]
            self.sl.append((name, songmid, peoplename))

    # 获取音乐资源，guid是登录后才能获取，nin也是
    def getVkey(self):
        uin = 264
        guid = 7107896008
        for s in self.sl:
            # 获取vkey,purl
            name = s[0]
            songmid = s[1]
            peoplename = s[2]
            keyUrl = 'https://u.y.qq.com/cgi-bin/musicu.fcg?&data={"req":{"param":{"guid":" %s"}},"req_0":' \
                     '{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":' \
                     '["%s"],"uin":"%s"}},"comm":{"uin":%s}}' % (guid, guid, songmid, uin, uin)
            res = self.getPage(keyUrl, headers=self.headers)
            html = res.text
            keyjs = json.loads(html)
            purl = keyjs['req_0']['data']['midurlinfo'][0]['purl']
            # 拼凑资源url
            url = 'http://dl.stream.qqmusic.qq.com/' + purl
            self.musicList.append((name, peoplename, url))
        music_list = []
        for i in self.musicList:
            temp = {"song_name": i[0], "singer_name": i[1], "url": i[2]}
            music_list.append(temp)
        return music_list


def download_url(url):
    cookies = {"kg_mid": "1e9dafb57510c5cd330a4db122cfd586;",
               "kg_dfid": "0Pe8mG4JbpeZ0gcRbM3r3DI6;",
               "kg_dfid_collect": "d41d8cd98f00b204e9800998ecf8427e;",
               "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": "1580985255,1580993682;",
               "kg_mid_temp": "1e9dafb57510c5cd330a4db122cfd586;",
               "Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d": "1580995447"}
    resp = requests.get(url, headers=headers, cookies=cookies)
    html = resp.content.decode('utf8')
    url_re = re.findall(r"\"play_backup_url\":\"(.+?)mp3", html)
    url_f = ""
    for i in url_re[-1]:
        if i == "\\":
            pass
        else:
            url_f = url_f + i
    url_f = url_f + "mp3"
    return url_f


def kg_music(song_name, page):
    """搜索歌曲"""
    search_url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery112405132987859127838_{}&page" \
                 "={}&pagesize=6&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_fil" \
                 "ter=0&_={}&keyword={}".format(str(int(time.time() * 1000)), page, str(int(time.time() * 1000)),
                                                song_name)
    obj = requests.get(search_url)
    start = re.search("jQuery\d+_\d+\(?", obj.text)
    data = json.loads(obj.text.strip().lstrip(start.group()).rstrip(")"))
    song_list = data['data']['lists']
    music_list = []
    for i in song_list:
        song_name = str(i['SongName']).replace('<em>', '').replace('</em>', '')
        singer_name = str(i['SingerName']).replace('<em>', '').replace('</em>', '')
        url_p = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&' \
                'callback=jQuery1910212680783679835_1555073815772&hash=' \
                + str(i['FileHash']) + '&album_id=' + str(i['AlbumID'])
        try:
            url = download_url(url_p)
        except:
            time.sleep(1)
            url = download_url(url_p)
        temp = {"song_name": song_name, "singer_name": singer_name, "url": url}
        music_list.append(temp)
    return music_list


@vip_user
def music(request):
    background_img = get_background(request)
    if request.method == "GET":
        search = request.GET.get('search')
        page = request.GET.get('page')
        search_id = request.GET.get("search_id")
        if not search:
            return render(request, 'music_search.html', locals())
        if not search:
            pass
        if page:
            page = int(page)
        else:
            page = 1
        page_next = page + 1
        if page > 1:
            page_pre = page - 1
        else:
            page_pre = page
        page_2 = page - 2
        page__2 = page + 2
        if search_id == "kg":
            musics_list = kg_music(str(search), str(page))
            return render(request, 'music.html', locals())
        elif search_id == "wyy":
            return render(request, 'music_search.html', locals())
        else:
            QQ = QQmusic()
            QQ.getSongmid(str(page), str(search))
            musics_list = QQ.getVkey()
            return render(request, 'music.html', locals())
    else:
        return render(request, 'music_search.html', locals())


@vip_user
def music_search(request):
    background_img = get_background(request)
    if request.method == "POST":
        search = request.POST.get('search')
        music_id = request.POST.get('search_id')
        if not search:
            return render(request, 'music_search.html', locals())
        if music_id == "qq":
            return redirect('/vip/music?page=1&search=%s&search_id=%s' % (search, music_id))
        elif music_id == "wyy":
            return redirect('/vip/music?page=1&search=%s&search_id=%s' % (search, music_id))
        elif music_id == "kg":
            return redirect('/vip/music?page=1&search=%s&search_id=%s' % (search, music_id))
        else:
            return redirect('/vip/music?page=1&search=%s' % search)
    return render(request, 'music_search.html', locals())


def movie_search_app(search):
    url = "http://www.k5.cc/movie/search/"
    session = requests.session()
    req = session.get(url)
    FormData = {
        "search_typeid": "1",
        "skey": str(search),
        "Input": "搜索"
    }
    resp = session.post(url, headers=headers, data=FormData)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    div = body.find("div", {"class": "clearfix noborder"})
    movies_list = []
    try:
        movies = div.find_all("a", {"target": "_blank"})
        for movie in movies:
            if movie.get("href")[1:3] in ["mo", "ju", "dm", "zy"]:
                movie_name = movie.get("title")
                movie_url = "/vip/movie/" + str(movie.get("href")).split("/")[-1]
                movie_img = "http:" + movie.find("img").get("_src")
                name_len = len(movie_name)
                temp = {"movie_name": movie_name, "movie_url": movie_url, "movie_img": movie_img, "len": name_len}
                movies_list.append(temp)
    except:
        pass
    return movies_list


def movie_page_app(movie_id):
    url = "http://www.k5.cc/movie/" + str(movie_id)
    session = requests.session()
    req = session.get(url)
    resp = session.get(url, headers=headers)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    div_1 = body.find("div", {"class": "s_block1"})
    a_all = div_1.find_all("a")
    for a in a_all:
        href = a.get("href")
        if href in ["/movie/list", "/ju/list", "/dm/list", "/zy/list"]:
            div = body.find("div", {"id": "minfo"})
            div_img = div.find("div", {"class": "img"})
            spans = div.find_all("span", {"class": "span_block"})
            img = "http://pic.616pic.com/ys_bnew_img/00/11/69/j2AjnHspwT.jpg"
            movie_img = "http://pic.616pic.com/ys_bnew_img/00/11/69/j2AjnHspwT.jpg"
            movie_name = "Tool Tool"
            movie_type = " "
            movie_area = " "
            movie_language = " "
            movie_director = " "
            movie_time = " "
            movie_long = " "
            movie_score = " "
            movie_content = " "
            x = 0
            for i in div_img:
                if x == 1:
                    img = i
                x = x + 1
            for span in spans:
                if span.find("span").text == "类型：":
                    for i in span.text[4:]:
                        if i == "\n":
                            movie_type = movie_type + " "
                        elif i == " ":
                            pass
                        else:
                            movie_type = movie_type + i
                elif span.find("span").text == "地区：":
                    for i in span.text[4:]:
                        if i in [" ", "\n"]:
                            pass
                        else:
                            movie_area = movie_area + i
                elif span.find("span").text == "语言：":
                    for i in span.text[4:]:
                        if i in [" ", "\n"]:
                            pass
                        else:
                            movie_language = movie_language + i
                elif span.find("span").text == "导演：":
                    for i in span.text[4:]:
                        if i in [" ", "\n"]:
                            pass
                        else:
                            movie_director = movie_director + i
                elif span.find("span").text == "上映日期：":
                    for i in span.text[5:]:
                        if i in [" ", "\n"]:
                            pass
                        else:
                            movie_time = movie_time + i
                elif span.find("span").text == "片长：":
                    for i in span.text[4:]:
                        if i in [" ", "\n"]:
                            pass
                        else:
                            movie_long = movie_long + i
                else:
                    pass
            try:
                movie_img = "http:" + img.get("src")
                movie_name = img.get("title")
            except:
                pass
            try:
                p = div.find("p", {"id": "movie_content_all"}).text[5:]
                if len(p) > 110:
                    p = p[0:110] + "......"
                for i in p:
                    if i == "\n":
                        pass
                    else:
                        movie_content = movie_content + i
            except:
                pass
            try:
                div_sc = div.find("div", {"style": "float:left; margin-right:10px;"})
                for i in div_sc.text[5:]:
                    if i in [" ", "\n"]:
                        pass
                    else:
                        movie_score = movie_score + i
            except:
                pass
            demp = {
                "movie_name": movie_name,
                "movie_img": movie_img,
                "movie_type": movie_type,
                "movie_area": movie_area,
                "movie_language": movie_language,
                "movie_director": movie_director,
                "movie_time": movie_time,
                "movie_long": movie_long,
                "movie_score": movie_score,
                "movie_content": movie_content
            }
            return demp
        else:
            pass
    return redirect('/vip/movie/home')


def movie_watch_app(movie_id):
    url = "http://www.k5.cc/movie/" + str(movie_id) + "/play/f-2"
    session = requests.session()
    req = session.get(url)
    resp = session.get(url, headers=headers)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    plays = soup.find_all("a")
    plays_list = []
    for play in plays:
        play_name = play.text
        play_url = "/vip/movie/" + str(play.get("href")).split("/")[-2] + "/" + \
                   str(play.get("href")).split("/")[-1]
        temp = {"play_name": play_name, "play_url": play_url}
        if temp in plays_list:
            pass
        else:
            plays_list.insert(0, temp)
    return plays_list


def movie_download_app(movie_id, type):
    url = "http://www.k5.cc/movie/" + str(movie_id) + "/bd-2"
    session = requests.session()
    req = session.get(url)
    resp = session.get(url, headers=headers)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    plays = soup.find_all("li")
    local_list = []
    thunder_list = []
    for play in plays:
        try:
            all_a = play.find_all("a")
            play_name = None
            local_play_url = " "
            thunder_play_url = " "
            for a in all_a:
                if a.text == "本地下载":
                    local_play_url = str(a.get("href"))
                elif a.text == "迅雷下载":
                    thunder_play_url = str(a.get("href"))
                elif a.text in ["", " ", "批量复制下载链接", "迅雷批量下载", "无法下载，请看教程"]:
                    pass
                else:
                    play_name = a.text
            if play_name:
                local_temp = {"play_name": play_name, "play_url": local_play_url}
                thunder_temp = {"play_name": play_name, "play_url": thunder_play_url}
                if local_temp in local_list:
                    pass
                else:
                    local_list.insert(0, local_temp)
                if thunder_temp in thunder_list:
                    pass
                else:
                    thunder_list.insert(0, thunder_temp)
        except:
            pass
    if type == "local":
        return local_list
    elif type == "thunder":
        return thunder_list
    else:
        return movie_watch_app(movie_id)


def movie_play_app(movie_id, play_id):
    url = "http://www.k5.cc/movie/" + str(movie_id) + "/play-" + str(play_id)
    session = requests.session()
    req = session.get(url)
    resp = session.get(url, headers=headers)
    html = resp.content.decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    play_url = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_" \
               "10000&sec=1581153694655&di=91a487a8dbf7f87ef3c09aeee26d3ec0" \
               "&imgtype=0&src=http%3A%2F%2Fhbimg.huabanimg.com%2Feaa7f1627" \
               "e850d56064be80d5723bafe386817d31989c-gJHcxy_fw658"
    try:
        iframe = body.find("iframe")
        play_url = iframe.get("src")
    except:
        pass
    return play_url


@vip_user
def movie_search(request):
    background_img = get_background(request)
    try:
        movies_list = request.session["movies_list"]
        movie_search_name = "_" + request.session["movies_search_name"]
        if not movie_search_name:
            movie_search_name = " "
        page = request.GET.get("page")
        if page:
            page = int(page)
        else:
            page = 1
        paginator = Paginator(movies_list, 8)
        page_num = paginator.num_pages
        if page > page_num:
            page = page_num
        movie_list = paginator.page(page)
        if movie_list.has_next():
            page_next = page + 1
        else:
            page_next = page
        if movie_list.has_previous():
            page_pre = page - 1
        else:
            page_pre = page
        page_num_1 = page_num - 1
        page_num_2 = page_num - 2
        movies_list_1 = movies_list[8*page-8:8*page-4]
        movies_list_2 = movies_list[8*page-4:8*page]
        return render(request, 'movie_search.html', locals())
    except:
        return render(request, 'movie_home.html', locals())


@vip_user
def movie_home(request):
    background_img = get_background(request)
    if request.method == "POST":
        movie_name = request.POST.get("search")
        if movie_name:
            movies_list = movie_search_app(movie_name)
            request.session["movies_list"] = movies_list
            request.session["movies_search_name"] = movie_name
            return redirect('/vip/movie/search')
    return render(request, 'movie_home.html', locals())


@vip_user
def movie_page(request, movie_id):
    background_img = get_background(request)
    try:
        type = request.GET.get("type")
        if type:
            if type == "local":
                plays_list = movie_download_app(str(movie_id), str(type))
            elif type == "thunder":
                plays_list = movie_download_app(str(movie_id), str(type))
            elif type == "play":
                plays_list = movie_watch_app(str(movie_id))
            else:
                plays_list = movie_watch_app(str(movie_id))
        else:
            plays_list = movie_watch_app(str(movie_id))
        temp = movie_page_app(str(movie_id))
        movie_name = temp["movie_name"]
        movie_img = temp["movie_img"]
        movie_type = temp["movie_type"]
        movie_area = temp["movie_area"]
        movie_language = temp["movie_language"]
        movie_director = temp["movie_director"]
        movie_time = temp["movie_time"]
        movie_long = temp["movie_long"]
        movie_score = temp["movie_score"]
        movie_content = temp["movie_content"]
        return render(request, 'movie_page.html', locals())
    except:
        return render(request, 'movie_home.html', locals())


@vip_user
def movie_play(request, movie_id, play_id):
    background_img = get_background(request)
    try:
        play_url = movie_play_app(movie_id, play_id)
    except:
        return render(request, 'movie_home.html', locals())
    return render(request, 'movie_play.html', locals())


class Translate:
    def __init__(self, query):
        self.query = query
        self.session = requests.session()
        self.home_url = 'https://www.baidu.com'
        self.root_url = "https://fanyi.baidu.com/"
        self.type_url = "https://fanyi.baidu.com/langdetect"
        self.trans_url = "https://fanyi.baidu.com/v2transapi"
        self.get_url = f'http://tooltool.club/vip/baidu/translate?query={query}'

    def get_token_gtk(self):
        """获取token和gtk(用于合成Sign)"""
        self.session.get(self.root_url)
        resp = self.session.get(self.root_url)
        html_str = resp.content.decode()
        token = re.findall(r"token: '(.*?)'", html_str)[0]
        gtk = re.findall(r"window.gtk = '(.*?)'", html_str)[0]
        return token, gtk

    def get_sign(self, gtk):
        """生成sign"""
        context = js2py.EvalJs()
        with open('webtrans.js', encoding='utf8') as f:
            js_data = f.read()
            js_data = re.sub("window\[l\]", '"' + gtk + '"', js_data)
            context.execute(js_data)
        sign = context.e(self.query)
        return sign


def translate(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            trans = Translate(query)
            token, gtk = trans.get_token_gtk()
            sign = trans.get_sign(gtk)
            data = {
                "query": query,
                "simple_means_flag": 3,
                "sign": sign,
                "token": token
            }
            return JsonResponse(data)
        else:
            data = {
                "query": '',
                "simple_means_flag": 3,
                "sign": '',
                "token": ''
            }
            return JsonResponse(data)


url_datas = []


def data_post(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        url_datas.append(url)
    return JsonResponse({'data': url_datas})






