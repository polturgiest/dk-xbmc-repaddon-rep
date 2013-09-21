import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
try: import simplejson as json
except ImportError: import json
import cgi
import urlresolver
from t0mm0.common.addon import Addon
import datetime
ADDON = xbmcaddon.Addon(id='plugin.video.pinoy_ako')
addon = Addon('plugin.video.pinoy_ako')
datapath = addon.get_profile()
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "pinoy_ako"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.9" #<---- PLUGIN VERSION

strdomain ='http://www.pinoy-ako.info'
def HOME():
        addDir('Search','http://www.pinoy-ako.info',8,'')
        addDir('Latest Videos','http://www.pinoy-ako.info',7,'')
        addDir('Pinoy Movies','http://www.pinoy-ako.info/movies/pinoy-movies-uploaded.html',6,'')
        addDir('Foreign Films','http://www.pinoy-ako.info/movies/foreign-films-uploaded.html',6,'')
        #addDir('Pinoy Box Office','http://www.pinoy-ako.info/movies/pinoy-box-office.html',6,'')
        #addDir('Cinema One','http://www.pinoy-ako.info/movies/pinoy-box-office.html',6,'')
        addDir('Sports & Others','http://www.pinoy-ako.info/movies/sports-a-other-videos.html',5,'')
        addDir('All TV Shows','http://www.pinoy-ako.info/tv-show-replay.html',10,'')
        addDir('ABS-CBN Shows','http://www.pinoy-ako.info/tv-show-replay/abs-cbn-2-tv-shows.html',2,'http://img687.imageshack.us/img687/5412/abscbntvshows.jpg')
        addDir('ABS-CBN Old Shows','http://www.pinoy-ako.info/index.php?option=com_content&view=article&id=11672:watch-old-abscbn-2-kapamilya-tv-shows',2,'http://img687.imageshack.us/img687/5412/abscbntvshows.jpg')
        addDir('GMA 7 Shows','http://www.pinoy-ako.info/tv-show-replay/gma-7-tv-shows.html',2,'http://img198.imageshack.us/img198/7536/gmatvshows.jpg')
        addDir('GMA 7 Old Shows','http://www.pinoy-ako.info/index.php?option=com_content&view=article&id=11671:watch-old-gma-7-kapuso-tv-shows',2,'http://img198.imageshack.us/img198/7536/gmatvshows.jpg')
        addDir('TV5 Shows','http://www.pinoy-ako.info/tv-show-replay/tv5-tv-shows.html',2,'http://img29.imageshack.us/img29/2499/tv5tvshows.jpg')
        addDir('TV5 Old Shows','http://www.pinoy-ako.info/tv-show-replay/94-tv-guide/59771-watch-old-tv5-kapatid-tv-shows.html',2,'http://img29.imageshack.us/img29/2499/tv5tvshows.jpg')
        addDir('TV Specials','http://www.pinoy-ako.info/tv-show-replay/tv-specials.html',5,'http://img857.imageshack.us/img857/8424/tvspecials.jpg')
        addLink('ABS-CBN live','rtmp://tko.og.abscbn.streamguys.com:1935/abs/_definst_/abs live=true',11,'')
        addLink('GMA live','rtmp://live.iguide.to/edge playpath=tj6zegfdas16p08 swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl=http://www.ilive.to/embedplayer.php?width=630&height=360&channel=44090&autoplay=true token=#e87JDUJD264YED687 swfVfy=1 live=1 timeout=15',12,'')
def AllTV(url):
        link = GetContent(url)
        link=link.encode("UTF-8")
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<div id="content">(.+?)<div class="clr"></div>').findall(link)
        movielist=re.compile('<li>(.+?)</li>').findall(vidcontent[0])
        for moviecontent in movielist:
            vurlc=re.compile('<a href="(.+?)" class="category">(.+?)</a>').findall(moviecontent)
            (vurl,vname)=vurlc[0]
            addDir(vname,strdomain+vurl,5,"")
def INDEX(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('</table><table class="contentpaneopen">(.+?)<span class="article_separator">').findall(newlink)
        tblecontent=re.compile('<tbody>(.+?)</tbody>').findall(vidcontent[0])
        showlist=re.compile('<a [^s][^>]*href=["\']?([^>^"^\']+)["\']?[^>]*><img alt="(.+?)" src="(.+?)" /></a>').findall(tblecontent[0])
        for (vlink,vname,vimg) in showlist:
                addDir(vname.replace("&amp;","&"),vlink.replace("&amp;amp;","&amp;"),5,vimg)
def INDEX2(url):
        link = GetContent(url)
        link=link.encode("UTF-8")
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<div id="content">(.+?)<div class="clr"></div>').findall(link)
        movielist=re.compile('<table class="contentpaneopen">(.+?)<span class="article_separator">').findall(vidcontent[0])
        for moviecontent in movielist:
            vimg=""
            vimgc=re.compile('<img style="margin: 5px; float: left;" alt="(.+?)" src="(.+?)" height="100"').findall(moviecontent)
            if(len(vimgc) > 0):
                    (vtmp,vimg)=vimgc[0]
            vurlc=re.compile('<a href="(.+?)" class="contentpagetitle">(.+?)</a>').findall(moviecontent)
            if(len(vurlc) > 0):
                    (vurl,vname)=vurlc[0]
                    addDir(vname,strdomain+vurl,4,vimg)	
def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.pinoy-ako.info/component/search/?searchword='+ searchText +'&ordering=newest&searchphrase=all&limit=20'
        SearchResults(url)


				
def SearchResults(url):
        link = GetContent(url)
        link=link.encode("UTF-8")
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<div id="content">(.+?)<div class="clr"></div>').findall(link)
        movielist=re.compile('<fieldset>(.+?)</fieldset>').findall(vidcontent[0])
        for moviecontent in movielist:
            vurlc=re.compile('<a href="(.+?)">(.+?)</a>').findall(moviecontent)
            (vurl,vname)=vurlc[0]
            addDir(vname,strdomain+vurl,4,"")	
        pagin=re.compile('<ul class="pagination">(.+?)</li></ul>').findall(vidcontent[0])
        if(len(pagin) > 0):
             pagelist=re.compile('<a href="(.+?)" title="(.+?)">').findall(pagin[0])
             for (vlink,vname) in pagelist:
                  addDir("page - " + vname,strdomain+vlink,9,"")

def GetLatest(url):
        link = GetContent(url)
        link = link.encode("UTF-8")
        link = ''.join(link.splitlines()).replace('\t','')
        CategoryList = ["Latest TV shows", "Latest Pinoy Movies", "Latest Sports & Other videos","Latest Foreign Films"]
        vidcontent=re.compile('<div id="sidebar2">(.+?)<div class="clr">').findall(link)
        latestUl=re.compile('<ul class="latestnews">(.+?)</ul></div>').findall(vidcontent[0])
        Catcount=0
        for content in latestUl:
                if(Catcount < len(CategoryList)):
                        addLink("--------"+CategoryList[Catcount]+"--------","",0,"")
                latestVideos=re.compile('<li class="latestnews"><a href="(.+?)" class="latestnews">(.+?)</a></li>').findall(content)
                for (vlink,vname) in latestVideos:
                        addDir(vname,strdomain+vlink,4,"")	
                Catcount=Catcount+1
				
def GetXmlPlaylist(url, name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        partcnt=0
        embsrc=re.compile('<location>(.+?)</location>').findall(link)
        for embvid in embsrc:
                vname = embvid.replace("http://","").replace("https://","").split(".")[1]
                partcnt=partcnt+1
                addLink(name+ " youtube part " + str(partcnt),embvid,3,"")
				
def GetVideoLinks(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidcontent=re.compile('</table><table class="contentpaneopen">(.+?)<span class="article_separator">').findall(link)
        tabvids=re.compile('<div class="(blitzer|tabbertab|jwts_tabber|smoothness)">(.+?)</div></div>').findall(vidcontent[0])
        singlevids=re.compile('<p style="text-align:center;">(.+?)</p>').findall(vidcontent[0])
        singledivs=re.compile('<div style="text-align: center;">(.+?)</div>').findall(vidcontent[0])
        singlevids.extend(singledivs)
        mirrorcnt = 0
        for spancontent in singlevids:
                if (spancontent.find("blitzer") == -1 and spancontent.find("tabbertab") == -1 ):
                        mirrorcnt=mirrorcnt+1
                        partcnt=0
                        embsrc=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(spancontent.lower())
                        for embvid in embsrc:
                                arr = embvid.replace("http://","").replace("https://","").split(".")
                                if(arr[1].find("/") > -1):
                                      vname=arr[0]
                                else:
                                      vname=arr[1]
                                fileext = arr[len(arr)-1]
                                if fileext.lower() !="swf":
                                        partcnt=partcnt+1
                                        if(len(embsrc) == 1):
                                               vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                                        else:
                                               vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                                        addLink(vname,embvid,3,"")
                        embsrc=re.compile('<embed[^>]*flashvars=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(spancontent.replace(" ",""))
                        for embvid in embsrc:
                                embvid=embvid.replace("file=","")
                                vname = embvid.replace("http://","").replace("https://","").split(".")
                                if(vname[1].find("/") > -1):
                                      vname=vname[0]
                                else:
                                      vname=vname[1]
                                partcnt=partcnt+1
                                if(len(embsrc) == 1):
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                                else:
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                                if(embvid.find("youtubetune") > -1  or embvid.find("youtubereloaded") > -1):
                                      #print urllib.unquote_plus(embvid).replace("&amp;http://","http://")
                                      embvid1=urllib.unquote_plus(embvid).replace("&amp;http://","http://").split("&")[0]
                                      GetXmlPlaylist(embvid1, "mirror "+str(mirrorcnt))
                                else:
                                      addLink(vname,embvid,3,"")
                        frmsrc1=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(spancontent)
                        for frmvid in frmsrc1:
                                vname = frmvid.replace("http://","").replace("https://","").split(".")
                                if(vname[1].find("/") > -1):
                                      vname=vname[0]
                                else:
                                      vname=vname[1]
                                partcnt=partcnt+1
                                if(len(frmsrc1) == 1):
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                                else:
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                                addLink(vname,frmvid,3,"")
                        if partcnt==0:
                                mirrorcnt=mirrorcnt-1
        for tmp, divcotent in tabvids:
                mirrorcnt=mirrorcnt+1
                embsrc=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(divcotent)
                partcnt=0
                for embvid in embsrc:
                        vname = embvid.replace("http://","").replace("https://","").split(".")
                        if(vname[1].find("/") > -1):
                                      vname=vname[0]
                        else:
                                      vname=vname[1]
                        partcnt=partcnt+1
                        if(len(embsrc) == 1):
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                        else:
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                        addLink(vname,embvid,3,"")
                frmsrc=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(divcotent)
                for frmvid in frmsrc:
                        vname = frmvid.replace("http://","").replace("https://","").split(".")
                        if(vname[1].find("/") > -1):
                                      vname=vname[0]
                        else:
                                      vname=vname[1]
                        partcnt=partcnt+1
                        if(len(frmsrc) == 1):
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                        else:
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                        addLink(vname,frmvid,3,"")
                objsrc=re.compile('<object [^>]*data=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(divcotent)
                for objvid in objsrc:
                        vname = objvid.replace("http://","").replace("https://","").split(".")
                        if(vname[1].find("/") > -1):
                                      vname=vname[0]
                        else:
                                      vname=vname[1]
                        partcnt=partcnt+1
                        if(len(frmsrc) == 1):
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " full "
                        else:
                                      vname="mirror "+str(mirrorcnt)+" "+ vname + " part " + str(partcnt)
                        addLink(vname,urllib.unquote_plus(objvid.replace("&amp;","&")),3,"")
                if partcnt==0:
                        mirrorcnt=mirrorcnt-1
						
def Episodes(url):
        link = GetContent(url)
        link=link.encode("UTF-8")
        link  = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('<form action="(.+?)" method="post" name="adminForm">(.+?)</form>').findall(link)
        episodelist=re.compile('<td><a href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></td>').findall(match[0][1])
        for (vlink,vname) in episodelist:
                addDir(vname,strdomain+vlink,4,"")
        pagin=re.compile('<ul class="pagination">(.+?)</li></ul>').findall(match[0][1])
        if(len(pagin) > 0):
             pagelist=re.compile('<a href="(.+?)" title="(.+?)">').findall(pagin[0])
             for (vlink,vname) in pagelist:
                  addDir("page - " + vname,strdomain+vlink,5,"")


def ParseXml(newcontent):
        try:
                xmlcontent=xml.dom.minidom.parseString(newcontent)
        except:
                ParsePlayList(newcontent)
                return ""
        if('<tracklist>' in newcontent):
                ParsePlayList(newcontent)
                channels = xmlcontent.getElementsByTagName('tracklist')
                items=xmlcontent.getElementsByTagName('track')
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('location')[0].childNodes[0].data
                        addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")
        else:
                channels = xmlcontent.getElementsByTagName('channel')
                if len(channels) == 0:
                    channels = xmlcontent.getElementsByTagName('feed')
                items=xmlcontent.getElementsByTagName('item')
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('media:content')[0].getAttribute('url')
                        addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")

def ParsePlayList(newcontent):
        newcontent=''.join(newcontent.splitlines()).replace('\t','')
        match=re.compile('<title>(.+?)</title>[^>]*<location>(.+?)</location>').findall(newcontent)
        for vcontent in match:
                (vname,vurl)=vcontent
                addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")				

def ParseSeparate(vcontent,namesearch,urlsearch):
        newlink = ''.join(vcontent.splitlines()).replace('\t','')
        match2=re.compile(urlsearch).findall(newlink)
        match3=re.compile(namesearch).findall(newlink)
        imglen = len(match3)
        if(len(match2) >= 1):
                for i in range(len(match2)):
                    if(i < imglen ):
                        namelink = match3[i]
                    else:
                        namelink ='part ' + str(i+1)
                    addLink(namelink.encode("utf-8"),match2[i],3,"")
                return True
        return False
					
def GetContent2(url):
    conn = httplib.HTTPConnection(host="pinoy-ako.info",timeout=30)
    req = url
    try:
        conn.request('GET',req)
        content = conn.getresponse().read()
    except:
        print 'echec de connexion'
    conn.close()
    return content
	
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def PostContent(referrer,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', referrer)
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data


def iLiveLink(mname,murl,thumb):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Opening Stream,3000)")
        #link=GetContent(murl)
        ok=True

        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        #link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile('http://www.ilive.to/embed/(.+?)&width=(.+?)&height=(.+?)&autoplay=true').findall(murl)
        for fid,wid,hei in match:
                    pageUrl='http://www.ilive.to/embedplayer.php?width='+wid+'&height='+hei+'&channel='+fid+'&autoplay=true'
        link=GetContent(pageUrl)
        playpath=re.compile('file: "(.+?).flv"').findall(link)
        tokenpage=re.compile('getJSON\("(.+?)", function').findall(link)
        if len(tokenpage)>0:
                        tokencontent=PostContent(pageUrl,tokenpage[0])
                        token=re.compile('"token":"(.+?)"').findall(tokencontent)[0]
        if len(playpath)==0:
                        playpath=re.compile('http://snapshots.ilive.to/snapshots/(.+?)_snapshot.jpg').findall(thumb)      
        for playPath in playpath:
                    stream_url = 'rtmp://live.iguide.to/edge playpath=' + playPath + " swfUrl=http://player.ilive.to/player_ilive_2.swf pageUrl="+pageUrl+" token="+token+" swfVfy=1 live=1 timeout=15"
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        listitem.setInfo('video', {'Title': mname, 'Genre': 'Live'} )
        
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
                #WatchHistory

        return ok
		
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
        #xbmc.executebuiltin("xbmc.PlayMedia("+videoId+")")
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def resolve_180upload(url,inhtml=None):
    net = Net()
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        puzzle_img = os.path.join(datapath, "180_puzzle.png")
        print '180Upload - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        dialog.update(50)
                
        data = {}
        r = re.findall(r'type="hidden" name="(.+?)" value="(.+?)">', html)

        if r:
            for name, value in r:
                data[name] = value
        else:
            raise Exception('Unable to resolve 180Upload Link')
        
        #Check for SolveMedia Captcha image
        solvemedia = re.search('<iframe src="(http://api.solvemedia.com.+?)"', html)

        if solvemedia:
           dialog.close()
           html = net.http_GET(solvemedia.group(1)).content
           hugekey=re.search('id="adcopy_challenge" value="(.+?)">', html).group(1)
           open(puzzle_img, 'wb').write(net.http_GET("http://api.solvemedia.com%s" % re.search('<img src="(.+?)"', html).group(1)).content)
           img = xbmcgui.ControlImage(450,15,400,130, puzzle_img)
           wdlg = xbmcgui.WindowDialog()
           wdlg.addControl(img)
           wdlg.show()
        
           xbmc.sleep(3000)

           kb = xbmc.Keyboard('', 'Type the letters in the image', False)
           kb.doModal()
           capcode = kb.getText()
   
           if (kb.isConfirmed()):
               userInput = kb.getText()
               if userInput != '':
                   solution = kb.getText()
               elif userInput == '':
                   Notify('big', 'No text entered', 'You must enter text in the image to access video', '')
                   return False
           else:
               return False
               
           wdlg.close()
           dialog.create('Resolving', 'Resolving 180Upload Link...') 
           dialog.update(50)
           if solution:
               data.update({'adcopy_challenge': hugekey,'adcopy_response': solution})

        print '180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        dialog.update(100)
        
        link = re.search('<a href="(.+?)" onclick="thanks\(\)">Download now!</a>', html)
        if link:
            print '180Upload Link Found: %s' % link.group(1)
            return link.group(1)
        else:
            raise Exception('Unable to resolve 180Upload Link')

    except Exception, e:
        print '**** 180Upload Error occured: %s' % e
        raise
    finally:
        dialog.close()
		
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]
	
def unpackjs4(texto):

    matches = texto.split("return p}")
    if len(matches)>0:
        data = matches[1].replace(".split(\"|\")))","")
    else:
        return ""

    patron = "(.*)\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    
    descifrado = ""
    
    claves = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"]
    palabras = matches[0][1].split("|")
    diccionario = {}
   
    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1


    def lookup(match):
        return diccionario[match.group(0)]


    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    return descifrado

def unpackjs3(texto,tipoclaves=1):

    
    patron = "return p\}(.*?)\.split"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    if len(matches)>0:
        data = matches[0]
    else:
        patron = "return p; }(.*?)\.split"
        matches = re.compile(patron,re.DOTALL).findall(texto)
        if len(matches)>0:
            data = matches[0]
        else:
            return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]

    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    if tipoclaves==1:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    else:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
        claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
        claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
        
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:

        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

     # Substitute the words of the conversion table
     # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

     # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)

    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    descifrado = descifrado.replace("\\","")


    return descifrado
	
def unpackjs(texto):

    # Extract the function body
    patron = "eval\(function\(p\,a\,c\,k\,e\,d\)\{[^\}]+\}(.*?)\.split\('\|'\)\)\)"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    
    # Separate code conversion table
    if len(matches)>0:
        data = matches[0]

    else:
        return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
    claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
    claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

    # Substitute the words of the conversion table
    # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

    # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)


    return descifrado
	
def postContent2(url,data,referr):
    req = urllib2.Request(url,data)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    return data
	
def loadVideos(url,name):
        #try:
           GA("LoadVideo",name)
           newlink=url
           xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
           print "newlink=" + newlink
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(url+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(url)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
           elif (newlink.find("allmyvideos") > -1):
                videoid=  re.compile('http://allmyvideos.net/embed-(.+?).html').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://allmyvideos.net/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(newlink,posdata,url)
                vidlink=re.compile('"file" : "(.+?)",').findall(pcontent)[0]
           elif (newlink.find("nosvideo") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(newlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]
           elif (newlink.find("uploadpluz") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                pcontent=''.join(link.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1].replace('<script type="text/javascript">',"")
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                vidUrl=re.compile('"file","(.+?)"').findall(unpacked)[0]
                vidlink=vidUrl+"|Referer=http%3A%2F%2Fuploadpluz.com%3A8080%2Fplayer%2Fplayer.swf"
           elif (newlink.find("180upload") > -1):
                urlnew= re.compile('http://180upload.com/embed-(.+?).html').findall(newlink)
                print urlnew
                if(len(urlnew) > 0):
                      newlink="http://180upload.com/" + urlnew[0]
                vidlink=resolve_180upload(newlink,None)
           elif (newlink.find("youtube") > -1) and (newlink.find("playlists") > -1):
                playlistid=re.compile('playlists/(.+?)\?v').findall(newlink)
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("list=") > -1):
                playlistid=re.compile('videoseries\?list=(.+?)&').findall(newlink+"&")
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("/p/") > -1):
                playlistid=re.compile('/p/(.+?)\?').findall(newlink)
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif (newlink.find("youtube") > -1) and (newlink.find("/embed/") > -1):
                playlistid=re.compile('/embed/(.+?)\?').findall(newlink+"?")
                vidlink=getYoutube(playlistid[0])
           elif (newlink.find("youtube") > -1):
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                print "in youtube" + lastmatch[0]
                vidlink=getYoutube(lastmatch[0])
           else:
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + url
                if source:
                        vidlink = source.resolve()
                else:
                        vidlink =""
           playVideo("pinoy",vidlink)
        #except: pass
        
def extractFlashVars(data):
    for line in data.split("\n"):
            index = line.find("ytplayer.config =")
            if index != -1:
                found = True
                p1 = line.find("=", (index-3))
                p2 = line.rfind(";")
                if p1 <= 0 or p2 <= 0:
                        continue
                data = line[p1 + 1:p2]
                break
    if found:
            data = json.loads(data)
            flashvars = data["args"]
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

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


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
        GA("HOME","HOME")
        HOME()
elif mode==11:
        playVideo("pinoy",url)
elif mode==12:
        iLiveLink("test","http://www.ilive.to/embed/44090&width=630&height=360&autoplay=true","")
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
       #PlaywithHeader()
       loadVideos(url,name)
elif mode==4:
       GetVideoLinks(url)
elif mode==5:
       GA("Episodes",name)
       Episodes(url)
elif mode==6:
       INDEX2(url)
elif mode==7:
       GetLatest(strdomain)
elif mode==8:
       SEARCH()
elif mode==9:
       SearchResults(url)
elif mode==10:
       AllTV(url)
xbmcplugin.endOfDirectory(int(sysarg))
