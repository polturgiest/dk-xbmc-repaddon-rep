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


strdomain ='moviekhmer.com/'
def HOME():
        addDir('Khmer Comedy','http://moviekhmer.com/category/khmer/khmer-comedy/',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Movies','http://moviekhmer.com/category/khmer/khmer-movies/',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Song','http://moviekhmer.com/category/khmer/khmer-songs/',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer TV Show','http://moviekhmer.com/category/khmer/khmer-tv-show-khmer/',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Thai Movies','http://moviekhmer.com/category/thai/thai-movies/',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Thai Lakorns','http://moviekhmer.com/category/thai/thai-lakorns/',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Korean Drama','http://moviekhmer.com/category/korean/korean-dramas/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        addDir('Korean Movies','http://moviekhmer.com/category/korean/korean-movies/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        addDir('Chinese Movies','http://moviekhmer.com/category/chinese/chinese-movies/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Chinese Series','http://moviekhmer.com/category/chinese/chinese-series/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Documentaries','http://moviekhmer.com/category/uncategories/documentary-uncategories/',2,'http://moviekhmer.com/wp-content/uploads/2011/04/vlcsnap-2011-04-04-21h01m29s71-180x135.jpg')

def INDEX(url):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        #start=newlink.index('<div id="main">')
        #end=newlink.index('<!-- main -->')
        match=re.compile('<div class="arc-main">((.|\s)*?)<div id="page-sidebar">').findall(newlink)
        if(len(match) >= 1 and len(match[0]) >= 1):
                match=re.compile('<div class="img-th">((.|\s)*?)<h4 class="post-tit">').findall(match[0][0])
                if(len(match) >= 1):
                        for vcontent in match:
                            match1=re.compile('<a href="(.+?)" rel="bookmark"><img [^>]*src="(.+?)" class="attachment-thumbnail wp-post-image" alt="(.+?)"').findall(vcontent[0])
                            (vurl, vimage, vname)=match1[0]
                            addDir(vname.encode("utf-8"),vurl,5,vimage)
        match5=re.compile("<div class='wp-pagenavi'>((.|\s)*?)</div>").findall(newlink)
        if(len(match5) >= 1 and len(match5[0]) >= 1 and newlink.find("class='nextpostslink'") > -1 ):
                startlen=re.compile("<span class='current'>(.+?)</span>").findall(match5[0][0])
                url=url.replace("page/"+startlen[0],"")
                print url
                addDir("Next >>",url+'page/' + str(int(startlen[0])+1),2,"")
    except: pass
			
def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<h2 class="title"><a href="(.+?)" rel="bookmark" title="">(.+?)</a></h2>').findall(newlink)
        if(len(match) >= 1):
                for vLink, vLinkName in match:
                    addDir(vLinkName,vLink,5,'')
        match=re.compile('<a class="next page-numbers" href="(.+?)">').findall(link)
        if(len(match) >= 1):
            nexurl= match[0]
            addDir('Next>',nexurl,6,'')			
			
def Episodes(url,name):
    try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('{ "file": "(.+?)", "title": "(.+?)", "description": "", "image":').findall(link)
        if(len(match) >= 1):
                for mcontent in match:
                    vLink, vLinkName=mcontent
                    addLink(vLinkName.encode("utf-8"),vLink,3,'')
        else:
                match=re.compile('"file": "(.+?)",').findall(link)
                if(len(match) >= 1):
                        if(".xml" in match[0]):
                                newcontent=GetContent("http://moviekhmer.com"+match[0])
                                ParseXml(newcontent)
                        elif (len(match) > 1):
                                counter = 0
                                for mcontent in match:
                                        counter += 1
                                        addLink(name.encode("utf-8") + " part " + str(counter),mcontent,3,"")
                        else:
                                addLink(name.encode("utf-8"),match[0],3,"")
                else:
                        match=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        if(len(match) >= 1):
                                addLink(name.encode("utf-8"),match[0],3,"")
                        else:
                                match=re.compile("'flashvars','&#038;file=(.+?)'").findall(link)
                                if(len(match) >= 1):
                                        ParseXml(GetContent(match[0]).encode("utf-8"))
                                elif(len(re.compile('file: "(.+?)",').findall(link)) >=1):
                                        hasitem=ParseSeparate(newlink,'title: "(.+?)",','file: "(.+?)",')
                                else:
                                        hasitem=ParseSeparate(newlink,'{"title":"(.+?)","creator":','"levels":\[{"file":"(.+?)"}')
 
              
    except: pass		


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
    conn = httplib.HTTPConnection(host="moviekhmer.com",timeout=30)
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

def PostContent(formvar,url):
        try:
                net = Net()
                headers = {}
                headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                headers['Accept-Encoding'] = 'gzip, deflate'
                headers['Accept-Charset']='ISO-8859-1,utf-8;q=0.7,*;q=0.7'
                headers['Referer'] = 'http://www.khmeraccess.com/video/videolist/videonew.html?cid=1'
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0.1) Gecko/20100101 Firefox/5.0.1'
                headers['Connection'] = 'keep-alive'
                headers['Host']='www.khmeraccess.com'
                headers['Accept-Language']='en-us,en;q=0.5'
                headers['Pragma']='no-cache'
                formdata={}                      
                formdata['start']=formvar


                #first_response = net.http_Get('http://khmerfever.com/wp-login.php',headers=header_dict)
                #net.save_cookies('c:\cookies.txt')
                #net.set_cookies('c:\cookies.txt')
                second_response = net.http_POST(url,formdata,headers=headers,compression=False)
                return second_response.content
        except: 
                d = xbmcgui.Dialog()
                d.ok('Time out',"Can't Connect to site",'Try again in a moment')
	
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
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
	
def loadVideos(url,name):
        try:
           newlink=url
           xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
           if (newlink.find("dailymotion") > -1):
                match=re.compile('(dailymotion\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
                lastmatch = match[0][len(match[0])-1]
                link = 'http://www.dailymotion.com/'+str(lastmatch)
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('"sequence",  "(.+?)"').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                playVideo('dailymontion',urllib2.unquote(dm_low[0]).decode("utf8"))
           elif (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')		
           else:
                if (newlink.find("linksend.net") > -1):
                     d = xbmcgui.Dialog()
                     d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')		
                newlink1 = urllib2.unquote(newlink).decode("utf8")+'&dk;'
                print 'NEW url = '+ newlink1
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                    #d = xbmcgui.Dialog()
                    #d.ok('mode 2',str(lastmatch),'launching yout')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('moviekhmer',urllib2.unquote(newlink).decode("utf8"))
        except: pass
        
def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response       
def extractFlashVars(data):
        flashvars = {}
        found = False
        for line in data.split("\n"):
            if line.strip().startswith("yt.playerConfig = "):
                found = True
                print line
                p1 = line.find('"url_encoded_fmt_stream_map":')
                p2 = line.rfind('};')
                if p1 <= 0 or p2 <= 0:
                    continue
                data = line[p1 + 1:p2]
                print "databefore" + data
                p2 = data.find('",')
                data = data[1:p2]
                data = data.split(":")[1].strip().replace('"','').replace("\u0026","&")
                print "newdata"+data
                break
        if found:
            #data = json.loads(data)
            #print "loadjson"+data
            #data = data[data.find("flashvars"):]
            #data = data[data.find("\""):]
            #data = data[:1 + data[1:].find("\"")]

            #flashvars[u"url_encoded_fmt_stream_map"]=urllib.quote_plus("sig=5F5DCF6D8710C32BAB3BF7716F817A96129BD004.9ED642709E32DEC5070F225A2BF30BED8989C2BB&itag=43&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26ratebypass%3Dyes%26itag%3D43%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26source%3Dyoutube%26expire%3D1360836986%26sparams%3Dcp%252Cid%252Cip%252Cipbits%252Citag%252Cratebypass%252Csource%252Cupn%252Cexpire&type=video%2Fwebm%3B+codecs%3D%22vp8.0%2C+vorbis%22&quality=medium&fallback_host=tc.v7.cache1.c.youtube.com,sig=C1FB08FE99ACA2BFAE0D3EF67B30D1F0ED990A38.9D2480603ECACC8263BD9EACE86FDB065BCBE5A1&itag=34&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26itag%3D34%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26factor%3D1.25%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26burst%3D40%26algorithm%3Dthrottle-factor%26source%3Dyoutube%26expire%3D1360836986%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26sparams%3Dalgorithm%252Cburst%252Ccp%252Cfactor%252Cid%252Cip%252Cipbits%252Citag%252Csource%252Cupn%252Cexpire&type=video%2Fx-flv&quality=medium&fallback_host=tc.v3.cache4.c.youtube.com,sig=0A0393E3D42E3ECA061F3631DAE92E1A86562237.C4A42977A7BCB3697391501A87AF6DEE26C35906&itag=18&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26ratebypass%3Dyes%26itag%3D18%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26source%3Dyoutube%26expire%3D1360836986%26sparams%3Dcp%252Cid%252Cip%252Cipbits%252Citag%252Cratebypass%252Csource%252Cupn%252Cexpire&type=video%2Fmp4%3B+codecs%3D%22avc1.42001E%2C+mp4a.40.2%22&quality=medium&fallback_host=tc.v24.cache7.c.youtube.com,sig=17D8079585E194851B1827C484A960DA22AD51C9.02F0E6DAF8CC9EA320E477549CAC62B1788964D2&itag=5&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26itag%3D5%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26factor%3D1.25%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26burst%3D40%26algorithm%3Dthrottle-factor%26source%3Dyoutube%26expire%3D1360836986%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26sparams%3Dalgorithm%252Cburst%252Ccp%252Cfactor%252Cid%252Cip%252Cipbits%252Citag%252Csource%252Cupn%252Cexpire&type=video%2Fx-flv&quality=small&fallback_host=tc.v2.cache1.c.youtube.com,sig=39AE834781AA29AC4DC4AF7DB5EE23943C427D93.1A0E0F0393E5FC7A7089552E8BB90C15D9F9AC13&itag=36&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26itag%3D36%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26factor%3D1.25%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26burst%3D40%26algorithm%3Dthrottle-factor%26source%3Dyoutube%26expire%3D1360836986%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26sparams%3Dalgorithm%252Cburst%252Ccp%252Cfactor%252Cid%252Cip%252Cipbits%252Citag%252Csource%252Cupn%252Cexpire&type=video%2F3gpp%3B+codecs%3D%22mp4v.20.3%2C+mp4a.40.2%22&quality=small&fallback_host=tc.v13.cache7.c.youtube.com,sig=A79C1538EB3E4B4D2DAD1420BD8188D7B0ED9CB5.6D0EC72728EAE97ED7A5642666FA00F02FF685FD&itag=17&url=http%3A%2F%2Fr9---sn-i3b7sn7d.c.youtube.com%2Fvideoplayback%3Fmt%3D1360813931%26itag%3D17%26sver%3D3%26fexp%3D902904%252C901803%252C914036%252C911928%252C920704%252C912806%252C902000%252C922403%252C922405%252C929901%252C913605%252C925006%252C908529%252C920201%252C911116%252C926403%252C910221%252C901451%252C919114%26ms%3Dau%26upn%3DjibP6ZvjXl4%26factor%3D1.25%26key%3Dyt1%26id%3D1d9229a6ccfa63e4%26mv%3Dm%26newshard%3Dyes%26ipbits%3D8%26ip%3D111.67.106.161%26burst%3D40%26algorithm%3Dthrottle-factor%26source%3Dyoutube%26expire%3D1360836986%26cp%3DU0hVRVhOVF9NUENONV9QSFhKOlpqbmZMTXRYMHVP%26sparams%3Dalgorithm%252Cburst%252Ccp%252Cfactor%252Cid%252Cip%252Cipbits%252Citag%252Csource%252Cupn%252Cexpire&type=video%2F3gpp%3B+codecs%3D%22mp4v.20.3%2C+mp4a.40.2%22&quality=small&fallback_host=tc.v21.cache4.c.youtube.com")
            flashvars[u"url_encoded_fmt_stream_map"]=data
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
		
def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="http://i42.tinypic.com/4uz9lc.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://i42.tinypic.com/4uz9lc.png", thumbnailImage=iconimage)
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
elif mode==5:
       Episodes(url,name)

	   
xbmcplugin.endOfDirectory(int(sysarg))
