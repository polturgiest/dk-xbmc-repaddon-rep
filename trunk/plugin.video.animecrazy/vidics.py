import urllib,urllib2,re,sys,xbmcplugin,xbmcgui,cookielib,os
#vidlcs.com -- nixa

def CATS():
        addDir('latest movies','http://www.vidics.com/index.php',2,'')
	addDir('comedy','http://www.vidics.com/movies.php?c=comedy',1,'')
	addDir('drama','http://www.vidics.com/movies.php?c=drama',1,'')
	addDir('action','http://www.vidics.com/movies.php?c=action',1,'')
	addDir('adventure','http://www.vidics.com/movies.php?c=adventure',1,'')
	addDir('horror','http://www.vidics.com/movies.php?c=horror',1,'')
	addDir('music','http://www.vidics.com/movies.php?genre=7',1,'')
	addDir('animation','http://www.vidics.com/movies.php?c=animation',1,'')
	addDir('documentaries','http://www.vidics.com/movies.php?c=documentary',1,'')
	addDir('search','http://www.vidics.com/',4,'')
	addDir('best rated','http://www.vidics.com/movies.php?best=1',1,'')

def INDEX(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
	code=re.sub('&quot;','',link)
        code1=re.sub('&#039;','',code)
        code2=re.sub('&#038;','',code1)
	code3=re.sub('&#8217;','',code2)
        code4=re.sub('&amp;','&',code3)
        code5=re.sub('#x26;','',code4)
        code6=re.sub('#x27;','',code5)
        code7=re.sub('&#xFB;','',code6)
        code8=re.sub('&','`',code7)
        code9=re.sub("`",'',code8)
	names=re.compile('style=".+?" href=".+?">(.+?)</a></td>').findall(code9)
	urls=re.compile('style=".+?" href="(.+?)">.+?</a></td>').findall(code9)
	thumbs=re.compile('<td width="87" valign="top" class="cat_item_img"> <a  rel="nofollow" href=".+?"><img src="posters/(.+?)" width=".+?" height=".+?"').findall(link)
	plot=re.compile('<div class="cat_content_desc">\n(.+?)\n').findall(code9)
	nxt=re.compile("<td><a href='(.+?)'> (.+?) </a></td>").findall(link)
	videos=[(names[i],urls[i],thumbs[i],plot[i])for i in range (0,len(urls))]
 	for name,url,thumb,plot in videos:
                addDir(name.replace('(',' ').replace(')',' ').replace('2009',' ').replace('2008',' ').replace('2007',' ').replace('2006',' ').replace('2005',' ').replace('2004',' ').replace('2003',' ').replace('2002',' ').replace('2001',' ').replace(':',' '),'http://www.vidics.com'+url,3,'http://www.vidics.com/posters/'+thumb,plot.replace('</div>',' '))
	for url,name in nxt:
		addDir(' Go to page '+name,'http://www.vidics.com/'+url,1,'http://www.clker.com/cliparts/0/5/7/9/1195435734741708243kuba_arrow_button_set_2.svg.hi.png')

def INDEX2(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        page = urllib2.urlopen(req)
	link=page.read()
	code=re.sub('&quot;','',link)
        code1=re.sub('&#039;','',code)
        code2=re.sub('&#038;','',code1)
	code3=re.sub('&#8217;','',code2)
        code4=re.sub('&amp;','&',code3)
        code5=re.sub('#x26;','',code4)
        code6=re.sub('#x27;','',code5)
        code7=re.sub('&#xFB;','',code6)
        code8=re.sub('&','`',code7)
        code9=re.sub("`",'',code8)
    	latest=re.compile('    <a rel=.+? href="(.+?)">	<img src="(.+?)" width="87" height="126" alt="" border="0" /></a><br>\n        <a href=".+?">(.+?)</a>').findall(code9)
	for url,thumb,name in latest:
		addDir(name.replace('(',' ').replace(')',' ').replace('2009',' ').replace('<br>',' '),'http://www.vidics.com'+url,3,'http://www.vidics.com/'+thumb)

	                     
def PARTS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
      	mvshareblk=re.compile('<a href=".+?movshare.net/video/(.+?)" target="_blank"').findall(link)
      	mvshare=re.compile('<a href=".+?movshare.net/video/(.+?)\n"').findall(link)
      	mv2=re.compile('".+?www2.movshare.net/.+?v=(.+?)"').findall(link)
      	nv=re.compile('<a href="http://www.novamov.com/video/(.+?)"').findall(link)
      	nv2=re.compile('<a href="http://www.novamov.com/video/(.+?)\n').findall(link)
      	divx=re.compile('<a href="http://www.divxstage.net/video/(.+?)\n').findall(link)
      	divx2=re.compile('".+?divxstage.net/video/(.+?)"').findall(link)

	for url in divx2:
		try:
			req = urllib2.Request('http://www.divxstage.net/video/'+url)
			response = urllib2.urlopen(req)
			the_page = response.read()
			swap=re.compile('<embed type="video/divx" src="(.+?)&.+?"').findall(the_page)
			if not swap: swap=re.compile('<embed type="video/divx" src="(.+?)"').findall(the_page)
			if not swap: swap=re.compile('"file","(.+?)&ec_rate=.+?"').findall(the_page)
			for url in swap:
				addLink(name,swap[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
		except: pass

	for url in divx:
		try:
			req = urllib2.Request('http://www.divxstage.net/video/'+divx[0])
			response = urllib2.urlopen(req)
			the_page = response.read()
			swap=re.compile('<embed type="video/divx" src="(.+?)&.+?"').findall(the_page)
			if not swap: swap=re.compile('<embed type="video/divx" src="(.+?)"').findall(the_page)
			if not swap: swap=re.compile('"file","(.+?)&ec_rate=.+?"').findall(the_page)
			for url in swap:
				addLink(name,swap[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
		except: pass

	for url in nv:
		try:
			link2='http://www.novamov.com/video/'+nv[0]
      			req = urllib2.Request(link2)
        		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        		response = urllib2.urlopen(req)
        		now=response.read()
			flv=re.compile('"file","(.+?)"').findall(now)
			for url in flv:
                		addLink(name,flv[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
		except: pass

	for url in nv2:
		try:
			link2='http://www.novamov.com/video/'+nv2[0]
      			req = urllib2.Request(link2)
        		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        		response = urllib2.urlopen(req)
        		now=response.read()
			flv=re.compile('"file","(.+?)"').findall(now)
			for url in flv:
                		addLink(name,flv[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
		except: pass


	for url in mvshare:
		try:
			link3='http://www.movshare.net/video/'+url
			user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
			values = {'name' : 'watch','action' : '#'}
			headers = { 'User-Agent' : user_agent }
			data = urllib.urlencode(values)
			req = urllib2.Request(link3, data, headers)
			response = urllib2.urlopen(req)
			the_page = response.read()
			swap=re.compile('<embed type="video/divx" src="(.+?)&.+?"').findall(the_page)
			if not swap: swap=re.compile('<embed type="video/divx" src="(.+?)"').findall(the_page)
			if not swap: swap=re.compile('"file","(.+?)"').findall(the_page)
			try:		
				addLink(name,swap[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
			except: pass
		except: pass

	for url in mvshareblk:
		try:
			link3='http://www.movshare.net/video/'+url
			user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
			values = {'name' : 'watch','action' : '#'}
			headers = { 'User-Agent' : user_agent }
			data = urllib.urlencode(values)
			req = urllib2.Request(link3, data, headers)
			response = urllib2.urlopen(req)
			the_page = response.read()
			swap=re.compile('<embed type="video/divx" src="(.+?)&.+?"').findall(the_page)
			if not swap: swap=re.compile('<embed type="video/divx" src="(.+?)"').findall(the_page)
			if not swap: swap=re.compile('"file","(.+?)"').findall(the_page)
			try:		
				addLink(name,swap[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
			except: pass
		except: pass


	for url in mv2:
		try:
			link4='http://www.movshare.net/video/'+url
			user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
			values = {'name' : 'watch','action' : '#'}
			headers = { 'User-Agent' : user_agent }
			data = urllib.urlencode(values)
			req = urllib2.Request(link4, data, headers)
			response = urllib2.urlopen(req)
			the_page = response.read()
			swap=re.compile('<embed type="video/divx" src="(.+?)&.+?"').findall(the_page)
			if not swap: swap=re.compile('<embed type="video/divx" src="(.+?)"').findall(the_page)
			if not swap: swap=re.compile('"file","(.+?)"').findall(the_page)
			try:		
				addLink(name,swap[0],'http://www.bitdefender.com/files/KnowledgeBase/img/movie_icon.png')
			except: pass
		except: pass


def SEARCH():
        keyb = xbmc.Keyboard('', 'Search Vidlcs')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText()
                encode=urllib.quote(search)
                req = urllib2.Request('http://www.vidics.com/movies.php?s='+encode+'&Search.x=0&Search.y=0')
	        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        	page = urllib2.urlopen(req)
		link=page.read()
		code=re.sub('&quot;','',link)
        	code1=re.sub('&#039;','',code)
        	code2=re.sub('&#038;','',code1)
		code3=re.sub('&#8217;','',code2)
        	code4=re.sub('&amp;','&',code3)
        	code5=re.sub('#x26;','',code4)
        	code6=re.sub('#x27;','',code5)
        	code7=re.sub('&#xFB;','',code6)
        	code8=re.sub('&','`',code7)
        	code9=re.sub("`",'',code8)
		names=re.compile('style=".+?" href=".+?">(.+?)</a></td>').findall(code9)
		urls=re.compile('style=".+?" href="(.+?)">.+?</a></td>').findall(code9)
		thumbs=re.compile('<td width="87" valign="top" class="cat_item_img"> <a  rel="nofollow" href=".+?"><img src="posters/(.+?)" width=".+?" height=".+?"').findall(link)
		plot=re.compile('<div class="cat_content_desc">\n(.+?)\n').findall(code9)
		nxt=re.compile("<td><a href='(.+?)'> (.+?) </a></td>").findall(link)
		videos=[(names[i],urls[i],thumbs[i],plot[i])for i in range (0,len(urls))]
 		for name,url,thumb,plot in videos:
                	addDir(name.replace('(',' ').replace(')',' ').replace('2009',' ').replace('2008',' ').replace('2007',' ').replace('2006',' ').replace('2005',' ').replace('2004',' ').replace('2003',' ').replace('2002',' ').replace('2001',' ').replace(':',' '),'http://www.vidics.com'+url,3,'http://www.vidics.com/posters/'+thumb,plot.replace('</div>',' '))
		for url,name in nxt:
			addDir(' Go to page '+name,'http://www.vidics.com/'+url,1,'http://www.clker.com/cliparts/0/5/7/9/1195435734741708243kuba_arrow_button_set_2.svg.hi.png')


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

def geturl(url):
        try:
                urlfetch.fetch(url)
        except :
                pass

def addDir(name,url,mode,thumbnail,plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "plot": plot} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

     
      
def addLink(name,url,thumbnail):
        ok=True
        def Download(url,dest):
                dp = xbmcgui.DialogProgress()
                dp.create("Fast Pass Tv Download","Downloading File",url)
                urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
        def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
                try:
                        percent = min((numblocks*blocksize*100)/filesize, 100)
                        print percent
                        dp.update(percent)
                except:
                        percent = 100
                        dp.update(percent)
                if dp.iscanceled():
                        dp.close()
        if xbmcplugin.getSetting("Download Flv") == "true":
                dialog = xbmcgui.Dialog()
                path = dialog.browse(3, 'Choose Download Directory', 'files', '', False, False, '')
                Download(url,path+name+'.flv')
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


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
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
        print "categories"
        CATS()
elif mode==1:
        print "PAGE"
        INDEX(url,name)
elif mode==2:
        print "PAGE"
        INDEX2(url,name)
elif mode==3:
        print "PAGE"
        PARTS(url,name)
elif mode==4:
        print "SEARCH  :"+url
        SEARCH()



        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
