import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from xml.dom.minidom import Document
import urlresolver

__settings__ = xbmcaddon.Addon(id='plugin.video.AsianHorror')
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'horrormovies.xml'))
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	   
def HOME():
        addDir('Search','search',5,'')
        addDir('Movies A-Z','Movies',2,'')
        addDir('Latest','http://asian-horror-movies.com/',8,'')
        addDir('Get Movies by Country','Country',9,'')
        addLink('Refresh Movie list','http://asian-horror-movies.com/indexm.html',7,'')

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
        
def Latest(url):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<img src="http://asian-horror-movies.com/images/new0.png" (.+?)<img src="http://asian-horror-movies.com/12.jpg"').findall(newlink)
        match2=re.compile('<a href="(.+?)">(.+?)</a></font>').findall(match[0])
        for vcontent in match2:
            (vurl,vname)=vcontent
            addDir(vname.encode("utf-8"),vurl,6,"")

    except: pass
		
def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    if SearchText=='-1':
        match=re.compile('<movie name="[^A-Za-z](.+?)" url="(.+?)"/>', re.IGNORECASE).findall(text)	
        SearchText=""
    else:
        match=re.compile('<movie name="' + SearchText + '(.+?)" url="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(len(match)):
        (mName,mNumber)=match[i]
        addDir(SearchText+mName,mNumber,6,"")
		
def ParseXML(startlen,endlen,vcontent, doc, mlist):
    link=vcontent[startlen:endlen]
    match=re.compile('<li><a href="(.+?)">(.+?)</a>').findall(link)
    for vcontent in match:
        (vurl,vname)=vcontent
        movie= doc.createElement("movie")
        mlist.appendChild(movie)
        movie.setAttribute("name", vname)
        movie.setAttribute("url", vurl)
	
def BuildXMl(url):
    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Refreshing Movie List,5000)")
    link = GetContent(url)
    newlink = ''.join(link.splitlines()).replace('\t','')
    newlink=newlink[newlink.find('<b>Scroll Down To View Full Movie List</b>'):len(newlink)]
    mydoc=Document()
    mlist = mydoc.createElement("movielist")
    mydoc.appendChild(mlist)
    
    match=re.compile('<strong>(.+?)</strong><br /><img src="(.+?)" width="75" height="75" align="center" />').findall(newlink)
    maxcountry = len(match)

    for i in range(maxcountry):
        (vCountry,vImg)=match[i]
        xCountry= mydoc.createElement("country")
        mlist.appendChild(xCountry)
        xCountry.setAttribute("thumb", vImg)
        xCountry.setAttribute("name", vCountry)
        startlen = newlink.find('<strong>'+vCountry+'</strong><br /><img')
        endlen = 0
        if(i < maxcountry-1):
                (vCountry2,vImg2)=match[i+1]
                endlen=newlink.find('<strong>'+vCountry2+'</strong><br /><img')
        else:
                endlen = len(newlink)
        ParseXML(startlen,endlen,newlink, mydoc,xCountry)
    print mydoc.toprettyxml()
    f = open(filename, 'w');f.write(mydoc.toprettyxml());f.close()
	
def GetCountryMovies(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    text=''.join(text.splitlines()).replace('\t','')
    cmatch=re.compile('<country name="'+SearchText.replace("(","\(").replace(")","\)")+'" thumb="(.+?)">(.+?)</country>', re.IGNORECASE).findall(text)
    match=re.compile('<movie name="(.+?)" url="(.+?)"/>', re.IGNORECASE).findall(cmatch[0][1])
    for i in range(len(match)):
        (mName,mNumber)=match[i]
        addDir(mName,mNumber,6,"")

def GetCountry():
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    text=''.join(text.splitlines()).replace('\t','')
    cmatch=re.compile('<country name="(.+?)" thumb="(.+?)">', re.IGNORECASE).findall(text)
    for i in range(len(cmatch)):
        (mName,mImg)=cmatch[i]
        addDir(mName,"",10,mImg)
		
def Episodes(url,name):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
        mirrorctr = 0
        if(len(match)):
                for pcontent in match:
                        print "embed match"
                        mirrorctr= mirrorctr+1
                        addLink(name +" mirror "+ str(mirrorctr),pcontent,3,"") 
        match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
        if(len(match)):
                for pcontent in match:
                        print "iframe match"
                        mirrorctr= mirrorctr+1
                        addLink(name +" mirror "+ str(mirrorctr),pcontent,3,"") 
        match=re.compile("'flashvars','&file=(.+?)'").findall(link)
        if(len(match)):
                for pcontent in match:
                        print "vars match"
                        mirrorctr= mirrorctr+1
                        addLink(name +" mirror "+ str(mirrorctr),pcontent,3,"") 
        match=re.compile('onclick="window.open\(\'(.+?)\'', re.IGNORECASE).findall(link)
        if(len(match)):
                for pcontent in match:
                        print "part match"
                        mirrorctr= mirrorctr+1
                        vmode = 3
                        partnum = name.split(' part ')
                        name=name.replace(' part '+ str(len(partnum)),'')
                        if(pcontent.find(".php") > 0):
                                if(pcontent.find("asian-horror-movies.com") > 0):
                                        addDir(name +" part " + str(len(partnum)+1),pcontent,6,"")
                        else:
                                addLink(name +" mirror "+ str(mirrorctr),pcontent,3,"")
        match=re.compile('<a href="(.+?)">CLICK FOR', re.IGNORECASE).findall(link)
        if(len(match)):
                for pcontent in match:
                        print "part match"
                        mirrorctr= mirrorctr+1
                        vmode = 3
                        partnum = name.split(' part ')
                        name=name.replace(' part '+ str(len(partnum)),'')
                        if(pcontent.find(".php") > 0):
                                if(pcontent.find("asian-horror-movies.com") > 0):
                                        addDir(name +" part " + str(len(partnum)+1),pcontent,6,"")
                        else:
                                addLink(name +" mirror "+ str(mirrorctr),pcontent,3,"") 

    except: pass  



def PlayUrlSource(url,name):
 try:
    xbmc.executebuiltin("XBMC.Notification(if this mirror is a trailer,try another mirror,5000)")
    match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(url)
    if(len(match) > 0):
        lastmatch = match[0][len(match[0])-1].replace('v/','')
        playVideo('youtube',lastmatch)
        url1 = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + lastmatch.replace('?','')
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=url1, listitem=liz)
    else:
        sources = []
        #try:
        label=name
        hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
        sources.append(hosted_media)
        #except:
        print 'Error while trying to resolve %s' % url

        source = urlresolver.choose_source(sources)
        print "source info=" + str(source)
        if source:
                stream_url = source.resolve()
                print 'Attempting to play url: %s' % stream_url
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                listitem = xbmcgui.ListItem(label, iconImage="", thumbnailImage="")
                playlist.add(url=stream_url, listitem=listitem)
                xbmc.Player().play(playlist)
 except: pass 
		
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
        liz=xbmcgui.ListItem('Next >', iconImage="http://asian-horror-movies.com/images/logogg.gif", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://asian-horror-movies.com/images/logogg.gif", thumbnailImage=iconimage)
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
if mode==None:
        HOME()
elif mode==2:
        INDEXAZ(url) 
elif mode==3:
        PlayUrlSource(url,name)
elif mode==4:
        SearchXml(url)
elif mode==5:
        SEARCH()
elif mode==6:
       Episodes(url,name)
elif mode==7:
       BuildXMl(url)
elif mode==8:
       Latest(url)
elif mode==9:
       GetCountry()
elif mode==10:
       GetCountryMovies(name)
xbmcplugin.endOfDirectory(int(sysarg))
