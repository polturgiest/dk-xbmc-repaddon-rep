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

def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        addDir('Search','http://phim47.com/',4,'http://yeuphim.net/images/logo.png')
        addDir('HQ Videos','http://phim47.com/list-hd.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Movies','http://phim47.com/movie-list/phim-le.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Series','http://phim47.com/movie-list/phim-bo.html ',2,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Videos By Region','http://phim47.com/',8,'http://phim47.com/skin/movie/style/images/logo.png')
        addDir('Videos By Category ','http://phim47.com/',9,'http://phim47.com/skin/movie/style/images/logo.png')


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
		
homeLink="http://phim47.com/"
def INDEX(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        match=re.compile('<div id="content_show">(.+?)<div class="pagination">').findall(link)
        vidlist = re.compile('<a href="(.+?)"  onmouseover="(.+?)" onmouseout="(.+?)" alt="(.+?)" ><img class="showend" src="(.+?)" [^>]*').findall(match[0])
        for vurl,vtmp1,vtmp2,vname,vimg in vidlist:
            addDir(vname.encode("utf-8"),vurl.encode("utf-8"),7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        navmatch=re.compile('[^>]* href="(.+?)" >(.+?)</a>').findall(pagelist[0])
        for vurl,vname in navmatch:
            addDir(vname.encode("utf-8"),vurl.encode("utf-8"),2,"")


def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://phim47.com/tim-kiem/'+searchText+'/0'
        INDEX(url)
    except: pass

def Mirrors(url,name):
  mirrorlink =getVidPage(url,name)
  link = GetContent(mirrorlink)
  link=''.join(link.splitlines()).replace('\'','"')
  mirmatch=re.compile('<div id="list_episodes">(.+?)<div id="fb-root">').findall(link)
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
  mlink=re.compile('<a onclick="this.style.behavior="url\(#default#homepage\)"; this.setHomePage\("http://phim47.com"\);"  href="(.+?)" ><img src="http://phim47.com/skin/movie/style/images/watch_now.png"  width="(.+?)" height="(.+?)">').findall(contentlink)
  return mlink[0][0]


def Episodes(url,name):
    try:
        link = GetContent(url)
        link=''.join(link.splitlines()).replace('\'','"')
        mirmatch=re.compile('<div id="list_episodes">(.+?)<div id="fb-root">').findall(link)
        servlist =re.compile('<div class="name left namew">'+name+'&nbsp;&nbsp;&nbsp;(.+?)<div class="clear_td">').findall(mirmatch[0])
        epilist =re.compile('<a  href=(.+?) >(.+?)</a>').findall(servlist[0])
        curmatch =re.compile('<a class="current" >(.+?)</a>').findall(servlist[0])
        if(len(curmatch)>0):
              addLink("part - "+ curmatch[0].strip().encode("utf-8"),url.encode("utf-8"),3,'',name.encode("utf-8"))
        for vlink,vLinkName in epilist:
              addLink("part - "+ vLinkName.strip().encode("utf-8"),vlink.encode("utf-8"),3,'',name.encode("utf-8"))

    except: pass

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
        xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
        link=GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        match = re.compile('proxy.link=phim47\*(.+?)&').findall(link)
        newlink =decodeurl(match[0])
        if(newlink.find("cyworld.vn") > 0):
            vidcontent=GetContent(newlink)
            vidmatch=re.compile('<meta property="og:video" content="(.+?)" />').findall(vidcontent)
            vidlink=vidmatch[0]
            playVideo("direct",vidlink)
        elif(newlink.find("picasaweb.google") > 0):
            vidcontent=GetContent(newlink)
            vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
            vidlink=vidmatch[0][0]
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
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't play video",'Try another link')

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
