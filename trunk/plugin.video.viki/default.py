import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import urlresolver
from xml.dom.minidom import Document

__settings__ = xbmcaddon.Addon(id='plugin.video.viki')
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'sub.srt'))
langfile = xbmc.translatePath(os.path.join(home, 'resources', 'lang.txt'))
strdomain ="http://www.viki.com"
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

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
        addDir('Search channel','search',5,'')
        addDir('Search Videos','search',12,'')
        addDir('Genres','http://www.viki.com/explore',2,'')
        addDir('Updated Tv shows','http://www.viki.com/tv/recent',8,'')
        addDir('Updated Movies','http://www.viki.com/recent?utf8=%E2%9C%93&category=movies&country=&subtitle_language_code=',8,'')
        addDir('Select Sub Language','http://www.viki.com/',9,'')
def LangOption():
        addDir('Show Top Languages','Top',10,'')
        addDir('Show All Languages','All',10,'')
		
def ListGenres(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<li class="genre-item">          <div class="thumb-container big-thumb">            <a href="(.+?)">              <img alt="(.+?)" class="thumb-design" src="(.+?)" /></a>').findall(link)
        for vurl,vname,vimg in vidlist:
            addDir(vname,strdomain+vurl,6,vimg)
			
def SaveLang(langcode, name):
    f = open(langfile, 'w');f.write(langcode);f.close()   
    d = xbmcgui.Dialog()
    d.ok(name,"Language Saved",'')
    HOME()
def Genre(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<div class="vk-thumbnail medium"><a href="(.+?)"><img alt="(.+?)" src="(.+?)" />').findall(link)
        for vurl,vname,vimg in vidlist:
            vurl = vurl.split("/videos/")[0]
            addDir(vname,strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,6,"")

def UpdatedVideos(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<div class="thumb-container big-thumb">      <a href="(.+?)">        <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(link)
        for vurl,vname,vimg in vidlist:
            vurl = vurl.split("/videos/")[0]
            addDir(vname,strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    print strdomain+purl
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,8,"") 
					
def getVidPage(url,name):
  link = GetContent(url)
  link = ''.join(link.splitlines()).replace('\'','"')
  vidcontainer=re.compile('<li class="clearfix" id="media_(.+?)">(.+?)<p class="sub-headline">').findall(link)
  if(len(vidcontainer) ==0):
          vidcontainer=re.compile('<li class="clearfix" id="media_(.+?)">(.+?)</li>').findall(link)
  for mediaid,vcontent in vidcontainer:
        vidlist=re.compile('<a href="(.+?)>        <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(vcontent)
        vidlist2=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>').findall(vcontent)
        (vurl,vname,vimg)=vidlist[0]
        (vurl,vname)=vidlist2[0]
        vurl = vurl.split("/videos/")[0]
        sublinks=re.compile('data-path="/subtitles/media_resource/(.+?).json"').findall(vcontent)
        if(len(sublinks)==0):
                subidlist1 =  re.compile('/media_resource/thumbnail/(.+?)/(.+?)').findall(vimg)
                if(len(subidlist1[0]) > 1):
                     subidlist = subidlist1[0][0]
                else:
                     subidlist=mediaid
        else:   
                subidlist='_'.join(sublinks)
        addDir(vname,mediaid+"|"+subidlist,4,vimg)
  pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
  if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    if(pname.find("About Us") != 0):
                          addDir("page " + pname.decode("utf-8"),strdomain+purl,7,"")

def getLanguages(url, ltype):
        link = GetContent("http://www.viki.com/tv/recent")
        link = ''.join(link.splitlines()).replace('\'','"')
        if(ltype=="Top"):
                match = re.compile('<optgroup label="Top Languages">(.+?)<optgroup label="All Languages">').findall(link)
        else:
                match = re.compile('<optgroup label="All Languages">(.+?)</select>').findall(link)
        if(len(match)>0):
                langlist= re.compile('<option value="(.+?)">(.+?)</option>').findall(match[0])
                for purl,pname in langlist:
                       addDir(pname,purl,11,"")
					   
def checkLanguage(mediaid):
        data = json.load(urllib2.urlopen("http://www.viki.com/subtitles/media/"+mediaid+".json"))
        f = open(langfile, "r")
        langs = f.read()
        langcnew=""
        try:
               transpercent=data[langs]
               if(transpercent < 50):
                      langs="en"
                      xbmc.executebuiltin("Language is less then 50% finish,defaulting to english,5000)")
        except:
               langs="en"
               xbmc.executebuiltin("Language you selected isn't available,defaulting to english for this video,5000)")
        return langs
		
def SearchChannelresults(url,searchtext):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<div class="thumb-container big-thumb">        <a href="(.+?)">          <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(link)
        for vurl,vname,vimg in vidlist:
            vurl = vurl.split("/videos/")[0]
            print "currechannel:" + strdomain+vurl+"/videos"
            addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    print strdomain+purl
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,13,"")
					
def SEARCHChannel():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="http://www.viki.com/search_channel?q=" + searchText
        SearchChannelresults(searchurl,searchText.lower())
		
def getVideoUrl(url,name):

   data = json.load(urllib2.urlopen(url))['streams']
   for i, item in enumerate(data):
        if(item["type"].find("DAILYMOTION") > -1):
                dailylink = item["uri"]+"&dk;"
                match=re.compile('/swf/(.+?)&dk;').findall(dailylink)
                if(len(match) == 0):
                        match=re.compile('/video/(.+?)&dk;').findall(dailylink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                linkcontent=GetContent(link)
                sequence=re.compile('"sequence":"(.+?)"').findall(linkcontent)
                newseqeunce = urllib.unquote(sequence[0]).replace('\\/','/')
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                        imgSrc=re.compile('/jpeg" href="(.+?)"').findall(linkcontent)
                dm_low=re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                if(len(dm_high) == 0):
                        vidlink = dm_low[0]
                else:
                        vidlink = dm_high[0]
        elif(item["type"].find("GOOGLE") > -1):
            vidcontent=GetContent(item["uri"])
            vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
            vidlink=vidmatch[0][0]
        elif(item["type"].find("YOUTUBE") > -1):
            vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(item["uri"])
            vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
            vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        else:
            sources = []
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=item["uri"], title=label)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            print "urlrsolving" + item["uri"]
            if source:
                vidlink = source.resolve()
            else:
                vidlink =""
   return vidlink
   
def SearchVideoresults(url,searchtext):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidcontainer=re.compile('<li id="media-result">(.+?)</li>').findall(link)
        for vcontent in vidcontainer:
                vidlist=re.compile('<div class="thumb-container big-thumb">      <a href="(.+?)">        <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(vcontent)
                vidlist2=re.compile('<h3>      <a href="(.+?)">(.+?)</a>    </h3>').findall(vcontent)
                (vurl,vname,vimg)=vidlist[0]
                (vurl,vname)=vidlist2[0]
                vurl = vurl.split("/videos/")[0]
                addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,14,"")
def SEARCHVideos():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="http://www.viki.com/search_media?q=" + searchText 
        SearchVideoresults(searchurl,searchText.lower())
		
def getVidQuality(url,name):
  idlist=url.split("|")
  mediaid= idlist[0]
  subidlist= idlist[1].split("_")
  
  vidurl = "http://www.viki.com/player/medias/"+mediaid+"/info.json?rtmp=false"
  data = json.load(urllib2.urlopen(vidurl))['streams']
  langcode=checkLanguage(mediaid)
  if(data[0]['quality']!="solo"):
          suburl= "http://www.viki.com/subtitles/media/" + mediaid + "/" + langcode + ".json"
          subid=subidlist[0]
          for i, item in enumerate(data):
                  addLink(item['quality'],item['uri'],3,"")
          try:
                  json2srt(suburl, name)
          except:
                  try:
                        suburl= "http://www.viki.com/subtitles/media_resource/" + subid + "/" + langcode + ".json"
                        json2srt(suburl, name)
                  except:  
                        f = open(filename, 'w');f.write("");f.close()
  else:
          pctr=0
          for subid in subidlist:
                  pctr=pctr+1
                  suburl= "http://www.viki.com/subtitles/media_resource/" + subid + "/" + langcode + ".json"
                  vidurl="http://www.viki.com/player/media_resources/" + subid + "/info.json?rtmp=false"
                  #directurl = getVideoUrl(vidurl,suburl)
                  addLinkSub("part " + str(pctr),vidurl,15,"",suburl)
                 

def playVideo(suburl,videoId):
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        xbmcPlayer.setSubtitles(suburl) 
		
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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode("utf-8"))
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
		
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        HOME()
       
elif mode==2:
        ListGenres(url,name) 
elif mode==3:
        playVideo(filename,url)
elif mode==4:
        getVidQuality(url,filename) 
elif mode==5:
        SEARCHChannel()
elif mode==6:
        Genre(url,name)
elif mode==7:
        getVidPage(url,name)
elif mode==8:
        UpdatedVideos(url,name)
elif mode==9:
        LangOption()
elif mode==10:
        getLanguages(name, url)
elif mode==11:
        SaveLang(url,name)
elif mode==12:
        SEARCHVideos()
elif mode==13:
        SearchChannelresults(url)
elif mode==14:
        SearchVideoresults(url)
elif mode==15:
        print "outside:" + subtitleurl
        playVideoPart(subtitleurl,url,filename)

xbmcplugin.endOfDirectory(int(sysarg))
