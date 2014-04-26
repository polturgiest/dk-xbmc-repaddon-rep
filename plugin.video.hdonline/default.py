import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
from xml.dom.minidom import Document
import datetime
import HTMLParser

addonid='plugin.video.hdonline'
ADDON=__settings__ = xbmcaddon.Addon(id=addonid)

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "hdonline"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.0" #<---- PLUGIN VERSION

home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'sub.srt'))
sublang = ADDON.getSetting('sublang')
strdomain ="http://hdonline.vn"
enableSubtitle=ADDON.getSetting('enableSub')
enableProxy= ADDON.getSetting('enableProxy')
reg_list = ["http://webcache.googleusercontent.com/search?q=cache:*url*"]
proxyurl = reg_list[int(ADDON.getSetting('region'))]

try: 
        from sqlite3 import dbapi2 as database
        print 'Loading sqlite3 as DB engine'
except: 
        from pysqlite2 import dbapi2 as database
        addon.log('pysqlite2 as DB engine')
DB = 'sqlite'
db_dir = os.path.join(xbmc.translatePath("special://database"), 'hdonline.db')

def initDatabase():
    if DB != 'mysql':
        if not os.path.isdir(os.path.dirname(db_dir)):
            os.makedirs(os.path.dirname(db_dir))
        db = database.connect(db_dir)
        db.execute('CREATE TABLE "medias" ("media_id" INTEGER NOT NULL  UNIQUE , "media_name" VARCHAR, "media_type" VARCHAR, "media_url" VARCHAR PRIMARY KEY  NOT NULL , "mscinfo" VARCHAR, "addonid" VARCHAR, "imgurl" VARCHAR, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
        db.execute('CREATE TABLE "episodes" ("epi_id" VARCHAR PRIMARY KEY  NOT NULL, "epi_name" VARCHAR, "sub_url", "epi_desc" VARCHAR, "epi_img" VARCHAR, "media_id" INTEGER, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
        db.execute('CREATE TABLE "videolinks" ("vid_id" INTEGER NOT NULL ,"vid_domain" VARCHAR,"vid_img" VARCHAR,"vid_url" VARCHAR PRIMARY KEY  NOT NULL ,"isbroken" BOOL DEFAULT (0) ,"update_dt" DATETIME DEFAULT (CURRENT_TIMESTAMP) ,"epi_id" INTEGER, "referer_url" VARCHAR)')
        db.execute('CREATE TABLE "groupings" ("grp_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "grp_name" VARCHAR, "media_id" INTEGER, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
    db.commit()
    db.close()

def SaveData(SQLStatement): #8888
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
        db = database.connect( db_dir )
    cursor = db.cursor()
    cursor.execute(SQLStatement)
    db.commit()
    db.close()
	
def buildMovieInsertSQl(vidurl,vidname,vidtype,vidimg,vplot,parenturl,tablename,referer_url,isbroken=0):
    strSQL=""
    try:
         vidname= vidname.encode("utf-8")
    except: pass
    try:
         vidurl= vidurl.encode("utf-8")
    except: pass
    if(tablename=="media"):
         strSQL='INSERT OR REPLACE INTO medias(media_id, media_url,media_name,media_type,imgurl,addonid,update_dt)VALUES ("%s","%s","%s","%s","%s","%s",CURRENT_TIMESTAMP );' %(vidurl,vidurl,vidname,vidtype,vidimg,addonid)
    elif(tablename=="episodes"):
         strSQL='INSERT OR REPLACE INTO episodes(epi_id, sub_url,epi_name,epi_desc,media_id,update_dt)VALUES ("%s","%s","%s","%s","%s",CURRENT_TIMESTAMP );' %(vidurl,vidimg,vidname,vplot,parenturl)
    elif(tablename=="groupings"):
         strSQL='INSERT OR REPLACE INTO groupings(grp_name, media_id,update_dt)VALUES ("%s",(SELECT media_id FROM medias WHERE media_url = "%s"),CURRENT_TIMESTAMP );' %(vidname,vidurl)
    elif(tablename=="groupings2"):
         strSQL='INSERT OR REPLACE INTO groupings(grp_name, media_id,update_dt)VALUES ("%s",(select media_id from episodes where epi_id="%s"),CURRENT_TIMESTAMP );' %(vidname,vidurl)
    #think of how to group video parts.
    elif(tablename=="videolinks"):
         strSQL='INSERT OR REPLACE INTO videolinks(vid_id, vid_url,vid_domain,vid_img,epi_id,referer_url,update_dt,isbroken)VALUES (COALESCE((SELECT vid_id FROM videolinks WHERE vid_url = "%s"), (SELECT COALESCE((select MAX(vid_id) from videolinks), 0) + 1)),"%s","%s","%s","%s","%s",CURRENT_TIMESTAMP,%s );' %(vidurl,vidurl,vidname,vidimg,parenturl,referer_url,isbroken)
    try:
         strSQL= strSQL.encode("utf-8")
    except: pass
    #print strSQL
    return strSQL
	
def SaveMovieTVshow(vname,vurl,vimg,vtype):
        SaveData(buildMovieInsertSQl(vurl,vname,vtype,vimg,"","","media",vurl))
		
def SaveEpisodes(vname,vurl,vimg,parenturl):
        SaveData(buildMovieInsertSQl(vurl,vname,"",vimg,"",parenturl,"episodes",parenturl))
		
def SaveVideoLink(vname,vurl,vimg,parenturl):
        SaveData(buildMovieInsertSQl(vurl,vname,"",vimg,"",parenturl,"videolinks",parenturl))
def SaveGroupings(vname,vurl,type):
        SaveData(buildMovieInsertSQl(vurl,vname,"","","","",type,""))
		
def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def GetContentMob(url):
    opener = urllib2.build_opener()
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',"http://m.hdonline.vn/"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','www.phimmobile.com')]
    usock = opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response
	
def GetContent(url, useProxy=False):
    strresult=""
    if useProxy==True:
        url = proxyurl.replace("*url*",urllib.quote_plus(url))
        print "use proxy:" + str(useProxy) + url
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', 'http://hdonline.vn/')
        response = urllib2.urlopen(req, timeout=360)
        strresult=response.read()
        response.close()
    except Exception, e:
       print str(e)+" |" + url
    return strresult

def write2srt(url, fname):
    try:
          subcontent=GetContent(url).encode("utf-8")
    except:
          subcontent=GetContent(url)
    subcon=re.compile('vplugin\*\*\*(.+?)&').findall(subcontent+"&")
    if(len(subcon)>0):
          subcontent=decodevplug(subcon[0]).decode('base-64')
    f = open(fname, 'w');f.write(subcontent);f.close()

def json2srt(url, fname):

    data = json.load(urllib2.urlopen(url))['subtitles']

    def conv(t):
        return '%02d:%02d:%02d,%03d' % (
            t / 1000 / 60 / 60,
            t / 1000 / 60 % 60,
            t / 1000 % 60,
            t % 1000)

    with open(fname, 'wb') as fhandle:
        for i, item in enumerate(data):
            fhandle.write('%d\n%s --> %s\n%s\n\n' %
                (i,
                 conv(item['start_time']),
                 conv(item['end_time']),
                 item['content'].encode('utf8')))
def HOME():
        #addDir('Search channel','search',5,'')

        useProxy=(enableProxy=="true")
        link = GetContent("http://hdonline.vn/",useProxy)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        addDir("Search","http://hdonline.vn/tim-kiem/superman.html",5,"")
        addDir("View Cached Videos","http://hdonline.vn/",7,"")
        addDir("New Movies","http://hdonline.vn/danh-sach/phim-moi.html",2,"")
        vidcontentlist=re.compile('<div class="menus">\s*<span class="title">(.+?)</span>\s*<ul class="mn mnfl">(.+?)</ul>').findall(link)
        for mainname,vidcontent in vidcontentlist:
            addLink(mainname,"",0,'')
            vidlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(vidcontent)
            for vurl,vname in vidlist:
                 addDir("--"+vname,vurl,2,"")

if os.path.exists(db_dir)==False:
	initDatabase()

def HOMEMob():
        #addDir('Search channel','search',5,'')
        addDir('Search Videos','search',12,'')
        link = GetContent("http://m.hdonline.vn//?noscript=true")
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        vidcontentlist=re.compile('<div id="fnNav" class="sidebar none">(.+?)<div class="s-footer">').findall(link)
        if(len(vidcontentlist)>0):
             mainnavcontent=re.compile('<ul class="navigator">(.+?)</ul>').findall(vidcontentlist[0])
             if(len(mainnavcontent)>0):
                     mainnavitem=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(mainnavcontent[0])
                     for vurl,vname in mainnavitem:
                           addDir(vname,vurl,2,'')
        mainnavcontent=re.compile('<div class="glist">(.+?)</div>').findall(vidcontentlist[0])
        for glistcontent in mainnavcontent:
                     mainnavitem=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(glistcontent)
                     mainnavnames=re.compile('<h3 class="stitle">(.+?)</h3>').findall(glistcontent)
                     addLink(mainnavnames[0],"",0,"")
                     for vurl,vname in mainnavitem:
                           addDir("-----"+vname,vurl,2,'')


def decodevplug(_arg_1):
            import math
            _local_2 = "";
            _local_3 = list("1234567890qwertyuiopasdfghjklzxcvbnm")
            _local_4= len(_local_3)
            strlen=len(_arg_1)
            _local_5= list("f909e34e4b4a76f4a8b1eac696bd63c4")
            _local_6 = list(_arg_1[((_local_4 * 2) + 32):strlen])
            _local_7= list(_arg_1[0:(_local_4 * 2)])
            _local_8= []
            _local_9= _arg_1[((_local_4 * 2) + 32):strlen]
            _local_10 = 0
            while (_local_10 < (_local_4 * 2)):
                _local_11 = (_local_3.index(_local_7[_local_10]) * _local_4)
                _local_11 = (_local_11 + _local_3.index(_local_7[(_local_10 + 1)]))
                idx= int(math.floor((_local_10 / 2)) % len(_local_5))
                str(_local_5[idx])[0]
                _local_11 = (_local_11 - ord(str(_local_5[idx])[0]))
                _local_8.append(chr(_local_11))
                _local_10 = (_local_10 + 2)
				
            _local_10 = 0
            while (_local_10 < len(_local_6)):
                _local_11 = (_local_3.index(_local_6[_local_10]) * _local_4)
                _local_11 = (_local_11 + _local_3.index(_local_6[(_local_10 + 1)]))
                idx= int((math.floor((_local_10 / 2)) % _local_4))
                _local_11 = (_local_11 - ord(str(_local_8[idx])[0]))
                _local_2 = (_local_2 + chr(_local_11))
                _local_10 = (_local_10 + 2)

            return _local_2
			
def INDEXCache():
    sql = 'SELECT distinct media_name,imgurl,medias.media_id FROM medias inner join episodes on episodes.media_id = medias.media_id where addonid=? order by medias.update_dt desc' 

    db = database.connect(db_dir)
    cur = db.cursor()

    cur.execute(sql, (addonid,))
    favs = cur.fetchall()
    totalvideos = 0
    for row in favs:
        totalvideos=totalvideos+1
        try:
            media_name = row[0].encode("UTF-8")
        except:
            media_name = row[0]
        imgurl   = row[1].replace(" ","%20")
        media_id   = row[2]
        #print media_name+"+" +str(media_id)+"+"+imgurl
        addDir(media_name,str(media_id),8,imgurl)
    db.close()

def EpisodesCache(media_id,name):
    sql = 'SELECT epi_name,vid_url,sub_url,epi_desc, ifnull(vid_img,"") as epi_img FROM videolinks inner join episodes on episodes.epi_id = videolinks.epi_id where episodes.media_id = ? order by episodes.epi_id' 
    db = database.connect(db_dir)
    cur = db.cursor()

    cur.execute(sql, (media_id,))
    favs = cur.fetchall()
    totalcnt = 0
    
    for row in favs:
        totalcnt=totalcnt+1
        try:
            media_name = row[0].encode("UTF-8")
        except:
            media_name = row[0]
        media_url   = row[1].replace(" ","%20")
        suburl= row[2]
        imgurl   = row[4]
        addLinkSub(media_name,media_url,3,imgurl,suburl)
    db.close()
	
def Index(url,name):
        useProxy=(enableProxy=="true")
        link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        vidcontentlist=re.compile('<ul class="clearfix listmovie">(.+?)</ul>').findall(link)
        if(len(vidcontentlist)>0):
			movielist=re.compile('<img [^>]*data-original=["\']?([^>^"^\']+)["\']?[^>]*>\s*<div class="meta_block_spec" style="bottom:10px">\s*<h1 class="title"><a href="(.+?)" title="(.+?)">').findall(vidcontentlist[0])
			for vimg,vurl,vname in movielist:
				vidid=vurl.split("-")[-1].replace('.html','')
				SaveMovieTVshow(vname,vidid,vimg,"")
				addDir(vname,vidid,4,vimg)
        pagecontent=re.compile('<div class="load-more">(.+?)</div>').findall(link)
        if(len(pagecontent)>0):
			pagelist=re.compile('<span><a class="pagelink" href="(.+?)" >(.+?)</a></span>').findall(pagecontent[0])
			for vurl,vname in pagelist:
				addDir("page "+vname,vurl,2,"")



def Episodes(vidid,name):
        url="http://hdonline.vn/vxml.php?film="+vidid
        link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        episodelist=re.compile('<item>(.+?)</item>').findall(link)
        epid="0"
        for episodecontent in episodelist:
             vurl=decodevplug(re.compile('<jwplayer:file>(.+?)</jwplayer:file>').findall(episodecontent)[0])
             vname=re.compile('<title>(.+?)</title>').findall(episodecontent)[0]
             vimg=decodevplug(re.compile('<jwplayer:vplugin.image>(.+?)</jwplayer:vplugin.image>').findall(episodecontent)[0])
             vsubtitle=re.compile('<jwplayer:vplugin.subfile>(.+?)</jwplayer:vplugin.subfile>').findall(episodecontent)
             epid=re.compile("<jwplayer:vplugin.episodeid>(.+?)</jwplayer:vplugin.episodeid>").findall(episodecontent)
             suburl=""
             h = HTMLParser.HTMLParser()
             #print h.unescape(vname.encode("UTF-8"))
             if(len(vsubtitle)>0):
                 suburl=decodevplug(vsubtitle[0])
             if(len(epid)>0):
                 epid=epid[0]
             SaveEpisodes(h.unescape(vname).encode("UTF-8"),epid,suburl,vidid)
             SaveVideoLink(h.unescape(vname).encode("UTF-8"),vurl,vimg,epid)
             addLinkSub(h.unescape(vname).encode("UTF-8"),vurl,3,vimg,suburl)



def SEARCHVideos():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="http://hdonline.vn/tim-kiem/"+searchText+".html"
        Index(searchurl,searchText.lower())



def playVideo(suburl,videoId):
        print videoId
        vidinfo = videoId.split("_")[0]
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', vidinfo)
        win.setProperty('1ch.playing.season', str(3))
        win.setProperty('1ch.playing.episode', str(4))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        xbmcPlayer.setSubtitles(suburl) 



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
	
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

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

def playVideoPart(suburl,videoId,subfilepath):
        try:
                  json2srt(suburl, subfilepath)
        except:  
                  f = open(filename, 'w');f.write("");f.close()
        vidurl=getVideoUrl(videoId,"")
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidurl)
        xbmcPlayer.setSubtitles(subfilepath)

def addLinkSub(name,url,mode,iconimage,suburl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&suburl="+urllib.quote_plus(suburl)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
    	
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
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
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
subtitleurl=None
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
try:
        subtitleurl=urllib.unquote_plus(params["suburl"])
except:
        pass

print "mode is:"+ str(mode)
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        GA("Home","Home")
        HOME()
elif mode==2:
        Index(url,name) 
elif mode==3:
        if(enableSubtitle=="true"):
           sublist=subtitleurl.split(",")
           if(len(sublist)>1):
               subtitleurl=sublist[int(sublang)]
           else:
               subtitleurl=sublist[0]
        else:
           subtitleurl=""
        write2srt(subtitleurl,filename)
        playVideo(filename,url)
elif mode==4:
        Episodes(url,name)
elif mode==5:
        SEARCHVideos()
elif mode==6:
        GA("Genre",name)
        Genre(url,name)
elif mode==7:
        INDEXCache()
elif mode==8:
        EpisodesCache(url,name)



xbmcplugin.endOfDirectory(int(sysarg))
