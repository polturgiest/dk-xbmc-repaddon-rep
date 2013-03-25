import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from xml.dom.minidom import Document

addon_id="plugin.video.NoobRoom"
__settings__ = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
tvfilename = xbmc.translatePath(os.path.join(home, 'resources', 'tvshow.xml'))
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	   

def GetNoobLink():
    link = GetContent("http://www.noobroom.com")
    match=re.compile('value="(.+?)">').findall(link)
    return match[0]

nooblink=GetNoobLink()

def GetVideoLink(url):
    link = GetContent(url)
    match=re.compile('"streamer": "(.+?)",').findall(link)

    return match[0]
	
noobvideolink=GetVideoLink(nooblink)

def HOME():
        addDir('Search','search',5,'')
        addDir('Movies A-Z','Movies',2,'')
        addDir('TV Shows','TV',9,'')
        addDir('Last 25 Added','Latest',8,'')
        addLink('Refresh Movie list','Refresh',7,'')

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
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    match=re.compile('<movie name="(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(25):
        (mName,mNumber,vyear)=match[i]
        addLink(mName,mNumber,6,"")
		
def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
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
	
def BuildXMl():
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Refreshing Movie List,5000)")
    link = GetContent(nooblink +"/latest.php")
    mydoc=Document()
    mlist = mydoc.createElement("movielist")
    mydoc.appendChild(mlist)
    match=re.compile('<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    for i in range(len(match)):
        (vyear,mNumber,mName)=match[i]
        ParseXML(vyear,mNumber.replace('?',''),urllib.quote_plus(mName).replace('+',' '), mydoc,mlist)

    f = open(filename, 'w');f.write(mydoc.toprettyxml());f.close()
	
def Episodes(name,videoId):
    try:
          match=re.compile("\/(.+?)&sp").findall(videoId+"&sp")
          if len(match)>=0:
                videoId=match[0]
          playVideo("noobroom",noobvideolink+"&start=0&file="+videoId+'|Referer="'+nooblink+'/player.swf'+'"')
          #addLink(name+"-Default Server",noobvideolink+"&start=0&file="+videoId+'|Referer="'+nooblink+'/player.swf'+'"',3,"")
          #addLink(name+"-Server 1","http://178.159.0.134/index.php?file="+videoId+'&start=0&hd=0&auth=0&type=flv|Referer="'+nooblink+'/player.swf'+'"',3,"")
          #addLink(name+"-Server 2","http://178.159.0.59/index.php?file="+videoId+'&start=0&hd=0&auth=0&type=flv|Referer="'+nooblink+'/player.swf'+'"',3,"")
          #addLink(name+"-Server 4","http://178.159.0.10/index.php?file="+videoId+'&start=0&hd=0&auth=0&type=flv|Referer="'+nooblink+'/player.swf'+'"',3,"")
          #addLink(name+"-Server 5","http://178.159.0.8/index.php?file="+videoId+'&start=0&hd=0&auth=0&type=flv|Referer="'+nooblink+'/player.swf'+'"',3,"")
    except: pass


def ListTVSeries():
    link = GetContent(nooblink +"/series.php")
    link = ''.join(link.splitlines()).replace('\'','"')
    match=re.compile('<table><tr><td><a href="(.+?)"><img style="border:0" src="(.+?)"></a>').findall(link)
    matchname=re.compile('<b><a style="color:#fff" href="(.+?)">(.+?)</a></b>').findall(link)
    for i in range(len(match)):
            addDir(matchname[i][1],nooblink+match[i][0],10,nooblink+"/"+match[i][1])
def ListEpisodes(url):
    link = GetContent(url)
    link = ''.join(link.splitlines()).replace('\'','"')
    match=re.compile('<br><b>(.+?)<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    for i in range(len(match)):
            addLink(match[i][0]+match[i][2],nooblink+match[i][2],3,"")

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
        HOME()
       
elif mode==2:
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
       BuildXMl()
elif mode==8:
       Last25()  
elif mode==9:
       ListTVSeries()
elif mode==10:
       ListEpisodes(url)
xbmcplugin.endOfDirectory(int(sysarg))
