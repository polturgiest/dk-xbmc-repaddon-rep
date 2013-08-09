import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from xml.dom.minidom import Document
import datetime


addon_id="plugin.video.NoobRoom"
ADDON =__settings__ = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
tvfilename = xbmc.translatePath(os.path.join(home, 'resources', 'tvshow.xml'))
cookie_path = os.path.join(datapath, 'cookies')
cookiefile= os.path.join(cookie_path, "cookiejar.lwp")
cj=None
authcode=ADDON.getSetting('authcode')
reg_list = ["15", "12", "13", "14"]
if(len(authcode) > 0 and authcode!="0"):
     location=reg_list[int(ADDON.getSetting('region'))]
     isHD = "1"
else:
     isHD = "0"
     location=reg_list[0]
if(ADDON.getSetting('use-hd')!='true'):
    isHD="0"
	
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "NA"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.11" #<---- PLUGIN VERSION

strUsername=ADDON.getSetting('Username')
strpwd=ADDON.getSetting('Password')
def GetContent(url,data,referr,cj):
    if cj==None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
           buf = StringIO.StringIO(usock.read())
           f = gzip.GzipFile(fileobj=buf)
           response= f.read()
    else:
           response= usock.read()
    usock.close()
    return (cj,response)
	
def GetInput(strMessage,headtxt,ishidden):
    keyboard = xbmc.Keyboard("",strMessage,ishidden)
    keyboard.setHeading(headtxt) # optional
    keyboard.doModal()
    inputText=""
    if (keyboard.isConfirmed()):
        inputText = keyboard.getText()
    del keyboard
    return inputText
	
def GetLoginCookie(cj,cookiefile):
      if not os.path.exists(datapath): os.makedirs(datapath)
      if not os.path.exists(cookie_path): os.makedirs(cookie_path)
      if cj==None:
           cj = cookielib.LWPCookieJar()
      strUsername=urllib.quote_plus(GetInput("Please enter your username","Username",False))
      matchauth=None
      respon=""
      if strUsername != None and strUsername !="":
           strpwd=urllib.quote_plus(GetInput("Please enter your password","Password",True))
           (cj,respon)=GetContent(nooblink+"/login2.php","email="+strUsername+"&password="+strpwd+"&remember=on",nooblink+"/login.php",cj)
           link = ''.join(respon.splitlines()).replace('\'','"')
           match=re.compile('"streamer": "(.+?)",').findall(link)
           loginsuc=match[0].split("&")[1]
           matchauth=loginsuc.replace("auth=","")
           ADDON.setSetting('authcode',matchauth)
           #setSettings(strUsername,strpwd,True)
      cj.save(cookiefile, ignore_discard=True)
      cj=None
      cj = cookielib.LWPCookieJar()
      cj.load(cookiefile,ignore_discard=True)
      if (len(match)==0):
                ADDON.setSetting('authcode',"")
                d = xbmcgui.Dialog()
                d.ok("Incorrect Login","Login failed",'Try logging in again')
                return None
      else:
                ADDON.setSetting('Username',strUsername)
                ADDON.setSetting('Password',strpwd)
      return (cj,respon)
	  
def GetNoobLink(cj):
    (cj,link) = GetContent("http://www.noobroom.com","","",cj)
    match=re.compile('value="(.+?)">').findall(link)
    return match[0]

nooblink=GetNoobLink(cj)

def AutoLogin(url,cj):
      if not os.path.exists(datapath): os.makedirs(datapath)
      if not os.path.exists(cookie_path): os.makedirs(cookie_path)
      if cj==None:
           cj = cookielib.LWPCookieJar()
      if strUsername != None and strUsername !="" and strpwd != None and strpwd !="":
           (cj,respon)=GetContent(nooblink+"/login2.php","email="+strUsername+"&password="+strpwd+"&remember=on",nooblink+"/login.php",cj)
           cj.save(cookiefile, ignore_discard=True)
           link = ''.join(respon.splitlines()).replace('\'','"')
           match=re.compile('"streamer": "(.+?)",').findall(link)
           loginsuc=match[0].split("&")[1]
           matchauth=loginsuc.replace("auth=","")
           ADDON.setSetting('authcode',matchauth)  
      cj.load(cookiefile,ignore_discard=True)
      return (cj,respon)
print "locationis="+location
def GetVideoLink(url,isHD,cj):
    if(len(strUsername)==0 or len(strpwd)==0):
         (cj,link) = GetLoginCookie(cj,cookiefile)
    else:
         (cj,link) = AutoLogin(url,cj)
    authstring="&auth="+authcode
    match=re.compile('"streamer": "(.+?)",').findall(link)[0].split("&")[0] +authstring+ "&loc="+location+"&hd="+isHD

    return (cj,match)
	
(cj,noobvideolink)=GetVideoLink(nooblink+"/login2.php",isHD,cj)
print noobvideolink
def HOME():
        addDir('Search','search',5,'')
        addDir('Movies A-Z','Movies',2,'')
        addDir('TV Shows','TV',9,'')
        addDir('Last 25 Added','Latest',8,'')
        addLink('Refresh Movie list','Refresh',7,'')
        addLink('Login','Login',11,'')

def INDEXAZ(url):
        addDir('A','A',4,'')
        addDir('B','B',4,'')
        addDir('C','C',4,'')
        addDir('D','D',4,'')
        addDir('E','E',4,'')
        addDir('F','F',4,'')
        addDir('G','G',4,'')
        addDir('H','H',4,'')
        addDir('I','I',4,'')
        addDir('J','J',4,'')
        addDir('K','K',4,'')
        addDir('L','L',4,'')
        addDir('M','M',4,'')
        addDir('N','N',4,'')
        addDir('O','O',4,'')
        addDir('P','P',4,'')
        addDir('Q','Q',4,'')
        addDir('R','R',4,'')
        addDir('S','S',4,'')
        addDir('T','T',4,'')
        addDir('U','U',4,'')
        addDir('V','V',4,'')
        addDir('W','W',4,'')
        addDir('X','X',4,'')
        addDir('Y','Y',4,'')
        addDir('Z','Z',4,'')
        addDir('Others','-1',4,'')
			
def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        SearchXml(searchText)

def Last25():
    if os.path.isfile(filename)==False:
        BuildXMl(cj)
    f = open(filename, "r")
    text = f.read()
    match=re.compile('<movie name="(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(25):
        (mName,mNumber,vyear)=match[i]
        addLink(mName,mNumber,6,"")
		
def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl(cj)
    f = open(filename, "r")
    text = f.read()
    if SearchText=='-1':
        match=re.compile('<movie name="[^A-Za-z](.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)	
        SearchText=""
    else:
        match=re.compile('<movie name="' + SearchText + '(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(len(match)):
        (mName,mNumber,vyear)=match[i]
        addLink(SearchText+mName,mNumber,6,"")
		
def ParseXML(year,url,name, doc, mlist):
    movie= doc.createElement("movie")
    mlist.appendChild(movie)
    movie.setAttribute("year", year)
    movie.setAttribute("name", name)
    movie.setAttribute("url", url)
	
def BuildXMl(cj):
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Refreshing Movie List,5000)")
    (cj,link) = GetContent(nooblink +"/latest.php","",nooblink,cj)
    mydoc=Document()
    mlist = mydoc.createElement("movielist")
    mydoc.appendChild(mlist)
    match=re.compile('<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    for i in range(len(match)):
        (vyear,mNumber,mName)=match[i]
        ParseXML(vyear,mNumber.replace('?',''),urllib.quote_plus(mName).replace('+',' '), mydoc,mlist)

    f = open(filename, 'w');f.write(mydoc.toprettyxml());f.close()

def GetDirVideoUrl(url,cj):
    if cj==None:
        cj = cookielib.LWPCookieJar()


    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):    
        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            print "redirecturl" + self.video_url
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    redirhndler = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(redirhndler,urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', url),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache')]
    #urllib2.install_opener(opener)
    usock=opener.open(url)
    return redirhndler.video_url


def Episodes(name,videoId):
    #try:
          match=re.compile("\/(.+?)&sp").findall(videoId+"&sp")
          if len(match)>=0:
                videoId=match[0]
          try:
                vidlink=GetDirVideoUrl(noobvideolink+"&tv=0"+"&start=0&file="+videoId,cj)+ "&loc="+location
          except:
                vidlink=GetDirVideoUrl(noobvideolink.replace("&hd="+isHD,"&hd=0")+"&tv=0"+"&start=0&file="+videoId,cj)+ "&loc="+location
          #vidlink="http://46.165.228.108/index.php?file=1871&start=0&hd=0&auth=&type=flv&tv=0"
          cookiestr =""
          for cookie in cj:
                cookiestr=cookiestr+('%s=%s;'%(cookie.name,cookie.value))
          fullvid= ('%s|Cookie="%s"' % (vidlink,cookiestr+"save=1") )
          fullvid= ('%s|User-Agent="%s"' % (fullvid,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0') )
          playVideo("noobroom",fullvid)


	

				
def ListTVSeries(cj):
    (cj,link) = GetContent(nooblink +"/series.php","",nooblink,cj)
    link = ''.join(link.splitlines()).replace('\'','"')
    match=re.compile('<table><tr><td><a href="(.+?)"><img style="border:0" src="(.+?)"></a>').findall(link)
    matchname=re.compile('<b><a style="color:#fff" href="(.+?)">(.+?)</a></b>').findall(link)
    for i in range(len(match)):
            addDir(matchname[i][1],nooblink+match[i][0],10,nooblink+"/"+match[i][1])

def ListEpisodes(url,cj):
    (cj,link) = GetContent(url,"",nooblink,cj)
    link = ''.join(link.splitlines()).replace('\'','"')
    match=re.compile('<br><b>(.+?)<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    cookiestr =""
    for cookie in cj:
            cookiestr=cookiestr+('%s=%s;'%(cookie.name,cookie.value))
    for i in range(len(match)):
            vidlink=noobvideolink.replace("&hd=1","&hd=0")+match[i][1].replace("/?","&file=")
            
            if(i==0):
                   vidlink=GetDirVideoUrl(vidlink,cj)+ "&loc="+location+"&hd=0"
            else:
                   vidlink=vidlink.replace(match[i-1][1].replace("/?","&file="),match[i][1].replace("/?","&file="))
            fullvid= ('%s|Cookie="%s"' % (vidlink,cookiestr+"save=1") )
            fullvid= ('%s|User-Agent="%s"' % (fullvid,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0') )
            addLink(match[i][0]+match[i][2],fullvid,3,"")

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

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
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
        liz=xbmcgui.ListItem('Next >', iconImage="http://noobroom.com/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://noobroom.com/logo.png", thumbnailImage=iconimage)
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
        formvar=int(params["formvar"])
except:
        pass		
	
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        GA("NONE","HOME")
        HOME()
       
elif mode==2:
        GA("NONE","INDEX")
        INDEXAZ(url) 
elif mode==3:
        playVideo("noobroom",url)
elif mode==4:
        SearchXml(url)
elif mode==5:
        SEARCH()
elif mode==6:
       Episodes(name,str(url))
elif mode==7:
       BuildXMl(cj)
elif mode==8:
       Last25()  
elif mode==9:
       ListTVSeries(cj)
elif mode==10:
       ListEpisodes(url,cj)
elif mode==11:
        GetLoginCookie(cj,cookiefile)
xbmcplugin.endOfDirectory(int(sysarg))
