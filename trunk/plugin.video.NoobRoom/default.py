import json
import urllib
import urllib2
import re
import sys
import cookielib
import os
import StringIO
import gzip
import time
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import xbmcaddon
import xbmcplugin
import xbmcgui
from xml.dom.minidom import Document
import datetime


addon_id = "plugin.video.NoobRoom"
ADDON = __settings__ = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
tvfilename = xbmc.translatePath(os.path.join(home, 'resources', 'tvshow.xml'))
noobroomlogo = xbmc.translatePath(os.path.join(home, 'logo.png'))
cookie_path = os.path.join(datapath, 'cookies')
cookiefile = os.path.join(cookie_path, "cookiejar.lwp")
cj = None
authcode = ADDON.getSetting('authcode')
reg_list = ["15", "12", "13", "14"]
if len(authcode) > 0 and authcode != "0":
    location = reg_list[int(ADDON.getSetting('region'))]
    isHD = "1"
else:
    isHD = "0"
    location = reg_list[0]
if ADDON.getSetting('use-hd') != 'true':
    isHD = "0"

strUsername = ADDON.getSetting('Username')
strpwd = ADDON.getSetting('Password')


def GetContent(url, data, referr, cj):
    if cj is None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer', referr),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache')]
    usock = opener.open(url, data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return (cj, response)


def GetInput(strMessage, headtxt, ishidden):
    keyboard = xbmc.Keyboard("", strMessage, ishidden)
    keyboard.setHeading(headtxt)  # optional
    keyboard.doModal()
    inputText = ""
    if keyboard.isConfirmed():
        inputText = keyboard.getText()
    del keyboard
    return inputText


def GetLoginCookie(cj, cookiefile):
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)
    if cj is None:
        cj = cookielib.LWPCookieJar()
    strUsername = urllib.quote_plus(
        GetInput("Please enter your username", "Username", False))
    respon = ""
    if strUsername is not None and strUsername != "":
        strpwd = urllib.quote_plus(
            GetInput("Please enter your password", "Password", True))
        (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login.php", cj)
        link = ''.join(respon.splitlines()).replace('\'', '"')
        match = re.compile('"streamer": "(.+?)",').findall(link)
        loginsuc = match[0].split("&")[1]
        matchauth = loginsuc.replace("auth=", "")
        ADDON.setSetting('authcode', matchauth)
        # setSettings(strUsername,strpwd,True)
    cj.save(cookiefile, ignore_discard=True)
    cj = cookielib.LWPCookieJar()
    cj.load(cookiefile, ignore_discard=True)
    if len(match) == 0:
        ADDON.setSetting('authcode', "")
        d = xbmcgui.Dialog()
        d.ok("Incorrect Login", "Login failed", 'Try logging in again')
        return None
    else:
        ADDON.setSetting('Username', strUsername)
        ADDON.setSetting('Password', strpwd)
    return cj, respon


def GetNoobLink(cj):
    (cj, link) = GetContent("http://www.noobroom.com", "", "", cj)
    match = re.compile('value="(.+?)">').findall(link)
    return match[0]


nooblink = GetNoobLink(cj)

def AutoLogin(url, cj):
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)
    if cj is None:
        cj = cookielib.LWPCookieJar()
    if strUsername is not None and strUsername != "" and strpwd != None and strpwd != "":
        (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login.php", cj)
        cj.save(cookiefile, ignore_discard=True)
        link = ''.join(respon.splitlines()).replace('\'', '"')
        match = re.compile('"streamer": "(.+?)",').findall(link)
        loginsuc = match[0].split("&")[1]
        matchauth = loginsuc.replace("auth=", "")
        ADDON.setSetting('authcode', matchauth)
    cj.load(cookiefile, ignore_discard=True)
    return cj, respon


def GetVideoLink(url, isHD, cj):
    if len(strUsername) == 0 or len(strpwd) == 0:
        (cj, link) = GetLoginCookie(cj, cookiefile)
    else:
        (cj, link) = AutoLogin(url, cj)
    authstring = ""
    if len(authcode) > 0:
        authstring = "&auth=" + authcode
    else:
        isHD = "0"
    match = re.compile('"streamer": "(.+?)",').findall(link)[
        0].split("&")[0] + authstring + "&loc=" + location + "&hd=" + isHD

    return cj, match


(cj, noobvideolink) = GetVideoLink(nooblink + "/login2.php", isHD, cj)

def HOME():
    addDir('Search', 'search', 5, '')
    addDir('Movies A-Z', 'Movies', 2, '')
    addDir('TV Shows', 'TV', 9, '')
    addDir('Last 50 Added', 'Latest', 8, '')
    addDir('Recently Released', 'Released', 12, '')
    addDir('IMDB Rating order', 'ImdbRating', 13, '')
    addLink('Refresh Movie list', 'Refresh', 7, '')
    addLink('Login', 'Login', 11, '')


def INDEXAZ():
    addDir('A', 'A', 4, '')
    addDir('B', 'B', 4, '')
    addDir('C', 'C', 4, '')
    addDir('D', 'D', 4, '')
    addDir('E', 'E', 4, '')
    addDir('F', 'F', 4, '')
    addDir('G', 'G', 4, '')
    addDir('H', 'H', 4, '')
    addDir('I', 'I', 4, '')
    addDir('J', 'J', 4, '')
    addDir('K', 'K', 4, '')
    addDir('L', 'L', 4, '')
    addDir('M', 'M', 4, '')
    addDir('N', 'N', 4, '')
    addDir('O', 'O', 4, '')
    addDir('P', 'P', 4, '')
    addDir('Q', 'Q', 4, '')
    addDir('R', 'R', 4, '')
    addDir('S', 'S', 4, '')
    addDir('T', 'T', 4, '')
    addDir('U', 'U', 4, '')
    addDir('V', 'V', 4, '')
    addDir('W', 'W', 4, '')
    addDir('X', 'X', 4, '')
    addDir('Y', 'Y', 4, '')
    addDir('Z', 'Z', 4, '')
    addDir('Others', '-1', 4, '')


def SEARCH():
    keyb = xbmc.Keyboard('', 'Enter search text')
    keyb.doModal()
    searchText = ''
    if keyb.isConfirmed():
        searchText = urllib.quote_plus(keyb.getText())
    SearchXml(searchText)


def renderListingPage(resourceName, url):
    localfile = xbmc.translatePath(
        os.path.join(home, 'resources', resourceName + '.xml'))
    if os.path.isfile(localfile) is False:
        BuildXMl(cj, localfile, url)
    f = open(localfile, "r")
    text = f.read()
    match = re.compile(
        '<movie name="(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(50):
        (mName, mNumber, vyear) = match[i]
        addLink(urllib.unquote_plus(mName).replace("&amp;","&"), mNumber, 6, nooblink + "/2img" + mNumber + ".jpg")


def Released():
    renderListingPage("released", "year.php")


def ImdbRating():
    renderListingPage("rating", "rating.php")


def Last25():
    renderListingPage("noobroom", "latest.php")


def SearchXml(SearchText):
    (jc, link) = GetContent(nooblink + "/search.php?q=" + SearchText, "", nooblink, cj)
    print link
    match = re.compile(
        '<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>'
    ).findall(link)

    for i in range(len(match)):
        (movieYear, moviehref, movieName) = match[i]
        href = moviehref.replace("?", "")
        addLink(urllib.unquote_plus(movieName), href, 6, nooblink + "/2img" + href + ".jpg")
    # localfile = xbmc.translatePath(
    #     os.path.join(home, 'resources', "noobroom" + '.xml'))
    # if os.path.isfile(filename) is False:
    #     BuildXMl(cj, localfile, "latest.php")
    # f = open(filename, "r")
    # text = f.read()
    # if SearchText == '-1':
    #     match = re.compile(
    #         '<movie name="[^A-Za-z](.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    #     SearchText = ""
    # else:
    #     match = re.compile('<movie name="' + SearchText +
    #                        '(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    # for i in range(len(match)):
    #     (mName, mNumber, vyear) = match[i]
    #     addLink(urllib.unquote_plus(SearchText + mName), mNumber, 6, nooblink + "/2img" + mNumber + ".jpg")
    #     addLink(SearchText + mName, mNumber, 6, "")

def ParseXML(year, url, name, doc, mlist):
    movie = doc.createElement("movie")
    mlist.appendChild(movie)
    movie.setAttribute("year", year)
    movie.setAttribute("name", name)
    movie.setAttribute("url", url)

def RefreshAll():
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
    BuildXMl(cj, localfile, "latest.php")
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'rating.xml'))
    BuildXMl(cj, localfile, "rating.php")
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'released.xml'))
    BuildXMl(cj, localfile, "year.php")

def BuildXMl(cj, filename, url):
    xbmc.executebuiltin(
        "XBMC.Notification(Please Wait!,Refreshing Movie List,5000)")
    (cj, link) = GetContent(nooblink + "/" + url, "", nooblink, cj)
    mydoc = Document()
    mlist = mydoc.createElement("movielist")
    mydoc.appendChild(mlist)
    match = re.compile(
        '<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    for i in range(len(match)):
        (vyear, mNumber, mName) = match[i]
        ParseXML(vyear, mNumber.replace('?', ''),
                 urllib.quote_plus(mName).replace('+', ' '), mydoc, mlist)

    f = open(filename, 'w')
    f.write(mydoc.toprettyxml())
    f.close()


def GetDirVideoUrl(url, cj):
    if cj is None:
        cj = cookielib.LWPCookieJar()

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            print "redirecturl" + self.video_url
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    redirhndler = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(redirhndler, urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener()
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer', url),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache')]
    # urllib2.install_opener(opener)
    usock = opener.open(url)
    return redirhndler.video_url


def Episodes(name, videoId):
    # try:
    match = re.compile("\/(.+?)&sp").findall(videoId + "&sp")
    if len(match) >= 0:
        videoId = match[0]
    try:
        vidlink = GetDirVideoUrl(
            noobvideolink + "&tv=0" + "&start=0&file=" + videoId, cj) + "&loc=" + location
    except:
        vidlink = GetDirVideoUrl(noobvideolink.replace(
            "&hd=" + isHD, "&hd=0") + "&tv=0" + "&start=0&file=" + videoId, cj) + "&loc=" + location
    # vidlink="http://46.165.228.108/index.php?file=1871&start=0&hd=0&auth=&type=flv&tv=0"
    cookiestr = ""
    for cookie in cj:
        cookiestr = cookiestr + ('%s=%s;' % (cookie.name, cookie.value))
    fullvid = ('%s|Cookie="%s"' % (vidlink, cookiestr + "save=1"))
    fullvid = ('%s|User-Agent="%s"' %
               (fullvid, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'))

    meta = {
        'Title': name,
        'Thumb': nooblink + "/2img" + videoId + ".jpg"
    }

    playVideo("noobroom", fullvid, meta)


def ListTVSeries(cj):
    (cj, link) = GetContent(nooblink + "/series.php", "", nooblink, cj)
    link = ''.join(link.splitlines()).replace('\'', '"')
    match = re.compile(
        '<table><tr><td><a href="(.+?)"><img style="border:0" src="(.+?)" width="(\d+)" height="(\d+)"></a>').findall(link)
    matchname = re.compile(
        '<b><a style="color:#fff" href="(.+?)">(.+?)</a></b>').findall(link)
    for i in range(len(match)):
        addDir(matchname[i][1], nooblink + match[i][0], 10, nooblink + "/" + match[i][1])


def ListEpisodes(url, cj):
    (cj, link) = GetContent(url, "", nooblink, cj)
    link = ''.join(link.splitlines()).replace('\'', '"')
    match = re.compile(
        '<br><b>(.+?)<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    cookiestr = ""
    for cookie in cj:
        cookiestr = cookiestr + ('%s=%s;' % (cookie.name, cookie.value))
    for i in range(len(match)):
        vidlink = noobvideolink.replace(
            "&hd=1", "&hd=0") + match[i][1].replace("/?", "&file=")

        if i == 0:
            vidlink = GetDirVideoUrl(
                vidlink, cj) + "&loc=" + location + "&hd=0"
        else:
            vidlink = vidlink.replace(match[i - 1][1].replace(
                "/?", "&file="), match[i][1].replace("/?", "&file="))
        fullvid = ('%s|Cookie="%s"' % (vidlink, cookiestr + "save=1"))
        fullvid = ('%s|User-Agent="%s"' %
                   (fullvid, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'))
        addLink(match[i][0] + match[i][2], fullvid, 3, "")


def playVideo(videoType, link, meta=None):
    print videoType + '=' + link
    if videoType == "youtube":
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + link.replace('?', '')
        xbmc.executebuiltin("xbmc.PlayMedia(" + url + ")")
    # elif videoType == "vimeo":
        # url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    # elif videoType == "tudou":
        # url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        if(meta==None):
             meta = {
                 'Title': '',
                 'Thumb': ''
             }
        listitem = xbmcgui.ListItem(meta.get("Title"))
        listitem.setInfo('video', meta)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        xbmcPlayer.play(link, listitem)


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S"))
        )
    except:
        #force update
        return datetime.datetime.today() - datetime.timedelta(days=1)


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(
        url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    # ok = True
    # rating = "5.0"
    # movieModes = [6]
    # if mode in movieModes:
        # jsonData = getMovieInfo(name)
        # rating = str(jsonData['rating'])

    meta = {'title': name}

    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)

    liz.setInfo('Video', meta)
    # liz.setProperty('fanart_image', '')
    # liz.setProperty('imdb', 'tt1343092')
    # liz.setProperty('img', '')

    contextMenuItems = getContextMenuItems()

    liz.addContextMenuItems(contextMenuItems, replaceItems=True)

    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addNext(formvar, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&formvar=" + str(
        formvar) + "&name=" + urllib.quote_plus('Next >')
    ok = True
    liz = xbmcgui.ListItem(
        'Next >', iconImage=noobroomlogo, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": 'Next >'})
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(
        url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(
        name, iconImage=noobroomlogo, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def getContextMenuItems():
    menu_items = []
    # menu_items.append(('Show Information', 'XBMC.Action(Info)'), )
    return menu_items


def getMovieInfo(movieName):
    jsonUrl = 'http://deanclatworthy.com/imdb/?q=' + movieName
    data = json.load(urllib2.urlopen(jsonUrl))
    return data
    # http://deanclatworthy.com/imdb/?q=The+Green+Mile
    # url = 'http://deanclatworthy.com/'
    # values = {}
    # params = {}
    # values["method"] = 'get'
    # params["q"] = movieName
    # if params is not None:
    #     values["params"] = params
    # headers = {"Content-Type":"application/json"}
    #
    # data = json.dumps(values)
    # req = urllib2.Request(url, data, headers)
    # response = urllib2.urlopen(req)
    # response = response.read()
    # return json.loads(response)

params = get_params()
url = None
name = None
mode = None
formvar = None
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    formvar = int(params["formvar"])
except:
    pass

sysarg = str(sys.argv[1])
if mode is None or url is None or len(url) < 1:
    HOME()

elif mode == 2:
    INDEXAZ()
elif mode == 3:
    playVideo("noobroom", url)
elif mode == 4:
    SearchXml(url)
elif mode == 5:
    SEARCH()
elif mode == 6:
    Episodes(name, str(url))
elif mode == 7:
    RefreshAll()
elif mode == 8:
    Last25()
elif mode == 9:
    ListTVSeries(cj)
elif mode == 10:
    ListEpisodes(url, cj)
elif mode == 11:
    GetLoginCookie(cj, cookiefile)
elif mode == 12:
    Released()
elif mode == 13:
    ImdbRating()
xbmcplugin.endOfDirectory(int(sysarg))