import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import urlresolver
try: import simplejson as json
except ImportError: import json
import cgi

strdomain ='khmerportal.com'
def HOME():
        addDir('Chinese','/category/chinese/chinese-episode-1/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Korean Drama','/category/korean/korean-episode-1/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        addDir('Khmer Entertainment','/category/khmer-other-videos/khmer-other-videos-episode-1/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category12.jpg')
        addDir('Thai Lakorn','/category/thai/thai-episode-1/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category13.jpg')
        addDir('Search','/videos/categories',4,'')
        
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = '/?s=' + searchText
        INDEX(url)
        
def INDEX(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="nag cf">(.+?)<!-- end .loop-content -->').findall(newlink)
        if(len(match) >= 1):
                for mcontent in match:
                    quickLinks=re.compile('<a class="clip-link" data-id="(.+?)" title="(.+?)" href="(.+?)"><span class="clip"><img src="(.+?)" alt="(.+?)" />').findall(mcontent)
                    for vtmp1,vLinkName,vLink,vLinkPic,vtmp2 in quickLinks:
                        addDir(vLinkName.encode('string_escape'),vLink,5,vLinkPic)
        match=re.compile("<a (.+?) class=\"next\">&raquo;</a>").findall(link)
        if(len(match) >= 1):
                match=re.compile("href='(.+?)'").findall(match[0])
                nexurl= match[0]
                addDir('Next>',nexurl,2,'')
				
def Episodes(url,name):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile("<ul class='related_post'>(.+?)</ul></div>").findall(newlink)
        if(len(match) >= 1):
                linkmatch=re.compile("<li><a href='(.+?)' title='(.+?)'>(.+?)</a></li>").findall(match[0])
                for vpic in linkmatch:
                        (vurl,vname,vtmp3)=vpic
                        addLink(vname.encode('string_escape'),vurl,3,"")
                addLink(name.encode('string_escape'),url,3,"")
    except: pass
	
def GetCookie():
     response = ClientCookie.urlopen("http://www.khmerportal.com/")
     print response

def GetContent(url):
    conn = httplib.HTTPConnection(host=strdomain,timeout=30)
    req = url.replace('http://'+strdomain,'')
    try:
        conn.request('GET',req)
    except:
        print 'echec de connexion'
    content = conn.getresponse().read()
    conn.close()
    return content

def playVideo(videoType,videoId):
    url = videoId
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
        except:
                url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)
	
def loadVideos(url,name):
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
                link=GetContent(url)
                link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        #try:
                newlink = re.compile('"setMedia", {(.+?):"(.+?)"').findall(link)
                if(len(newlink) > 0):
                        (vtmp1,vlink)=newlink[0]
                else:
                        newlink = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        vlink=newlink[0]
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(vlink)
                if(len(match) > 0):
                        lastmatch = match[0][len(match[0])-1].replace('v/','')
                        playVideo('youtube',lastmatch)
                else:
                        sources = []
                        label=name
                        hosted_media = urlresolver.HostedMediaFile(url=vlink, title=label)
                        sources.append(hosted_media)
                        source = urlresolver.choose_source(sources)
            
                        if source:
                              print "in source"
                              vidlink = source.resolve()
                        else:
                              vidlink =vlink
                        print "vidlink" + vidlink
                        playVideo('khmerportal',urllib2.unquote(vidlink).decode("utf8"))
        #except: pass

def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response

def extractFlashVars(data):
        flashvars = {}
        found = False

        for line in data.split("\n"):
            if line.strip().startswith("var swf = \""):
                found = True
                p1 = line.find("=")
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                    continue
                data = line[p1 + 1:p2]
                break

        if found:
            data = json.loads(data)
            data = data[data.find("flashvars"):]
            data = data[data.find("\""):]
            data = data[:1 + data[1:].find("\"")]

            for k, v in cgi.parse_qs(data).items():
                flashvars[k] = v[0]

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
				
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://d3v6rrmlq7x1jk.cloudfront.net/templates/rt_iridium_j15/images/style2/logo.png", thumbnailImage=iconimage)
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
		
sysarg=str(sys.argv[1]) 		
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        INDEX(url)
        
elif mode==3:
        loadVideos(url,name)
elif mode==4:
        SEARCH(url) 
elif mode==5:
        print "in episode"
        Episodes(url,name)       
elif mode==8:
        PAGES(url)

xbmcplugin.endOfDirectory(int(sysarg))
