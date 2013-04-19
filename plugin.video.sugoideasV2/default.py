# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os
try: import simplejson as json
except ImportError: import json
import cgi
import datetime
import time

__addonname__ = "sugoideasV2"
__addonid__ = "plugin.video.sugoideasV2"
ADDON =__addon__ = xbmcaddon.Addon(id=__addonid__)

CATEGORY_LIST = {'Updates':{'url':'http://feeds.feedburner.com/twsugoideas?format=xml', 'mode':'6'}, 
                 'Variety Shows':{'url':'http://sugoideas.com/variety-shows/', 'mode':'1'}, 
                 'Drama Series':{'url':'http://sugoideas.com/', 'mode':'5'}, 
                 'Search':{'url':'http://sugoideas.com/', 'mode':'9'}}

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "sugoideasV2"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.5" #<---- PLUGIN VERSION

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

def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://sugoideas.com/search/'+ searchText
        dramaList(url)

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
                       #yturl = "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=" + ytid
                       yturl=getYoutube(ytid)
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
		
def extractFlashVars(data):
    for line in data.split("\n"):
            index = line.find("ytplayer.config =")
            if index != -1:
                found = True
                p1 = line.find("=", (index-3))
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                        continue
                data = line[p1 + 1:p2]
                break
    if found:
            data = json.loads(data)
            flashvars = data["args"]
    return flashvars    
		
def selectVideoQuality(links):
        link = links.get
        video_url = ""
        fmt_value = {
                5: "240p h263 flv container",
                18: "360p h264 mp4 container | 270 for rtmpe?",
                22: "720p h264 mp4 container",
                26: "???",
                33: "???",
                34: "360p h264 flv container",
                35: "480p h264 flv container",
                37: "1080p h264 mp4 container",
                38: "720p vp8 webm container",
                43: "360p h264 flv container",
                44: "480p vp8 webm container",
                45: "720p vp8 webm container",
                46: "520p vp8 webm stereo",
                59: "480 for rtmpe",
                78: "seems to be around 400 for rtmpe",
                82: "360p h264 stereo",
                83: "240p h264 stereo",
                84: "720p h264 stereo",
                85: "520p h264 stereo",
                100: "360p vp8 webm stereo",
                101: "480p vp8 webm stereo",
                102: "720p vp8 webm stereo",
                120: "hd720",
                121: "hd1080"
        }
        hd_quality = 1

        # SD videos are default, but we go for the highest res
        #print video_url
        if (link(35)):
            video_url = link(35)
        elif (link(59)):
            video_url = link(59)
        elif link(44):
            video_url = link(44)
        elif (link(78)):
            video_url = link(78)
        elif (link(34)):
            video_url = link(34)
        elif (link(43)):
            video_url = link(43)
        elif (link(26)):
            video_url = link(26)
        elif (link(18)):
            video_url = link(18)
        elif (link(33)):
            video_url = link(33)
        elif (link(5)):
            video_url = link(5)

        if hd_quality > 1:  # <-- 720p
            if (link(22)):
                video_url = link(22)
            elif (link(45)):
                video_url = link(45)
            elif link(120):
                video_url = link(120)
        if hd_quality > 2:
            if (link(37)):
                video_url = link(37)
            elif link(121):
                video_url = link(121)

        if link(38) and False:
            video_url = link(38)
        for fmt_key in links.iterkeys():

            if link(int(fmt_key)):
                    text = repr(fmt_key) + " - "
                    if fmt_key in fmt_value:
                        text += fmt_value[fmt_key]
                    else:
                        text += "Unknown"

                    if (link(int(fmt_key)) == video_url):
                        text += "*"
            else:
                    print "- Missing fmt_value: " + repr(fmt_key)

        video_url += " | " + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


        return video_url

def getYoutube(videoid):

                code = videoid
                linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
                req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
                        if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
                                req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                link=response.read()
                                response.close()
                
                flashvars = extractFlashVars(link)

                links = {}

                for url_desc in flashvars[u"url_encoded_fmt_stream_map"].split(u","):
                        url_desc_map = cgi.parse_qs(url_desc)
                        if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
                                continue

                        key = int(url_desc_map[u"itag"][0])
                        url = u""
                        if url_desc_map.has_key(u"url"):
                                url = urllib.unquote(url_desc_map[u"url"][0])
                        elif url_desc_map.has_key(u"stream"):
                                url = urllib.unquote(url_desc_map[u"stream"][0])

                        if url_desc_map.has_key(u"sig"):
                                url = url + u"&signature=" + url_desc_map[u"sig"][0]
                        links[key] = url
                highResoVid=selectVideoQuality(links)
                return highResoVid 
				
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
    match = re.compile('<divclass="postsearch"><divclass="upcomingad"><spanclass="complete">[^<]*</span><ahref="([^"]+)"><imgalt="([^"]+)"title="([^"]+)"src="([^"]+)"style="padding:3px;"height="170"width="250"border="0"/></a><br/><strong>Title:</strong>([^<]+)<br/><strong>Cast:</strong><spanclass="searchOne">([^<]+)</span><br/><strong>ReleaseDate:</strong>([^<]+)</div>').findall(html)
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
        url = getYoutube(videoId.replace('?',''))
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
checkGA()

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
    GA("Category","HOME")
    categoryList()
elif mode == '1': 
    GA("Programlist",name) 
    programList(url)
elif mode == '2':
    episodeList(url)
elif mode == '3':
    GA("PlayVideo",name)
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
    GA("PlayVideo",name) 
    PLAYLIST_VIDEOLINKS(url,name)
elif mode == '9':
    SEARCH()
