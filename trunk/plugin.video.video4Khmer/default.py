import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui


def HOME():
        addDir('Search','http://www.video4khmer.com/',4,'http://www.video4khmer.com/templates/3column/images/header/logo.png')
        addDir('Thai Lakorns','http://www.video4khmer.com/browse-thai-lakhorn-dubbed-khmer-online-free-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Thai Movies','http://www.video4khmer.com/browse-thai-movies-dubbed-khmer-online-free-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Korean Videos','http://www.video4khmer.com/browse-korean-drama-dubbed-khmer-online-free-videos-1-date.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/04/lietome.jpg')
        addDir('Chinese Drama','http://www.video4khmer.com/browse-chinese-drama-dubbed-khmer-online-free-videos-1-date.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/05/rosemartial.jpg')
        addDir('Chinese Movies','http://www.video4khmer.com/browse-chinese-movies-dubbed-khmer-online-free-videos-1-date.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/05/rosemartial.jpg')
        addDir('Khmer Videos','http://www.video4khmer.com/browse-khmer-drama-watch-online-free-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Movies','http://www.video4khmer.com/browse-khmer-movies-watch-online-free-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Comedy','http://www.video4khmer.com/browse-khmer-comedy-watch-online-free-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Boxing','http://www.video4khmer.com/browse-khmer-boxing-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Hang Meas Karaoke','http://www.video4khmer.com/browse-hang-meas-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Sunday Khmer Karaoke','http://www.video4khmer.com/browse-sunday-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Town Production Karaoke','http://www.video4khmer.com/browse-town-production-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Big Man Khmer Karaoke','http://www.video4khmer.com/browse-big-man-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('M Production Karaoke','http://www.video4khmer.com/browse-m-production-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Rock Production Karaoke','http://www.video4khmer.com/browse-rock-production-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Spark Production Karaoke','http://www.video4khmer.com/browse-spark-production-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Chenla Brother Karaoke','http://www.video4khmer.com/browse-chenla-brother-khmer-video-karaoke-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer video clip','http://www.video4khmer.com/browse-khmer-clips-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('MISC','http://www.video4khmer.com/browse-this-and-that-accident-society-misc-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Tv show','http://www.video4khmer.com/browse-watch-cambodia-tv-shows-online-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Funney Videos','http://www.video4khmer.com/browse-funny-video-clips-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')		
def INDEX(url):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div id="list_subcats"><ul>(.+?)</ul>').findall(newlink)
        listcontent=re.compile('<a href="(.+?)">(.+?)</a>').findall(match[0])
        for vcontent in listcontent:
            (vurl,imgcontent)=vcontent
            titlecontent = re.compile('<img style=\'(.+?)\' class=imag src=(.+?)title="(.+?)" />').findall(imgcontent)
            if(len(titlecontent)):
                    (tmpvar,vimage,vname)=titlecontent[0]
                    addDir(vname.encode("utf-8"),vurl,5,vimage)
        match5=re.compile('<div class="pagination">(.+?)</div></div>').findall(newlink)
        if(len(match5)):
                pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match5[0])
                for pcontent in pages:
                        (pageurl,pagenum)=pcontent
                        addDir("Page " + pagenum,"http://www.video4khmer.com/"+pageurl,2,"")
    except: pass
			
def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.video4khmer.com/search.php?keywords='+ searchText +'&btn=Search'
        SearchResults(url)
        
def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div id="browse_results"><ul>(.+?)</ul></div>').findall(newlink)
        if(len(match) >= 1):
                linkmatch=re.compile('<a href="(.+?)"><img src="(.+?)"  alt="(.+?)" class="imag" width[^>]*').findall(match[0])
                for vLink,vpic,vLinkName in linkmatch:
                    addLink(vLinkName,vLink,3,vpic)
        match5=re.compile('<div class="pagination">(.+?)</div></div>').findall(newlink)
        if(len(match5)):
                pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match5[0])
                for pcontent in pages:
                        (pageurl,pagenum)=pcontent
                        addDir("Page " + pagenum,"http://www.video4khmer.com/"+pageurl,6,"")			
			
def Episodes_old(url,name):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<ul><li class="video"><div class="video_i"><a href="(.+?)">').findall(newlink)
        vidseries = re.compile('-video_(.+?).html').findall(url)
        if(len(match[0])):
                vidseries = re.compile('-video_(.+?).html').findall(match[0])
                vidseries=vidseries[0]
                addLink(name,match[0],3,"")
        elif (len(vidseries)):
                vidseries=vidseries[0]
                addLink(name,url,3,"")
        try:
                lastvidseries = ParseXml("http://www.video4khmer.com/relatedclips.php?vid=" + vidseries)
                if(len(lastvidseries)):
                        lastvidseries = ParseXml("http://www.video4khmer.com/relatedclips.php?vid=" + lastvidseries)
                        if(len(lastvidseries)):
                                addDir("Next >>","http://www.video4khmer.com/relatedclips.php?vid=" + lastvidseries,7,"")
                else:
                        raise Exception("Didn't fine listing")
        except:
                match=re.compile('<div id="browse_results" (.+?)<ul>(.+?)</ul></div>').findall(newlink)
                if(len(match) >= 1):
                        linkmatch=re.compile('<img src="(.+?)"  alt=[^>]*').findall(match[0][1])
                        counter = 0
                        for vpic in linkmatch:
                            counter += 1
                            youtubeid = re.compile('/vi/(.+?)/').findall(vpic)
                            addLink(name + " " + str(counter),"http://www.youtube.com/watch?v="+youtubeid[0],3,vpic)
    #except: pass
	
def Episodes(url,name):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div id="browse_results" (.+?)<ul>(.+?)</ul></div>').findall(newlink)
        if(len(match) >= 1):
                linkmatch=re.compile('<li class="video"><div class="video_i">(.+?)</div></li>').findall(match[0][1])
                counter = 0
                for vpic in linkmatch:
                    vidlink=re.compile('<a href="(.+?)"><img src="(.+?)"  alt="(.+?)" class="imag" width="(.+?)" height="(.+?)" />').findall(vpic)
                    (vurl,vimg,vname,vtmp1,vtmp2)=vidlink[0]
                    counter += 1
                    youtubeid = re.compile('/vi/(.+?)/').findall(vimg)
                    if(len(youtubeid)):
                            addLink(vname.encode('utf-8'),"http://www.youtube.com/watch?v="+youtubeid[0],3,vimg)
                    else:
                            addLink(vname.encode('utf-8'),vurl,3,vimg)
        match5=re.compile('<div class="pagination">(.+?)</div></div>').findall(newlink)
        if(len(match5)):
                pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match5[0])
                for pcontent in pages:
                        (pageurl,pagenum)=pcontent
                        addDir("Page " + pagenum,"http://www.video4khmer.com/"+pageurl,5,"")
    #except: pass    

def ParseXml(url):
        newcontent=GetContent(url)
        vurl=""
        xmlcontent=xml.dom.minidom.parseString(newcontent.encode('utf-8'))
        items=xmlcontent.getElementsByTagName('video')
        if(len(items)>=1 and len(items[0].getElementsByTagName('url')[0].childNodes)):
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('url')[0].childNodes[0].data
                        vimg=itemXML.getElementsByTagName('thumb')[0].childNodes[0].data
                        youtubeid = re.compile('/vi/(.+?)/').findall(vimg)
                        if(len(youtubeid)):
                                addLink(vname,"http://www.youtube.com/watch?v="+youtubeid[0],3,vimg)
                        else:
                                addLink(vname,vurl,3,vimg)
        if(len(vurl) >= 1):
                vidseries = re.compile('-video_(.+?).html').findall(vurl)[0]
        else:
                vidseries =""
        return vidseries


def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = ""
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
	
def loadVideos(newlink,name):
        try:
           if (newlink.find("video4khmer.com") > -1):
                linkcontent = GetContent(url)
                newContent = ''.join(linkcontent.splitlines()).replace('\t','')
                titlecontent = re.compile("var flashvars = {file: '(.+?)',").findall(newContent)
                newlink=titlecontent[0]
           if (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')		
           else:
                if (newlink.find("linksend.net") > -1):
                     d = xbmcgui.Dialog()
                     d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')		
                newlink1 = urllib2.unquote(newlink).decode("utf8")+'&dk;'
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                    #d = xbmcgui.Dialog()
                    #d.ok('mode 2',str(lastmatch),'launching yout')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('video4khmer',urllib2.unquote(newlink).decode("utf8"))
        except: pass
     	
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
        liz=xbmcgui.ListItem('Next >', iconImage="http://www.video4khmer.com/templates/3column/images/header/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.video4khmer.com/templates/3column/images/header/logo.png", thumbnailImage=iconimage)
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

#url='http://www.khmeraccess.com/video/viewvideo/6604/31end.html'		
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        INDEX(url)
elif mode==3:
        #sysarg="-1"
        loadVideos(url,name)
elif mode==4:
        #sysarg="-1"
        SEARCH()
elif mode==5:
       Episodes(url,name)
elif mode==6:
       SearchResults(url)
elif mode==7:
       ParseXml(url)

	   
xbmcplugin.endOfDirectory(int(sysarg))
