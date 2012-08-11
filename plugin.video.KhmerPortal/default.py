import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
import xbmcaddon,xbmcplugin,xbmcgui
#from t0mm0.common.net import Net

strdomain ='www.khmerportal.com'
def HOME():
        addDir('Videos about Cambodia','/videos/viewcategory/38/cambodia',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category38.jpg')
        addDir('Chinese','/videos/viewcategory/29/chinese',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Japanese Drama','/videos/viewcategory/25/japanese-drama',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category25.jpg')
        addDir('Korean Drama','/videos/viewcategory/21/korean-drama',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        addDir('Cars & Vehicles','/videos/viewcategory/1/cars-a-vehicles',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category1.jpg')
        addDir('Khmer Cooking','/videos/viewcategory/15/khmer-cooking',2,'http://img.youtube.com/vi/p-LmXztN3d8/default.jpg')
        addDir('Khmer Entertainment','/videos/viewcategory/12/khmer-entertainment',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category12.jpg')
        addDir('Khmer Surin','/videos/viewcategory/40/khmer-surin',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category40.jpg')
        addDir('Thai Lakorn','/videos/viewcategory/13/thai-lakorn',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category13.jpg')
        addDir('Search','/videos/categories',4,'')
        
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = '/videos/displayresults/0?pattern=' + searchText + '&rpp=0&sort=0&ep=&ex='
        INDEX(url)
        
def INDEX(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="listThumbnail" >(.+?)</div>').findall(newlink)
        if(len(match) >= 1):
                for mcontent in match:
                    quickLinks=re.compile('<a href="(.+?)" ><span class="hasTip" title="(.+?)"><img src="(.+?)"').findall(mcontent)
                    for vLink, vLinkName,vLinkPic in quickLinks:
                        addLink(vLinkName,vLink,3,vLinkPic)
        match=re.compile('<div class="page-inactive"><a href="(.+?)" title="Next">').findall(link)
        if(len(match) >= 1):
            print 'matches' +str(match[0])
            nexurl= match[0]
            addDir('Next>',nexurl,2,'')
                        
def GetCookie():
     response = ClientCookie.urlopen("http://www.khmerportal.com/")
     print response

def GetContent(url):
    conn = httplib.HTTPConnection(host=strdomain,timeout=30)
    req = url
    try:
        conn.request('GET',req)
    except:
        print 'echec de connexion'
    content = conn.getresponse().read()
    conn.close()
    return content

def playVideo(videoType,videoId):
    url = ""
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    elif (videoType == "khmerportal"):
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
	
def loadVideos(url,name):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
        link=GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        
        #khmerportal
        try:
                newlink = re.compile('allowfullscreen="true" flashvars="file=(.+?)&amp;linktarget=_blank').findall(link)
                newlink1 = urllib2.unquote(newlink[0]).decode("utf8")+'&dk;'
                print 'NEW url = '+ newlink1 
                match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                print match
                if(len(match) > 0):
                    playVideo('youtube',match[0])
                else:
                    playVideo('khmerportal',urllib2.unquote(newlink[0]).decode("utf8"))
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
        
elif mode==8:
        PAGES(url)

xbmcplugin.endOfDirectory(int(sysarg))
