import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import re
import urlresolver
import HTMLParser
import urlparse
from xml.dom.minidom import Document
import datetime
from textwrap import wrap
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote
	
ADDON=__settings__ = xbmcaddon.Addon(id='plugin.video.viki')

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "Viki"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.1.8" #<---- PLUGIN VERSION

home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'sub.srt'))
langfile = xbmc.translatePath(os.path.join(home, 'resources', 'lang.txt'))
strdomain ="http://www.viki.com"
enableProxy= ADDON.getSetting('enableProxy')
enableTrans= (ADDON.getSetting('enableTrans')=="true")
translanguage=ADDON.getSetting('translang')
reg_list = ["https://losangeles-s02-i01-traffic.cyberghostvpn.com/go/browse.php?u=*url*&b=1", 
            "https://bucharest-s05-i01-traffic.cyberghostvpn.com/go/browse.php?u=*url*&b=1",
            "https://frankfurt-s02-i01-traffic.cyberghostvpn.com/go/browse.php?u=*url*&b=1", 
            "https://london-s01-i15-traffic.cyberghostvpn.com/go/browse.php?u=*url*&b=1"]
proxyurl = reg_list[int(ADDON.getSetting('region'))]

class Translator:
    string_pattern = r"\"(([^\"\\]|\\.)*)\""
    match_string =re.compile(
                        r"\,?\["
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern
                        +r"\]")

    def __init__(self, to_lang, from_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        return self._unescape(self._get_translation_from_json5(json5))

    def _get_translation_from_json5(self, content):
        result = ""
        pos = 2
        while True:
            m = self.match_string.match(content, pos)
            if not m:
                break
            result += m.group(1)
            pos = m.end()
        return result

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        data="client=t&ie=UTF-8&oe=UTF-8&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
        req = request.Request(url="http://translate.google.com/translate_a/t", headers = headers)
        r = request.urlopen(req,data)
        return r.read().decode('utf-8')

    def _unescape(self, text):
        return json.loads('"%s"' % text)

translator= Translator(from_lang="en", to_lang=translanguage)

def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def GetContent(url, useProxy=False):
    if useProxy==True:
        return GetContent2(url, useProxy)
    hostn= urlparse.urlparse(url).hostname
    conn = httplib.HTTPConnection(host=hostn,timeout=30)
    req = url.replace(url.split(hostn)[0]+hostn,'')
    try:
        conn.request('GET',req)
    except:
        print 'echec de connexion'
    content = conn.getresponse().read()
    conn.close()
    return content
	
def GetContent2(url, useProxy=False):
    strresult=""
    response=None
    if useProxy==True:
        url = proxyurl.replace("*url*",urllib.quote_plus(url))
        #proxy_handler = urllib2.ProxyHandler({'http':us_proxy})
        #opener = urllib2.build_opener(proxy_handler)
        #urllib2.install_opener(opener)
        print "use proxy:" + str(useProxy) + url
    try:
        if(response!=None):
           connection.close()
        req = urllib2.Request(url)
        req.add_unredirected_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)')
        response = urllib2.urlopen(req)
        strresult=response.read()
        response.close()
    except Exception, e:
       print str(e)+" |" + url
       if(response!=None):
           connection.close()
    return strresult

def write2srt(url, fname):
    try:
          subcontent=GetContent(url).encode("utf-8")
    except:
          subcontent=GetContent(url)
    if(enableTrans):
          subcontent=Translate_lrge_str(subcontent)
    try:
          subcontent=subcontent.encode("utf-8")
    except: pass
    f = open(fname, 'w');f.write(subcontent);f.close()

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

def HOME(translator):
        #addDir('Search channel','search',5,'')
        staticmenu="Choose Translation Language|Search Videos|Find Video By Viki ID|Genres|Updated Tv shows|Updated Movies|Updated Music|Select Subtitle Language"
        
        if(enableTrans):
               transtext=translator.translate(staticmenu).replace(" | ","|")
               try:
                        transtext=transtext.encode("UTF-8")
               except: pass
               staticlist=transtext.split("|")
               addDir(staticlist[0],'search',17,'')
        else:
               staticlist=staticmenu.split("|")

        addDir(staticlist[1],'search',12,'')
        addDir(staticlist[2],'search',16,'')
        addDir(staticlist[3],'http://www.viki.com/genres',2,'')
        addDir(staticlist[4],'http://www.viki.com/tv/browse?sort=latest',8,'')
        addDir(staticlist[5],'http://www.viki.com/movies/browse?sort=latest',8,'')
        addDir(staticlist[6],'http://www.viki.com/music/browse?sort=latest',8,'')
        if(enableTrans==False):
               addDir(staticlist[7],'http://www.viki.com/tv/browse',10,'')
def LangOption():
        addDir('Show All Languages','All',10,'')

def ShowLangDiag(translator):
	dialog = xbmcgui.Dialog()
	langlist ="Afrikaans|Albanian|Arabic|Azerbaijani|Basque|Bengali|Belarusian|Bulgarian|Catalan|Chinese Simplified|Chinese Traditional|Croatian|Czech|Danish|Dutch|English|Esperanto|Estonian|Filipino|Finnish|French|Galician|Georgian|German|Greek|Gujarati|Haitian Creole|Hebrew|Hindi|Hungarian|Icelandic|Indonesian|Irish|Italian|Japanese|Kannada|Khmer|Korean|Latin|Latvian|Lithuanian|Macedonian|Malay|Maltese|Norwegian|Persian|Polish|Portuguese|Romanian|Russian|Serbian|Slovak|Slovenian|Spanish|Swahili|Swedish|Tamil|Telugu|Thai|Turkish|Ukrainian|Urdu|Vietnamese|Welsh|Yiddish".split("|")
	langcode="af|sq|ar|az|eu|bn|be|bg|ca|zh-CN|zh-TW|hr|cs|da|nl|en|eo|et|tl|fi|fr|gl|ka|de|el|gu|ht|iw|hi|hu|is|id|ga|it|ja|kn|km|ko|la|lv|lt|mk|ms|mt|no|fa|pl|pt|ro|ru|sr|sk|sl|es|sw|sv|ta|te|th|tr|uk|ur|vi|cy|yi".split("|")
	index = dialog.select('Choose the language to translate to', langlist)
	win = xbmcgui.Window(10000)
	ADDON.setSetting('translang', langcode[index])
	translanguage=langcode[index]
	translator= Translator(from_lang="vi", to_lang=translanguage)
	HOME(translator)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))
	
def Translate_lrge_str(string):
    totaltext =""
    chunksize=90000
    ctr=0
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('Please wait while text is being translated')
    percent = (ctr * 100)/chunksize
    remaining_display  = '[B]'+str(percent)+'%[/B] is done'
    pDialog.update(0,'Please wait while text is being translated',remaining_display)
    checklist=list(chunkstring(string, chunksize))
    for idx in checklist:
        transcontent = translator.translate(idx)
        totaltext=totaltext+transcontent.replace("- >","->").replace(" ->"," -->").replace("< / ","</").replace(" >",">")
        ctr = ctr + 1
        percent = (ctr * 100)/chunksize
        remaining_display = '[B]'+str(percent)+'%[/B] is done'
        pDialog.update(percent,'Please wait while text is being translated',remaining_display)

    return totaltext
	
def ListGenres(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        vidcontent=re.compile('<ul class="thumb-grid">(.+?)</ul>').findall(link)
        vidlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(vidcontent[0])
        transtext=""
        namelist=[]
        ctr=0
        if(enableTrans):
			for vurl,vname in vidlist:
				transtext=transtext+RemoveHTML(vname)+"|"
			transtext=translator.translate(transtext).replace(" | ","|")
			namelist=transtext.split("|")
        for vurl,vname in vidlist:
            if(len(namelist)>0):
				vname=namelist[ctr]
				try:
					vname=vname.encode("UTF-8")
				except:pass
            addDir(RemoveHTML(vname).replace("&amp;","&"),strdomain+vurl+"?sort=latest",8,"")
            ctr=ctr+1
			
def SaveLang(langcode, name):
    f = open(langfile, 'w');f.write(langcode);f.close()   
    d = xbmcgui.Dialog()
    d.ok(name,"Language Saved",'')
    HOME(translator)

def Genre(url,name):
        link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        #vcontent =re.compile('<div class="tab-content">(.+?)</section>').findall(link) 
        vidulist=re.compile('<ul class="thumb-grid mbl">(.+?)</ul>').findall(link)
        vidlist=re.compile('<li[^>]*>(.+?)</li>').findall(vidulist[0])
        transtext=""
        namelist=[]
        ctr=0
        if(enableTrans):
			for vlist in vidlist:
				(vname,vtmp1,vimg,vtmp2)=re.compile('<img alt="(.+?)" height="(.+?)" src="(.+?)" width="(.+?)" />').findall(vlist)[0]
				transtext=transtext+vname+"|"
			transtext=translator.translate(transtext).replace(" | ","|")
			namelist=transtext.split("|")
        for vlist in vidlist:
            vurl=re.compile('<a href="(.+?)" class="thumbnail">').findall(vlist)[0]
            vid=re.compile('data-tooltip-src="/container_languages_tooltips/(.+?).json"').findall(vlist)
            if(len(vid)==0):
                    vid=re.compile('data-tooltip-src="/video_languages_tooltips/(.+?).json"').findall(vlist)
            vid=vid[0]
            #vurl=re.compile('<a href="(.+?)" class="thumbnail pull-left">').findall(vlist)[0]
            #vname=re.compile('<li class="media">(.+?)</li>').findall(vlist)
            (vname,vtmp1,vimg,vtmp2)=re.compile('<img alt="(.+?)" height="(.+?)" src="(.+?)" width="(.+?)" />').findall(vlist)[0]
            if(len(namelist)>0):
				vname=namelist[ctr]
				try:
					vname=vname.encode("UTF-8")
				except:pass
            if(vurl.find("/tv/") > -1):
                    vlink = strdomain+"/related_videos?container_id="+vid+"&page=1&type=episodes"
                    mode=7
            else:
                    vurlist=vurl.split("/")
                    vid=vurlist[len(vurlist)-1].split("-")[0]
                    vlink =vid
                    mode=4
            addDir(vname.decode("UTF-8"),vlink,mode,vimg)
            ctr=ctr+1
        pagelist=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.replace("&rarr;",">").decode("utf-8"),strdomain+purl,6,"")

def UpdatedVideos(url,name):
        useProxy=(enableProxy=="true")
        link = GetContent(url,useProxy)
        link = ''.join(link.splitlines()).replace('\'','"').replace("/go/browse.php?u=","").replace("http%3A%2F%2Fwww.viki.com","").replace("%2F","/").replace("&amp;b=1","")
        try:
            link =link.encode("UTF-8")
        except: pass

        vcontent=re.compile('<ul class="medias medias-block medias-wide mbx(.+?)</ul>').findall(link)
        if(len(vcontent) ==0):
               vcontent=re.compile('<ul class="medias medias-block medias-wide mbl btz"(.+?)</ul>').findall(link)
        if(len(vcontent) ==0):
               vcontent=re.compile('Recently Added\s*</a>\s*</li>\s*</ul>(.+?)</ul>').findall(link)
        vidlist=re.compile('<li [^>]*(.+?)</li>').findall(vcontent[0])
        mode=7
        transtext=""
        namelist=[]
        ctr=0
        if(enableTrans):
			for licontent in vidlist:
				vid=re.compile('data-tooltip-src="/container_languages_tooltips/(.+?).json"').findall(licontent)
				if(len(vid)==0):
					vid=re.compile('data-tooltip-src="/video_languages_tooltips/(.+?).json"').findall(licontent)
				if(len(vid)>0):
					vurl,vname=re.compile('<h2 class="gamma mts">\s*<a href="(.+?)">(.+?)</a>\s*</h2>').findall(licontent)[0]
					transtext=transtext+vname+"|"
			transtext=translator.translate(transtext).replace(" | ","|")
			namelist=transtext.split("|")

        for licontent in vidlist:
            vid=re.compile('data-tooltip-src="/container_languages_tooltips/(.+?).json"').findall(licontent)
            if(len(vid)==0):
                    vid=re.compile('data-tooltip-src="/video_languages_tooltips/(.+?).json"').findall(licontent)
            if(len(vid)>0):
                    vid=vid[0]
                    vurl,vname=re.compile('<h2 class="gamma mts">\s*<a href="(.+?)">(.+?)</a>\s*</h2>').findall(licontent)[0]
                    vimg=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(licontent)[0]
                    if(len(namelist)>0):
						vname=namelist[ctr]
                    try:
						vname=vname.encode("UTF-8")
                    except:pass
                    if(vurl.find("/movies/") > -1):
                         vurlist=re.compile('<a href="(.+?)" class="thumbnail pull-left">').findall(licontent)[0]
                         vurlist=vurlist.split("/")
                         vid=vurlist[len(vurlist)-1].split("-")[0]
                         vlink =vid
                         mode=4
                    elif(vurl.find("/videos/")> -1):
                        vlink =strdomain+vurl
                        mode=7
                    else:
                        vlink = strdomain+"/related_videos?container_id="+vid+"&page=1&type=episodes"
                        mode=7
                    addDir(vname.replace("&amp;","&").replace("&#x27;","'"),vlink,mode,urllib.unquote_plus(vimg))
                    ctr=ctr+1
        pagelist=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname,strdomain+purl,8,"")

def getContainerID(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('data-subscribe="(.+?)"').findall(link)
        return vidcontent[0]

def getRelatedVID(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<li data-replace-with="(.+?)"').findall(link)
        return urllib.unquote_plus(vidcontent[0])
		
def getVidPage(url,page):
  url1=url
  if(url.find("related_videos") == -1):
        vcontainerid=getContainerID(url)
        url1=strdomain+"/related_videos?container_id="+vcontainerid+"&page=1&type=episodes"
  link = GetContent(url1)
  link = ''.join(link.splitlines()).replace('\'','"')
  if(len(link) ==0 or link.find("Oh no! Something went wrong.")!= -1):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        match=re.compile('<ul class="medias medias-block[^>]*data-slider-items="1">(.+?)</ul>').findall(link)
        link=match[0]
  
  try:
        link =link.encode("UTF-8")
  except: pass
  vidcontainer=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>\s*<div class="thumbnail-small pull-left">\s*<img alt="(.+?)" [^s][^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
  vidnum=re.compile('\/([0-9]*)([a-z]|\s*).json"').findall(link)
  transtext=""
  namelist=[]
  ctr=0
  if(enableTrans):
		for y in range(0, len(vidnum)):
			(vurl,vname,vimg) = vidcontainer[y]
			transtext=transtext+vname+"|"
		transtext=translator.translate(transtext).replace(" | ","|")
		namelist=transtext.split("|")
  for x in range(0, len(vidnum)):
       vid="".join(vidnum[x])
       if(vidnum[x][1]==""):
           vid=vidnum[x][0]+"v"
       (vurl,vname,vimg) = vidcontainer[x]
       if(len(namelist)>0):
			vname=namelist[ctr]
       try:
			vname=vname.encode("UTF-8")
       except:pass
       vurl = vurl.split("/videos/")[0]
       addDir(vname,vid,4,vimg)
       ctr=ctr+1
  #for vid,vtmp,vurl,vname,vimg in vidcontainer:
  #      vurl = vurl.split("/videos/")[0]
  #      addDir(vname,vid,4,vimg)
  pagelist=re.compile('<a class="btn btn-small btn-wide" href="#">Show more</a>').findall(link)
  if(len(pagelist) > 0):
          pagenum=re.compile('&page=(.+?)&type=episodes').findall(url1)
          pagectr=int(pagenum[0])+1
          addDir("page " + str(pagectr),url1.replace("&page="+pagenum[0]+"&","&page="+str(pagectr)+"&"),7,"")


def getLanguages(url, ltype):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
                link =link.encode("UTF-8")
        except: pass
        match = re.compile('<li>\s*<span class="filter-title">Subtitled in</span>(.+?)lolspeak</a></li>').findall(link)
        match = re.compile('<h3 class="nav-heading">All</h3>(.+?)lolspeak</a></li>').findall(match[0]+"lolspeak</a></li>")
        if(len(match)>0):
                langlist= re.compile('<li title=""><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(match[0].replace("/tv/browse?language=",""))
                for purl,pname in langlist:
                       if(pname !="All languages"):
                             addDir(pname,purl.replace("/tv/browse?country=",""),11,"")
					   
def checkLanguage(mediaid):
        data = GetVideoInfo(mediaid)
        f = open(langfile, "r")
        langs = f.read()
        langcnew=""
        try:
               transpercent=data["subtitle_completions"][langs]
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
            addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
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
   #data = json.load(urllib2.urlopen(url))['streams']
   #for i, item in enumerate(data):
        if(url.find("dailymotion") > -1):
                dailylink = url+"&dk;"
                match=re.compile('www.dailymotion.pl/video/(.+?)-').findall(dailylink)
                if(len(match) == 0):
                        match=re.compile('/video/(.+?)&dk;').findall(dailylink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                vidlink=getDailyMotionUrl(str(match[0]))
        elif(url.find("google") > -1):
            vidcontent=GetContent(url)
            vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
            vidlink=vidmatch[0][0]
        elif(url.find("youtube") > -1):
            vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(url)
            vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
            vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        else:
            sources = []
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            print "urlrsolving" + url
            if source:
                vidlink = source.resolve()
            else:
                vidlink =""
        return vidlink
		
def getDailyMotionUrl(id):
    maxVideoQuality="720p"
    content = GetContent("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30022)+' (DailyMotion)!,5000)')
        return ""
    else:
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(content)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(content)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(content)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(content)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(content)
        url = ""
        if matchFullHD and maxVideoQuality == "1080p":
            url = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        elif matchHD and (maxVideoQuality == "720p" or maxVideoQuality == "1080p"):
            url = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        elif matchHQ:
            url = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        elif matchSD:
            url = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        elif matchLD:
            url = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        return url
		
def SearchVideoresults(url,searchtext=""):
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
        searchurl="http://www.viki.com/search?q=" + searchText 
        UpdatedVideos(searchurl,searchText.lower())

def SEARCHByID():
        keyb = xbmc.Keyboard('', 'Enter Viki Video ID')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText()) 
        getVidQuality(searchText,"",filename,True) 

def GetVideoInfo(vidid):
    infourl=sign_request(vidid,".json")
    print infourl
    data = json.load(urllib2.urlopen(infourl))
    return data
    
def expires():
    '''return a UNIX style timestamp representing 5 minutes from now'''
    return int(time.time())

def sign_request(vidid,vtype):
    from hashlib import sha1
    import hmac
    import binascii

    # If you dont have a token yet, the key should be only "CONSUMER_SECRET&"
    key = "-$iJ}@p7!G@SyU/je1bEyWg}upLu-6V6-Lg9VD(]siH,r.,m-r|ulZ,U4LC/SeR)"
    ts=str(expires())
    # The Base String as specified here: 
    rawtxt = "/v4/videos/"+vidid+vtype+"?app=65535a&t="+ts+"&site=www.viki.com" # as specified by oauth

    hashed = hmac.new(key, rawtxt, sha1)
    fullurl = "http://api.viki.io" + rawtxt+"&sig="+binascii.hexlify(hashed.digest())
    # The signature
    return fullurl
	
def getVidQuality(vidid,name,filename,checkvideo):
  GA("Playing",name)
  print vidid
  print name
  useProxy=(enableProxy=="true")
  if(checkvideo):
          pardata=GetVideoInfo(vidid)

          if "parts" in pardata:
             partnum=len(pardata["parts"])
             if(partnum>1):
                for i in range(partnum):
                     addDir(name +" part " + str(pardata["parts"][i]["part"]),pardata["parts"][i]["id"],15,"")
                return ""
  if(useProxy):
          vidurl=proxyurl.replace("*url*",urllib.quote_plus(sign_request(vidid,"/streams.json")))
  else:
          vidurl = sign_request(vidid,"/streams.json")
  data = json.load(urllib2.urlopen(vidurl))
  if(len(data) == 0):
          if(useProxy):
                vidurl=proxyurl.replace("*url*",urllib.quote_plus(sign_request(vidid+"v","/streams")))
          else:
                vidurl = sign_request(vidid+"v","/streams")
          data = json.load(urllib2.urlopen(vidurl))
  langcode=checkLanguage(vidid)
  strQual=""
  strprot=""
  print vidurl
  try:
          if(enableTrans):
                suburl=sign_request(vidid,"/subtitles/en.srt")
          else:
                suburl=sign_request(vidid,"/subtitles/" + langcode + ".srt")
          print suburl
          write2srt(suburl, filename) 
  except:
          suburl=sign_request(vidid,"/subtitles/en.srt")
          write2srt(suburl, filename) 
		  
  for i, item in enumerate(data):
          strQual=str(item)
          mydata = data[item]
          if(item!="external"):
              for seas in mydata:
                  strprot=str(seas)
                  vlink=mydata[seas]["url"]
                  if(strprot=="http"):
                        addLink(strQual +"("+strprot+")",vlink,3,"")
          else:
              vlink=getVideoUrl(mydata["url"],name)
              addLink("external Video",vlink,3,"")
                 

def playVideo(suburl,videoId):
        print videoId
        vidinfo = videoId.split("_")[0]
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', vidinfo)
        win.setProperty('1ch.playing.season', str(3))
        win.setProperty('1ch.playing.episode', str(4))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        xbmcPlayer.setSubtitles(suburl) 

		
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

print "mode is:"+ str(mode)
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        GA("Home","Home")
        HOME(translator)
elif mode==2:
        ListGenres(url,name) 
elif mode==3:
        playVideo(filename,url)
elif mode==4:
        getVidQuality(url,name,filename,True) 
elif mode==5:
        SEARCHChannel()
elif mode==6:
        GA("Genre",name)
        Genre(url,name)
elif mode==7:
        getVidPage(url,name)
elif mode==8:
        GA("Recent_Videos",name)
        UpdatedVideos(url,name)
elif mode==9:
        LangOption()
elif mode==10:
        getLanguages(url,name)
elif mode==11:
        SaveLang(url,name)
elif mode==12:
        SEARCHVideos()
elif mode==13:
        SearchChannelresults(url)
elif mode==14:
        SearchVideoresults(url)
elif mode==15:
        getVidQuality(url,name,filename,False) 
elif mode==16:
        SEARCHByID() 
elif mode==17:
        ShowLangDiag(translator)

xbmcplugin.endOfDirectory(int(sysarg))
