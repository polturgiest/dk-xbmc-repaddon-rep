import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
try: import simplejson as json
except ImportError: import json
import cgi

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
        addDir('Hong Kong Series','http://www.thegioiphim.eu/',9,'http://www.thegioiphim.eu/images/logo.png')
        addDir('Japanese Series','http://yeuphim.net/movie-list.php?cat=78',2,'http://img.yeuphim.net/movie/thumb1/507147552_913437197.jpg')
        addDir('Korean Series','http://yeuphim.net/movie-list.php?cat=15',2,'http://img.yeuphim.net/movie/thumb1/307768252_968871912.jpg')
        addDir('Chinese Series','http://yeuphim.net/movie-list.php?cat=48',2,'http://img.yeuphim.net/movie/thumb1/209454570_431578655.jpg')
        addDir('Vietnamese Videos','http://yeuphim.net/movie-list.php?cat=16',2,'http://img.yeuphim.net/movie/thumb2/704748494_531915959.jpg')
        addDir('Vietnamese Comedy','http://yeuphim.net/movie-list.php?cat=17',2,'http://img.yeuphim.net/movie/thumb2/704748494_531915959.jpg')
        addDir('Ca Nhac','http://yeuphim.net/movie-list.php?cat=18',2,'http://img.yeuphim.net/movie/thumb2/704748494_531915959.jpg')
        addDir('Phong su - Thoi Su','http://yeuphim.net/movie-list.php?cat=50',2,'http://img.yeuphim.net/movie/thumb2/704748494_531915959.jpg')
        addDir('Cooking videos','http://yeuphim.net/movie-list.php?cat=51',2,'http://img.yeuphim.net/movie/thumb1/132693411_509434860.jpg')
        addDir('Children videos','http://yeuphim.net/movie-list.php?cat=52',2,'http://img.yeuphim.net/movie/thumb1/182738444.jpg')
        addDir('Martial arts Videos','http://www.yeuphim.net/movie-list.php?cat=34',2,'http://img.yeuphim.net/movie/thumb1/209454570_431578655.jpg')
        addDir('Chinese Action Films','http://www.yeuphim.net/movie-list.php?cat=20',2,'http://img.yeuphim.net/movie/thumb1/209454570_431578655.jpg')
        addDir('Chinese comedy','http://www.yeuphim.net/movie-list.php?cat=10',2,'http://img.yeuphim.net/movie/thumb1/396886694_103442932.jpg')
        addDir('Chinese Thrillers','http://www.yeuphim.net/movie-list.php?cat=27',2,'http://img.yeuphim.net/movie/thumb1/17036753_144339987.jpg')
        addDir('Chinese Drama','http://www.yeuphim.net/movie-list.php?cat=21',2,'http://img.yeuphim.net/movie/thumb1/209454570_431578655.jpg')
        addDir('Korean Action Films','http://www.yeuphim.net/movie-list.php?cat=44',2,'http://img.yeuphim.net/movie/thumb1/482396024_696771407.jpg')
        addDir('Korean comedy','http://www.yeuphim.net/movie-list.php?cat=45',2,'http://img.yeuphim.net/movie/thumb1/213708507_361790076.jpg')
        addDir('Korean Thrillers','http://www.yeuphim.net/movie-list.php?cat=46',2,'http://img.yeuphim.net/movie/thumb1/779188987_784611752.jpg')
        addDir('Korean Drama','http://www.yeuphim.net/movie-list.php?cat=47',2,'http://img.yeuphim.net/movie/thumb1/307768252_968871912.jpg')
        addDir('Animated videos','http://www.yeuphim.net/movie-list.php?cat=38',2,'http://img.yeuphim.net/movie/thumb1/939681617_855027886.jpg')
        addDir('Music Videos','http://www.yeuphim.net/movie-list.php?cat=39',2,'http://img.yeuphim.net/movie/thumb1/779388677.jpg')
        addDir('Funny Clips','http://www.yeuphim.net/movie-list.php?cat=40',2,'http://img.yeuphim.net/movie/thumb1/363.jpg')

homeLink="http://yeuphim.net/"
def INDEX(url):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<a title="(.+?)" href="(.+?)"><img src="(.+?)" width="100" border="0" class="thumb"></a>').findall(newlink)
        for vcontent in match:
            (vname,vurl, vimage)=vcontent
            addDir(vname.encode("utf-8"),homeLink+vurl,7,vimage)
        pagecontent=re.compile('<!-- newest video end -->(.+?)<!-- ads -->').findall(newlink)
        match5=re.compile('<span class="pagenum"><a href="(.+?)">(.+?)</a></span>').findall(pagecontent[1])
        for vpage in match5:
            (vurl,vname)=vpage
            addDir("page: " + vname.encode("utf-8"),vurl,2,"")
    except: pass

def INDEXes(url):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="list-movie-image"><a href="(.+?)" title="(.+?)"><img class="img" src="(.+?)"').findall(newlink)
        for vcontent in match:
            (vurl,vname,vimage)=vcontent
            addDir(vname.encode("utf-8"),"http://www.thegioiphim.eu/"+vurl,8,vimage)
        listalpha = re.compile('<div class="grid_8 omega" style=(.+?)<!-- end search -->').findall(newlink)
        alphabet=re.compile('<strong><a href="(.+?)">(.+?)</a></strong>').findall(listalpha[0])
        for alpage in alphabet:
            (vurl,vname)=alpage
            addDir(vname.encode("utf-8"),"http://www.thegioiphim.eu/"+vurl,9,"")
        pagenum = re.compile('<!-- page -->(.+?)<!-- end page -->').findall(newlink)
        num = re.compile('<span class="pagenum"><a href="(.+?)">(.+?)</a></span>').findall(pagenum[0])
        for alpagenum in num:
            (vurl,vname)=alpagenum
            addDir(vname.encode("utf-8"),vurl,9,"")
    except: pass
def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://yeuphim.net/movie-list.php?str='+ searchText
        INDEX(url)
    except: pass

def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<aclass="widget-title" href="(.+?)"><imgsrc="(.+?)" alt="(.+?)"').findall(newlink)
        if(len(match) >= 1):
                for vLink,vpic,vLinkName in match:
                    addDir(vLinkName,vLink,5,vpic)
        match=re.compile('<strong>&raquo;</strong>').findall(link)
        if(len(match) >= 1):
            startlen=re.compile("<strongclass='on'>(.+?)</strong>").findall(newlink)
            url=url.replace("/page/"+startlen[0]+"/","/page/"+ str(int(startlen[0])+1)+"/")
            addDir("Next >>",url,6,"")

def Mirrors(url,name):
    try:
        if(CheckRedirect(url)):
                MirrorsThe(name,url)
        else:
                link = GetContent(url)
                newlink = ''.join(link.splitlines()).replace('\t','')
                match=re.compile('<b>Episode list </b>(.+?)</table>').findall(newlink)
                mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">(.+?)</div>').findall(match[0])
                if(len(mirrors) >= 1):
                        for vLinkName in mirrors:
                            addDir(vLinkName.encode("utf-8"),url,5,'')

    except: pass
	
def MirrorsThe(name,url):
    link = GetContent(url)
    newlink = ''.join(link.splitlines()).replace('\t','')
    match=re.compile('>Phim Hong Kong<(.+?)</table>').findall(newlink)
    mirrors=re.compile('<div style="margin-top:10px; margin-bottom:5px">(.+?)</div>').findall(match[0])
    if(len(mirrors) >= 1):
        for vLinkName in mirrors:
            addDir(vLinkName.encode("utf-8"),url,10,'')
def Episodes2(url,name):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('>Phim Hong Kong<(.+?)</table>').findall(newlink)
        mirrors=re.compile('<div style="margin-top:10px; margin-bottom:5px">'+ name +'(.+?)<!-- mirror').findall(match[0])
        match1=re.compile('<a href="(.+?)"><strong class="moviered">(.+?)</strong></a>').findall(mirrors[0])
        if(len(match1) >= 1):
                for mcontent in match1:
                    vLink, vLinkName=mcontent
                    addLink("part - "+ vLinkName.strip().encode("utf-8"),homeLink+vLink,3,'',name)

    except: pass


def Episodes(url,name):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<b>Episode list </b>(.+?)</table>').findall(newlink)
        mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">'+ name +'(.+?)<div style="margin: 10px 0px 5px 0px">').findall(match[0])
        if(len(mirrors) == 0):
            mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">'+ name +'(.+?)<!-- Mirror').findall(match[0])
        match1=re.compile('<a href="(.+?)"><strong class="moviered">(.+?)</strong></a>').findall(mirrors[0])
        if(len(match1) >= 1):
                for mcontent in match1:
                    vLink, vLinkName=mcontent
                    addLink("part - "+ vLinkName.strip().encode("utf-8"),homeLink+vLink,3,'',name)

    except: pass

def Geturl(strToken):
        for i in range(20):
                try:
                        strToken=strToken.decode('base-64')
                except:
                        return strToken
                if strToken.find("http") != -1:
                        return strToken
def CheckRedirect(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return (second_response.get_url().find("www.thegioiphim.eu") > 0)
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	   
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def PostContent(url):
        try:
                net = Net()
                headers = {}
                headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                headers['Accept-Encoding'] = 'gzip, deflate'
                headers['Accept-Charset']='ISO-8859-1,utf-8;q=0.7,*;q=0.7'
                headers['Referer'] = 'http://yeuphim.net/'
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0.1) Gecko/20100101 Firefox/5.0.1'
                headers['Connection'] = 'keep-alive'
                headers['Host']='yeuphim.net'
                headers['Accept-Language']='en-us,en;q=0.5'
                headers['Pragma']='no-cache'
                formdata={}
                second_response = net.http_POST(url,formdata,headers=headers,compression=False)
                return second_response.content
        except:
                d = xbmcgui.Dialog()
                d.ok('Time out',"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)
        except:
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
        try:
           link=PostContent(url)
           newlink = ''.join(link.splitlines()).replace('\t','')
           match=re.compile("'file', '(.+?)'").findall(newlink)
           if(len(match) > 0):
                   if name.lower().find("dailymotion") != -1:
                           newlink=Geturl(match[0])
                   elif name.lower().find("youtube") != -1:
                           newlink="https://www.youtube.com/watch?v="+Geturl(match[0])
           else:
                   match=re.compile('<embed.+?src="(.+?)".+?').findall(newlink)
                   if(len(match) > 0):
                           newlink=match[0]+"&dk"
                   else:
                           d = xbmcgui.Dialog()
                           d.ok('Not Implemented','Sorry this video site is ',' not implemented yet')
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/swf/(.+?)&dk').findall(newlink)
                if(len(match) == 0):
                        link = newlink
                else:
                        link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('"sequence":"(.+?)"').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                playVideo('dailymontion',urllib2.unquote(dm_low[0]).decode("utf8"))
           elif (newlink.find("video.google.com") > -1):
                match=re.compile('http://video.google.com/videoplay.+?docid=(.+?)&.+?').findall(newlink)
                glink=""
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        playVideo('google',gcontent[0])
           elif (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')
           else:
                if (newlink.find("linksend.net") > -1):
                     d = xbmcgui.Dialog()
                     d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')
                newlink1 = urllib2.unquote(newlink).decode("utf8")+'&dk;'
                print 'NEW url = '+ newlink1
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('yeuphim.net',urllib2.unquote(newlink).decode("utf8"))
        except: pass
		
def extractFlashVars(data):
    flashvars = {}
    found = False
    pattern = "yt.playerConfig\s*=\s*({.*});"
    match = re.search(pattern, data)
    if match is None:
        return flashvars
    playerconfig =  json.loads(match.group(1))
    flashvars =  playerconfig['args']
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
        liz=xbmcgui.ListItem(name, iconImage="http://yeuphim.net/images/logo.png", thumbnailImage=iconimage)
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
        INDEX(url)
elif mode==3:
        print url
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       Episodes(url,name)
elif mode==6:
       SearchResults(url)
elif mode==7:
       Mirrors(url,name)
elif mode==8:
        MirrorsThe(name,url)
elif mode==9:
       INDEXes(url)
elif mode==10:
       Episodes2(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
