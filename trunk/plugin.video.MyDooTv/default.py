import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
import xbmcaddon,xbmcplugin,xbmcgui
#from t0mm0.common.net import Net
import hashlib,random

strdomain ='www.mydootv.com'
strServerUrl=""
def HOME():
    addDir('Search','/videos/categories',4,'')
    addDir('Live Tv','/videos/categories',13,'')
    addDir('Cartoons ', 'http://www.mydootv.com/products_list_wide.php?uri=/Cartoon&menuType=programmes&groupID=90&value2=&viewType=&page=1&groupName=%3Cstrong%3ECartoon%3C/strong%3E%20%A1%D2%C3%EC%B5%D9%B9&numRows=&limit=25',2,'')
    addDir('all thai drama ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama&menuType=programmes&groupID=38,10,193,194,200,206,210,212&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai on air ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/On-Air&menuType=programmes&groupID=10&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2013 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2013&menuType=programmes&groupID=215&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2012 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2012&menuType=programmes&groupID=212&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2011 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2011&menuType=programmes&groupID=210&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2010 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2010&menuType=programmes&groupID=206&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2009 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2009&menuType=programmes&groupID=193&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama 2008 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/2008&menuType=programmes&groupID=194&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('---thai drama classic ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Thai-Drama/Classic&menuType=programmes&groupID=200&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('K-j series ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Korean-Japanese&menuType=programmes&groupID=40,213&value2=&viewType=&page=1&groupName=&numRows=&limit=25',2,'')
    addDir('chinese ', 'http://www.mydootv.com/products_list_wide.php?uri=/Drama/Chinese-Taiwanese&menuType=programmes&groupID=121&value2=&viewType=&page=1&groupName=%3Cstrong%3EC-T%20Series%3C/strong%3E%20%CB%B9%D1%A7%A8%D5%B9-%E4%B5%E9%CB%C7%D1%B9%20%AA%D8%B4%20&numRows=&limit=25',2,'')
    addDir('all news ', 'http://www.mydootv.com/products_list_wide.php?uri=/News&menuType=programmes&groupID=131,151,27&value2=&viewType=&page=1&groupName=%3Cstrong%3ENews%3C/strong%3E%20%A2%E8%D2%C7&numRows=&limit=25',2,'')
    addDir('---breaking news  ', 'http://www.mydootv.com/products_list_wide.php?uri=/News/Breaking-News&menuType=programmes&groupID=131&value2=&viewType=&page=1&groupName=%3Cstrong%3EBreaking%20News%3C/strong%3E%20%A2%E8%D2%C7%A8%D2%A1%AA%E8%CD%A7%B5%E8%D2%A7%E6&numRows=&limit=25',2,'')
    addDir('---entertainment news ', 'http://www.mydootv.com/products_list_wide.php?uri=/News/Entertainment-News&menuType=programmes&groupID=151&value2=&viewType=&page=1&groupName=%3Cstrong%3EEntertainment%20News%3C/strong%3E%20%A2%E8%D2%C7%BA%D1%B9%E0%B7%D4%A7&numRows=&limit=25',2,'')
    addDir('---news analysis ', 'http://www.mydootv.com/products_list_wide.php?uri=/News/News-Analysis&menuType=programmes&groupID=27&value2=&viewType=&page=1&groupName=%3Cstrong%3ENews%20Analysis%3C/strong%3E%20%C7%D4%E0%A4%C3%D2%D0%CB%EC%A2%E8%D2%C7&numRows=&limit=25',2,'')
    addDir('tv programs ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program&menuType=programmes&groupID=125,126,127,132,185,152,129&value2=&viewType=&page=1&groupName=%3Cstrong%3ETV%20Program%3C/strong%3E%20%C3%D2%C2%A1%D2%C3%B7%D5%C7%D5&numRows=&limit=25',2,'')
    addDir('---talk show ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Talk-Show&menuType=programmes&groupID=125&value2=&viewType=&page=1&groupName=%3Cstrong%3ETalk%20Show%3C/strong%3E%20%B7%CD%C5%EC%A4%E2%AA%C7%EC&numRows=&limit=25',2,'')
    addDir('---variety show ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Variety-Show&menuType=programmes&groupID=126&value2=&viewType=&page=1&groupName=%3Cstrong%3EVariety%20Show%3C/strong%3E%20%C7%D2%E4%C3%B5%D5%E9%E2%AA%C7%EC&numRows=&limit=25',2,'')
    addDir('---game shows ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Game-Quiz&menuType=programmes&groupID=127&value2=&viewType=&page=1&groupName=%3Cstrong%3EGame%20&%20Quiz%3C/strong%3E%20%E0%A1%C1%E2%AA%C7%EC&numRows=&limit=25',2,'')
    addDir('---food & health ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Food-Healthy&menuType=programmes&groupID=132&value2=&viewType=&page=1&groupName=%3Cstrong%3EFood%20&%20Healthy%3C/strong%3E%20%CD%D2%CB%D2%C3-%CA%D8%A2%C0%D2%BE&numRows=&limit=25',2,'')
    addDir('---sports ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Sport&menuType=programmes&groupID=185&value2=&viewType=&page=1&groupName=%3Cstrong%3ESport%3C/strong%3E%20%A1%D5%CC%D2&numRows=&limit=25',2,'')
    addDir('---travel ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Travel&menuType=programmes&groupID=152&value2=&viewType=&page=1&groupName=%3Cstrong%3ETravel%3C/strong%3E%20%B7%E8%CD%A7%E0%B7%D5%E8%C2%C7&numRows=&limit=25',2,'')
    addDir('---documentary ', 'http://www.mydootv.com/products_list_wide.php?uri=/TV-Program/Documentary&menuType=programmes&groupID=129&value2=&viewType=&page=1&groupName=%3Cstrong%3EDocumentary%3C/strong%3E%20%CA%D2%C3%A4%B4%D5-%E0%A8%D2%D0%C5%D6%A1&numRows=&limit=25',2,'')
    addDir('films ', 'http://www.mydootv.com/products_list_wide.php?uri=/Film&menuType=programmes&groupID=143,144&value2=&viewType=&page=1&groupName=%3Cstrong%3EFilm%3C/strong%3E%20%C0%D2%BE%C2%B9%B5%C3%EC&numRows=&limit=25',2,'')
    addDir('Music ', 'http://www.mydootv.com/products_list_wide.php?uri=/Music&menuType=programmes&groupID=146,147,148,149,202&value2=&viewType=&page=1&groupName=%3Cstrong%3EMusic%3C/strong%3E%20%B4%B9%B5%C3%D5&numRows=&limit=25',2,'')
    addDir('Sitcom ', 'http://www.mydootv.com/products_list_wide.php?uri=/Sitcom-Comedy&menuType=programmes&groupID=16,97&value2=&viewType=&page=1&groupName=%3Cstrong%3ESitcom%20Comedy%3C/strong%3E%20%AB%D4%B7%A4%CD%C1-%B5%C5%A1&numRows=&limit=25',2,'')
    addDir('Advertising ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Ads&menuType=programmes&groupID=214&value2=&viewType=&page=1&groupName=%3Cstrong%3EAdvertising%3C/strong%3E%20&numRows=&limit=25',2,'')
    addDir('Contest ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Contest&menuType=programmes&groupID=204&value2=&viewType=&page=1&groupName=%3Cstrong%3EContest%3C/strong%3E%20%A1%D2%C3%BB%C3%D0%A1%C7%B4%B5%E8%D2%A7%E6%20&numRows=&limit=25',2,'')
    addDir('Study Language ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Study-Languages&menuType=programmes&groupID=136&value2=&viewType=&page=1&groupName=%3Cstrong%3EStudy%20Languages%3C/strong%3E%20%BD%D6%A1%C0%D2%C9%D2&numRows=&limit=25',2,'')
    addDir('Kids ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Kid&menuType=programmes&groupID=139&value2=&viewType=&page=1&groupName=%3Cstrong%3EKid%3C/strong%3E%20%CA%D3%CB%C3%D1%BA%E0%B4%E7%A1%20&numRows=&limit=25',2,'')
    addDir('Dhamma ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Dhamma&menuType=programmes&groupID=203&value2=&viewType=&page=1&groupName=%3Cstrong%3EDhamma%3C/strong%3E%20%B8%C3%C3%C1%D0%20&numRows=&limit=25',2,'')
    addDir('Special Shows ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Special&menuType=programmes&groupID=159&value2=&viewType=&page=1&groupName=%3Cstrong%3ESpecial%20Show%3C/strong%3E%20%C3%D2%C2%A1%D2%C3%BE%D4%E0%C8%C9&numRows=&limit=25',2,'')
    addDir('Adult +18 ', 'http://www.mydootv.com/products_list_wide.php?uri=/Others/Eighteen-Plus&menuType=programmes&groupID=209&value2=&viewType=&page=1&groupName=%3Cstrong%3E18+(Under%20Admitted)%3C/strong%3E%20%E0%AB%E7%A1%AB%D5%E8%E1%B5%E8%E4%C1%E8%E2%BB%EA&numRows=&limit=25',2,'')
    addDir('Coming soon ', 'http://www.mydootv.com/products_list_wide.php?uri=/Coming-Soon&menuType=programmes&groupID=156&value2=&viewType=&page=1&groupName=%3Cstrong%3EComing%20Soon%20!%3C/strong%3E%20%E0%C3%E7%C7%E6%B9%D5%E9&numRows=&limit=25',2,'')

  
def ShowLiveTV():
    addLink('TV 3 US Server','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_BqIe5vheSOYsU_Rgj_dumA_640_360_696 live=true',14,'','')
    addLink('Sabaidee2 tv','rtmp://202.142.207.150/live/livesabaidee2 swfUrl=http://www.tv-tube.tv/tvchannels/watch/3364/sabaidee-tv swfVfy=true live=true http:http://www.tv-tube.tv/tvchannels/watch/3364/sabaidee-tv',14,'','')
    addLink('Sabaidee tv','rtmp://203.146.170.102:1935/live/livestream3 swfUrl=http://www.r-siam.com/player.swf/ swfVfy=true live=true',14,'','')
    addLink('Oho','rtmp://flash.login.in.th/ohochannel/ohochannel swfUrl=http://www.tv-tube.tv/players/jwflashplayer/player-5.9-licensed.swf swfVfy=true live=true pageUrl=http://www.tv-tube.tv/tvchannels/watch/3300/oho-channel',14,'','')
    addLink('MTV5','rtmp://203.146.170.102:1935/live/livestream2 swfUrl=http://fpdownload.adobe.com/strobe/FlashMediaPlayback.swf/[[DYNAMIC]]/1 swfVfy=true live=true pageUrl=http://mvtv.co.th/wp/tv.php?channel=mv5',14,'','')
    addLink('TV 5','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_4MUCJ_wvTKgnOaeQdGMOk0_640_360_700 live=true',14,'','')
    addLink('TV 7 US Server','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_-fecoVNRTNInw9Ge70vyDg_640_360_696 live=true',14,'','')
    addLink('TV 7 UK Server','rtmp://01-live-01.dootvserver.com:80/uklive7/mp4:uklive7stream9 live=true',14,'','')
    addLink('TV 9 US Server','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_2SNwp7ygQ8cnXqsglDXw48_640_360_700 live=true',14,'','')
    addLink('NBT','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_QUnlGGb8QO8qh1WNiDeRAM_640_360_696 live=true',14,'','')
    addLink('TPBS','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_ia0CJ_OsTBojUFwN7pC4cs_640_360_696 live=true',14,'','')
    addLink('FAN TV','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_nccY09eETbcmPo69h1b898_640_360_696 live=true',14,'','')
    addLink('Green Channel','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38__Scd02cLT7UgTueLpbeerY_640_360_696 live=true',14,'','')
    addLink('Acts Channel','rtmpte://llnwvps348.fc.llnwd.net:80/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_08W_urLlRWAsogFHrCzJsw_640_360_696 live=true',14,'','')
    addLink('Bang Channel','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_ysf1M8xySnYonbbVTtF0oY_640_360_696 live=true',14,'','')
    addLink('Keera Channel','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_ghJ73vaoSgAhHoGi7IZ_uk_640_360_696 live=true',14,'','')
    addLink('Nation Channel','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_UIpYjsh1QPAqASF_Lxww3I_640_360_696 live=true',14,'','')
    addLink('Miracle Channels','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_hc9F6XfTTvcpokzyz8SUUY_640_360_696 live=true',14,'','')
    addLink('WorkPoint TV','rtmp://llnwvps348.fc.llnwd.net:1935/llnwvps348/_definst_/Hmv0CG7hRxokmH9xKend38_xG6WbUtkRSQjQzHjY05rqw_640_360_696 live=true',14,'','')
	
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = '/products_list_wide.php?uri=/advanced_search_result.php?search_in_description=1&menuType=search&groupID='+urllib.quote_plus(searchText.encode('tis-620'))+'&value2=&viewType=&page=1&groupName=&numRows=&limit=25'
        INDEX(url,"1")
        
def INDEX(url,name):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<a href="javascript:playVideo\("player.php\?products_id=([0-9]*?)"\)" class="link" title="(.+?)">[^>]*<img src="(.+?)" ').findall(link)
        for vurl,vname,vimg in vidlist:
            addDir(vname.replace("thai tv : ","").decode("tis-620"),vurl.decode("tis-620"),6,vimg.decode("tis-620"))
        pagelist=re.compile('<table border="0" cellpadding="1" cellspacing="1" width="100%" align="right" class="cornerBoxPage">(.+?)</table>').findall(link)
        navmatch=re.compile('<a href="javascript:(.+?)">(.+?)</a>').findall(pagelist[0])
        for vurl,vname in navmatch:
            vidparts=re.compile('doWorkGetProductsPageList\("(.+?)", "(.+?)", "", "", "(.+?)", "", "(.+?)", "(.+?)",  "productsPageList", "(.+?)"\)').findall(vurl)
            if (len(vidparts) > 0):
                    mentype,groupid,pagenum,numrows,llimit,pagename = vidparts[0]
            else:
                    vidparts=re.compile('doWorkGetProductsPageList\("(.+?)", "(.+?)", "", "", "(.+?)", "(.+?)", "(.+?)", "(.+?)",  "productsPageList", "(.+?)"\)').findall(vurl)
                    mentype,groupid,pagenum,subname,numrows,llimit,pagename = vidparts[0]
            urlfull = "/products_list_wide.php?menuType="+mentype+"&groupID="+groupid+"&value2=&viewType=&page="+pagenum+"&groupName=&numRows="+numrows+"&limit="+llimit
            if name != vname:
                    addDir(vname.encode("utf-8"),urlfull,2,"")
				
def Episodesold(serverurl,pid):
    #try:
        link = GetContent("/products_list_option.php?pID="+pid+"&selectTab=first#first")
        link=''.join(link.splitlines()).replace('\'','"')
        partlist=re.compile('<a href="javascript\:playVideo\("(.+?)"\)">(.+?)</a>').findall(link)
        cnt = 0
        for (chid,vname) in partlist:
                cnt=cnt+1
                addLink(vname.decode("tis-620"),pid+"_"+str(cnt),3,"",serverurl.decode("tis-620"))
    #except: pass
                
def Episodes(region,pid):
    #try:
        filecontent = GetContent("/player_flash_for_free.php?chapters_id=&products_id="+pid+"&ctLB="+region+"&is_hd=1&startVideo=false")
        nowhtsp= ''.join(filecontent.splitlines()).replace('\'','"')
        partcontent=re.compile('<select onchange=(.+?)</select>').findall(nowhtsp)

        partlist=re.compile('<option value=(.+?)><span style="(.+?)">(.+?)</span></option>').findall(partcontent[0])

        for (chapid,vtmp,vname) in partlist:
                chapid=chapid.split(" ")[0]
                addDir(vname.decode("tis-620"),chapid+"_"+region,3,"")

            
    #except: pass
                
def GetVideoFileName(chapterid,region):
        filecontent = GetContent("/player_flash_for_free.php?chapters_id="+chapterid+"&products_id=&ctLB="+region+"&is_hd=1&startVideo=false")
        nowhtsp= ''.join(filecontent.splitlines()).replace('\'','"')
        servname=re.compile('var serverName = "(.+?)"').findall(nowhtsp)[0]
        serurl="http://"+servname+".dootvserver.com"
        filenames=re.compile('if \(isHD == 0\) {        filepath = "(.+?)";    } else {        filepath = "(.+?)";        }').findall(nowhtsp)
        try:
            vidurl = filenames[0][0]
            addLink("Standard Quality",GenerateVideUrl(vidurl,serurl),14,"",serurl)
        except: pass
        try:
            vidurl = filenames[0][1]
            addLink("HD Quality",GenerateVideUrl(vidurl,serurl),14,"",serurl)
        except: pass
		
def GenerateVideUrl(url,serverurl):
    print "timeserver:" + serverurl+"/flowplayer/sectimestamp.php"
    try:
        tempts=GetContent2(serverurl+"/flowplayer/sectimestamp.php").strip()
        tempkey="dootv-secret"
        m = hashlib.md5()
        m.update((((tempkey + "/") + url) + tempts))
        urlcode= serverurl+"/streaming/"+m.hexdigest() + "/" + tempts+"/"+url
        return urlcode
    except:
        d = xbmcgui.Dialog()
        d.ok('NO VIDEO FOUND', "Can't Play video",'Try a different Server Region')

def ChooseServerReg(pid):
        addDir("UK Servers","UK",pid,"")
        addDir("US Servers","US",pid,"")
		
def GetServerList(CountryFile,pid):
        listcontent = GetContent(CountryFile)
        servelist = listcontent.split()
        resul= "http://"+servelist[random.randint(1,len(servelist)-1)].split(":")[0]
        addDir("default Server",resul,pid,"")
        cnt = 0
        for servername in servelist:
                cnt=cnt+1
                addDir("Server " + str(cnt),"http://"+servername.split(":")[0]+"_1",pid,"")
		

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
	
def GetContent2(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent','Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0')
  response = urllib2.urlopen(req)
  html=response.read()
  response.close()
  return html


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
	

def addLink(name,url,mode,iconimage,serverurl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('tis-620'))+"&serverurl="+urllib.quote_plus(serverurl)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('tis-620'))
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
serverurl=None
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
        serverurl=urllib.unquote_plus(params["serverurl"])
except:
        pass
		
sysarg=str(sys.argv[1]) 		
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        INDEX(url,name)
elif mode==3:
        chid,strRegion=url.split("_")
        GetVideoFileName(chid,strRegion)
elif mode==4:
        SEARCH(url)     
elif mode==6:
        ChooseServerReg(url)
elif mode==7:
        GetServerList("/sorted_UK120D.txt",url)
elif mode==8:
        GetServerList("/sorted_US60D.txt",url)
elif mode==9:
        GetServerList("/sorted_01_0111.txt",url)
elif mode==10:
        GetServerList("/sorted_01_0110.txt",url)
elif mode==11:
        GetServerList("/sorted_02_0112.txt",url)
elif mode==12:
        GetServerList("/sorted_01_0711.txt",url)
elif mode==13:
        ShowLiveTV()
elif mode==14:
        playVideo("direct",url)

elif mode > 100:
       Episodes(url,str(mode))
	   
xbmcplugin.endOfDirectory(int(sysarg))
