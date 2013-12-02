import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import urlresolver
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
import json
import datetime

ADDON = xbmcaddon.Addon(id='plugin.video.phim47')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "phim47"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.6" #<---- PLUGIN VERSION
homeLink="http://phim.li/"
usehd = ADDON.getSetting('use-hd') == 'true'
def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
#def HOME():
#        addDir('Search','http://phim47.com/',4,'http://yeuphim.net/images/logo.png')
#        addDir('HQ Videos','http://phim47.com/list-hd.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Movies','http://phim47.com/movie-list/phim-le.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Series','http://phim47.com/movie-list/phim-bo.html ',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Videos By Region','http://phim47.com/',8,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Videos By Category ','http://phim47.com/',9,'http://phim47.com/skin/movie/style/images/logo.png')
def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def HOME():
        addDir('Search','http://phim47.com/',4,'http://yeuphim.net/images/logo.png')
        link = GetContent(homeLink)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<li class="downmenu">(.+?)(</span>|</ul>)</li>').findall(newlink)
        for vmenu,vtmp in match:
              maincontent=re.compile('<span><a [^>]*onmouseover=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></span>').findall(vmenu+"</span>")
              if(len(maincontent) == 0):
                   maincontent=re.compile('<span><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></span>').findall(vmenu+"</span>")
              mainurl,mainname=maincontent[0]
              addDir(mainname,homeLink+mainurl,2,'')
              submatch=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vmenu)
              for vsubmenu in submatch:
                    vLink, vLinkName=vsubmenu
                    addDir("--- "+ RemoveHTML(vLinkName).strip(),homeLink+vLink,2,'')
def Countries():
        addDir('Vietnam','http://phim47.com/phim-viet-nam.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Korea','http://phim47.com/phim-han-quoc.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('China','http://phim47.com/phim-trung-quoc.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Hong Kong','http://phim47.com/phim-hong-kong.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Japan','http://phim47.com/phim-nhat-ban.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Taiwan','http://phim47.com/phim-dai-loan.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Asia','http://phim47.com/phim-chau-a.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('India','http://phim47.com/phim-an-do.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Thailand','http://phim47.com/phim-thai-lan.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('France','http://phim47.com/phim-phap.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('America','http://phim47.com/phim-my---khac.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
		
def Categories():
        addDir('Action','http://phim47.com/the-loai-phim-hanh-dong.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Comedy','http://phim47.com/the-loai-phim-hai-huoc.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Animation','http://phim47.com/the-loai-phim-hoat-hinh.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Martial Arts','http://phim47.com/the-loai-phim-vo-thuat.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Psychological','http://phim47.com/the-loai-phim-tam-ly.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Fiction','http://phim47.com/the-loai-phim-vien-tuong.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('War/Combat','http://phim47.com/the-loai-phim-chien-tranh.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Horror/Thriller','http://phim47.com/the-loai-phim-kinh-di.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Adventure','http://phim47.com/the-loai-phim-phieu-luu.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Fantasy','http://phim47.com/the-loai-phim-than-thoai.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('TV','http://phim47.com/the-loai-phim-truyen-hinh.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Sports','http://phim47.com/the-loai-phim-the-thao.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Music/Art','http://phim47.com/the-loai-phim-am-nhac.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Romance','http://phim47.com/the-loai-phim-tinh-cam.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Popular','http://phim47.com/the-loai-phim-da-su---co-trang.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Crime Drama','http://phim47.com/the-loai-phim-hinh-su.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
		
def INDEX(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        match=re.compile('<div id="list">(.+?)<div class="pagination">').findall(link)
        vidlist = re.compile('<li><div class="zitemList"><a [^>]*href="(.+?)" title="(.+?)" [^>]*>(.+?)</a>').findall(match[0])
        for vurl,vname,vimg in vidlist:
            vimg=re.compile('<img class="showend" [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vimg)[0]
            addDir(vname,homeLink+vurl,7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        navmatch=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(pagelist[0])
        for vurl,vname in navmatch:
            addDir("page " + vname,homeLink +'/'+vurl,2,"")


def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://phim.li/tim-kiem/'+searchText+'.html'
        INDEX(url)
    except: pass

def Mirrors(url,name):
  mirrorlink =getVidPage(url,name)
  link = GetContent(mirrorlink)
  link=''.join(link.splitlines()).replace('\'','"')
  try:
            link =link.encode("UTF-8")
  except: pass
  mirmatch=re.compile('<div class="listserver">(.+?)<div id="fb-root">').findall(link)
  servlist =re.compile('<div class="name left namew">(.+?)&nbsp;&nbsp;&nbsp;').findall(mirmatch[0])
  for vname in servlist:
         addDir(vname.encode("utf-8"),mirrorlink.encode("utf-8"),5,"")  

			
def decodeurl(encodedurl):
    tempp9 =""
    tempp4="1071045098811121041051095255102103119"
    strlen = len(encodedurl)
    temp5=int(encodedurl[strlen-4:strlen],10)
    encodedurl=encodedurl[0:strlen-4]
    strlen = len(encodedurl)
    temp6=""
    temp7=0
    temp8=0
    while temp8 < strlen:
        temp7=temp7+2
        temp9=encodedurl[temp8:temp8+4]
        temp9i=int(temp9,16)
        partlen = ((temp8 / 4) % len(tempp4))
        partint=int(tempp4[partlen:partlen+1])
        temp9i=((((temp9i - temp5) - partint) - (temp7 * temp7)) -16)/3
        temp9=chr(temp9i)
        temp6=temp6+temp9
        temp8=temp8+4
    return temp6
	
def getVidPage(url,name):
  contentlink = GetContent(url)
  contentlink = ''.join(contentlink.splitlines()).replace('\'','"')
  try:
            contentlink =contentlink.encode("UTF-8")
  except: pass
  mlink=re.compile('<a id="xemphimus" [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(contentlink)
  return mlink[0].replace("title=","")


def Episodes(url,name):
    #try:
        link = GetContent(url)
        link=''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        mirmatch=re.compile('<div class="listserver">(.+?)<div id="fb-root">').findall(link)
        servlist =re.compile('<div class="name left namew">'+name+'&nbsp;&nbsp;&nbsp;(.+?)<div class="clear_td">').findall(mirmatch[0])
        epilist =re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(servlist[0])
        curmatch =re.compile('<a class="current"\s*>(.+?)</a>').findall(servlist[0])
        if(len(curmatch)>0):
              addLink("part - "+ curmatch[0].strip(),"".join(i for i in url if ord(i)<128),3,'',name)
        for vlink,vLinkName in epilist:
              addLink("part - "+ vLinkName.strip(),"".join(i for i in vlink if ord(i)<128),3,'',name)

    #except: pass

def Geturl(strToken):
        for i in range(20):
                try:
                        strToken=strToken.decode('base-64')
                except:
                        return strToken
                if strToken.find("http") != -1:
                        return strToken
	   
def GetContent(url):
    try:
       net = Net()
       try:
            second_response = net.http_GET(url)
       except:
            second_response = net.http_GET(url.encode("utf-8"))
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','www.phim.li')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def loadVideos(url,name):
    #try:
        GA("LoadVideo","NA")
        xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
        link=GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        match = re.compile('proxy.link=phim47\*(.+?)&').findall(link)
        if(len(match)==0):
              match = re.compile('proxy.link=(.+?)&').findall(link)
              newlink=match[0]
        else:
              newlink =decodeurl(match[0])
        #newlink="http://picasaweb.google.com/lh/photo/L><bkExMzFHWsMxWPnx?qfp0Izq><HmrJ91ZTEDpmIzA@OiJSEGDGufZGHjoj=="
        if(newlink.find("cyworld.vn") > 0):
            vidcontent=GetContent(newlink)
            vidmatch=re.compile('<meta property="og:video" content="(.+?)" />').findall(vidcontent)
            vidlink=vidmatch[0]
            playVideo("direct",vidlink)
        elif(newlink.find("picasaweb.google") > 0):
            vidcontent=postContent("http://player.phim.li/picasaphp/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%20NT%206%2E1%3B%20WOW64%3B%20rv%3A13%2E0%29%20Gecko%2F20100101%20Firefox%2F13%2E0&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",homeLink)
            #vidcontent=GetContent(newlink)
            #print vidcontent
            #data = json.loads('{"'+vidcontent+'}]}')
            #print data
            vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
            hdmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?)').findall(vidmatch[-1][2])
            if(len(hdmatch) > 0) and usehd==True:
                 vidmatch=hdmatch
            vidlink=vidmatch[-1][0]
            playVideo("direct",vidlink)
        elif(newlink.find("youtube") > 0):
            vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
            vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
            playVideo("youtube",vidlink)
        else:
            sources = []
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=newlink, title=label)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            print "urlrsolving" + newlink
            if source:
                vidlink = source.resolve()
            else:
                vidlink =""
            playVideo("direct",vidlink)
    #except:
       #d = xbmcgui.Dialog()
       #d.ok(url,"Can't play video",'Try another link')
   
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

def addLink(name,url,mode,iconimage,mirrorname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirrorname="+urllib.quote_plus(mirrorname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="http://yeuphim.net/images/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param



params=get_params()
url=None
name=None
mode=None
formvar=None
mirrorname=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])
print "mode is:" + str(mode)
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       Episodes(url,name)
elif mode==7:
       Mirrors(url,name)
elif mode==8:
       Countries()
elif mode==9:
       Categories()
xbmcplugin.endOfDirectory(int(sysarg))
