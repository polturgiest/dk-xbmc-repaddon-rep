import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
import xbmcaddon,xbmcplugin,xbmcgui
#from t0mm0.common.net import Net

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
        try:
                newlink = re.compile('"setMedia", {(.+?):"(.+?)"').findall(link)
                if(len(newlink) > 0):
                        (vtmp1,vlink)=newlink[0]
                else:
                        newlink = re.compile('<iframe [^>]*src="(.+?)" frameborder="0" allowfullscreen>').findall(link)
                        vlink=newlink[0]
                print vlink
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(vlink)
                if(len(match) > 0):
                        lastmatch = match[0][len(match[0])-1].replace('v/','')
                        playVideo('youtube',lastmatch)
                else:
                        playVideo('khmerportal',urllib2.unquote(vlink).decode("utf8"))
        except: pass
        
def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response

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
