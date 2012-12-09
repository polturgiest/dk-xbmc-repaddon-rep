# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os

__addonname__ = "sugoideasV2"
__addonid__ = "plugin.video.sugoideasV2"
__addon__ = xbmcaddon.Addon(id=__addonid__)

CATEGORY_LIST = {'Updates':{'url':'http://feeds.feedburner.com/twsugoideas?format=xml', 'mode':'6'}, 
                 'Variety Shows':{'url':'http://sugoideas.com/variety-shows/', 'mode':'1'}, 
                 'Drama Series':{'url':'http://sugoideas.com/', 'mode':'5'}}

class Program :
    def __init__(self, link, titleAlt, imgTitle, img, title, hosts, releaseDate):
        self.link = link
        self.titleAlt = titleAlt
        self.imgTitle = imgTitle
        self.img = img
        self.title = title                
        self.hosts = hosts
        self.releaseDate = releaseDate                        

    def toString(self):
        return 'Title : ' + self.title + ', Link : ' + self.link      

class Episode :
    def __init__(self, title, link):
        self.title = title
        self.link = link
            
    def toString(self):
        return 'Title : ' + self.title + ', Link : ' + self.link

class Video:
    def __init__(self, title, link):
        self.title = title
        self.link = link
    def toString(self):
        return 'Title : ' + self.title + ', Link : ' + self.link

class YearList:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def toString(self):
        return 'Title : ' + self.title + ', Link : ' + self.link

def getYearList(url):
    year_list = [];
    html = getHttpData(url)
    match = re.compile('<li><ahref="(.+?)"><span>(.+?)</span></a>').findall(html)
    index = 0;    
    while index < len(match):    
        yearRec = YearList(match[index][1], url + match[index][0])    
        year_list.append(yearRec)
        index = index + 1                          
    return year_list
	
def PLAYLIST_VIDEOLINKS(url,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = url.split(';#')
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                ytid=getYoutubeID(videoLink)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                if(len(ytid)>0):
                       liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
                       playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                       yturl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=" + ytid
                       playlist.add(url=yturl, listitem=liz)
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False   
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items','Check links individually.')
        return ok

def get_params(param_string):
    param = []
    paramstring = param_string
    if len(paramstring) >= 2:
        params = param_string
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]   
    return param
    
def getHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    httpdata = re.sub("\s", "", httpdata)
    return httpdata

def getPrograms(html):
    programs = []
    match = re.compile('<divclass="upcomingad"><ahref="([^"]+)"><imgalt="([^"]+)"title="([^"]+)"src="([^"]+)"style="padding:3px;"height="170"width="250"border="0"/></a><br/><strong>Title:</strong>([^<]+)<br/><strong>Host:</strong><spanclass="searchOne">([^<]+)</span><br/><strong>ReleaseDate:</strong>([^<]+)</div>').findall(html)
    index = 0;    
    while index < len(match):    
        prog = Program(match[index][0], match[index][1], match[index][2], match[index][3], match[index][4], match[index][5], match[index][6])    
        programs.append(prog)
        index = index + 1                          
    return programs

def getDramas(html):
    programs = []
    match = re.compile('<divclass="postsearch"><divclass="upcomingad"><spanclass="complete">[^<]*</span><ahref="([^"]+)"><imgalt="([^"]+)"title="([^"]+)"src="([^"]+)"style="padding:3px;"height="170"width="250"border="0"/></a><br/><strong>Title:</strong>([^<]+)<br/><strong>Cast:</strong><spanclass="searchOne">([^<]+)</span><br/><strong>ReleaseDate:</strong>([^<]+)</div></div>').findall(html)
    index = 0;    
    while index < len(match):   
        prog = Program(match[index][0], match[index][1], match[index][2], match[index][3], match[index][4], match[index][5], match[index][6])    
        programs.append(prog)
        index = index + 1                          
    return programs

def getEpisodes(html):
    episodes = []
    match = re.compile('<li><atarget="_blank"href="([^"]+)">([^<]+)</a></li>').findall(html)
    index = 0;    
    while index < len(match):                
        epi = Episode(match[index][1], match[index][0])    
        episodes.append(epi)
        index = index + 1    
    return episodes

def getLatestEpisodes(html):
    episodes = []
    match = re.compile('<item><title>([^<]+)</title><link>([^<]+)</link><comments>').findall(html)
    index = 0;    
    while index < len(match):   
        epi = Episode(match[index][0], match[index][1])
        episodes.append(epi)
        index = index + 1                          
    return episodes

def getVideos(url):
    html = getHttpData(url)
    videos = []
    match = re.compile('<aclass="contentlist"href="([^"]+)">([^<]+)</a>').findall(html)
    index = 0;   
    videos.append(Video('Part1',url))
    while index < len(match):                
        video = Video(match[index][1], match[index][0])    
        videos.append(video)
        index = index + 1  
    return videos

def getYoutubeID(url):
    if(len(url) > 0):
         html = getHttpData(url)
    else:
         html=""
    id = ''
    match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(html)
    if len(match) > 0:
         id = match[0][len(match[0])-1].replace('v/','')
    return id

def categoryList():
    totalLen = len(CATEGORY_LIST)
    index = 1 
    for key in CATEGORY_LIST.keys():
        li = xbmcgui.ListItem(str(index) + '. ' + key)
        u = sys.argv[0] + '?mode=' + CATEGORY_LIST[key]['mode'] + '&url=' + urllib.quote_plus(CATEGORY_LIST[key]['url'])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)
        index = index + 1
    xbmcplugin.setContent(int(sys.argv[1]), 'category')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def dramaYearList():
    year_list = getYearList('http://sugoideas.com')
    totalLen = len(year_list)
    index = 1 
    for year in year_list:
        li = xbmcgui.ListItem(str(index) + '. ' + year.title)
        u = sys.argv[0] + '?mode=7&url=' + urllib.quote_plus(year.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)
        index = index + 1
    xbmcplugin.setContent(int(sys.argv[1]), 'programs')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return

def newList(url):
    html = getHttpData(url)
    episodes = getLatestEpisodes(html) 
    totalLen = len(episodes) 
    for epi in episodes:
        li = xbmcgui.ListItem(epi.title)
        u = sys.argv[0] + '?mode=3&url=' + urllib.quote_plus(epi.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)    
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return
       
def programList(url):
    html = getHttpData(url)
    programs = getPrograms(html) 
    totalLen = len(programs) 
    index = 1
    for prog in programs:
        li = xbmcgui.ListItem(label = str(index) + '. ' + prog.title, thumbnailImage = prog.img)
        u = sys.argv[0] + "?mode=2&url=" + urllib.quote_plus(prog.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)
        index = index + 1    
    xbmcplugin.setContent(int(sys.argv[1]), 'programs')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return

def dramaList(url):
    html = getHttpData(url)
    programs = getDramas(html) 
    totalLen = len(programs) 
    index = 1
    for prog in programs:
        li = xbmcgui.ListItem(label = str(index) + '. ' + prog.title, thumbnailImage = prog.img)
        u = sys.argv[0] + "?mode=2&url=" + urllib.quote_plus(prog.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)  
        index = index + 1  
    xbmcplugin.setContent(int(sys.argv[1]), 'programs')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def episodeList(url):
    html = getHttpData(url)
    episodes = getEpisodes(html) 
    totalLen = len(episodes) 
    for epi in episodes:
        li = xbmcgui.ListItem(epi.title)
        u = sys.argv[0] + '?mode=3&url=' + urllib.quote_plus(epi.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalLen)    
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return
	
def playVideo(videoType,videoId):
    url = videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)
	
def videoList(url):
    videos = getVideos(url) 
    totalLen = len(videos) 
    videolist =""
    for video in videos:
        videolist=videolist+video.link+";#"
        li = xbmcgui.ListItem(video.title)
        u = sys.argv[0] + '?mode=4&url=' + urllib.quote_plus(video.link)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalLen)    
    if(len(videolist) > 0):
        li = xbmcgui.ListItem("Play all the parts above")
        u = sys.argv[0] + '?mode=8&url=' + urllib.quote_plus(videolist)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalLen)  
    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return  

def getYoutubeVideoUrl(id):
    url = 'http://www.youtube.com/get_video_info?video_id=' + id
    html = getHttpData(url)
    params = get_params(html)
    parts = urllib.unquote_plus(params['fmt_stream_map']).split(',')
    url_map = {}
    for part in parts:
        tmp = urllib.unquote_plus(part).split('|')
        url_map[tmp[0]] = tmp[1]
    return url_map;

def getHQYoutubeVideoUrl(map):
    # 37 1080p
    url = ''
    if map.has_key('22'):  # 720p
        url = map['22']
    elif map.has_key('35'):
        url = map['35']
    elif map.has_key('34'):
        url = map['34']
    elif map.has_key('18'):
        url = map['18']
    elif map.has_key('5'):
        url = map['5']                
    return url

params = get_params(sys.argv[2])
mode = None
name = None
url = None
thumb = None
page = None

try:
    mode = urllib.unquote_plus(params["mode"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
    
if mode == None:
    categoryList()
elif mode == '1':  
    programList(url)
elif mode == '2':
    episodeList(url)
elif mode == '3':
    videoList(url)
elif mode == '4':
    try:
        id = getYoutubeID(url)
        playVideo("youtube",id)
        #video_map = getYoutubeVideoUrl(id)
        #video_link = getHQYoutubeVideoUrl(video_map)
        #xbmc.Player().play(video_link)
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok('eror', 'Error Playing Video')   
        pass    
elif mode == '5':
    dramaYearList();
elif mode == '6': 
    newList('http://feeds.feedburner.com/twsugoideas?format=xml');
elif mode == '7':
    dramaList(url)
elif mode == '8':
    PLAYLIST_VIDEOLINKS(url,name)