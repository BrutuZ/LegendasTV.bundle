# -*- coding: utf-8 -*-

import string, os, urllib, copy, zipfile, re, requests#, sys
from unrar import rarfile
# from selenium.webdriver.support.ui import WebDriverWait
# import UnRAR2
# from UnRAR2.rar_exceptions import *


# Network.Timeout = 60
LEGENDAS_MAIN_PAGE = "http://legendas.tv"
LEGENDAS_SEARCH_PAGE = "http://legendas.tv/util/carrega_legendas_busca/"
LEGENDAS_LOGIN_PAGE = "http://legendas.tv/login"
# LEGENDAS_SEARCH_PAGE = "http://legendas.tv/legenda/busca/"

OS_PLEX_USERAGENT = 'plexapp.com v9.0'
subtitleExt = ['utf','utf8','utf-8','sub','srt','smi','rt','ssa','aqt','jss','ass','idx']
#langPrefs2Podnapisi = {'sq':'29','ar':'12','be':'50','bs':'10','bg':'33','ca':'53','zh':'17','cs':'7','da':'24','nl':'23','en':'2','et':'20','fi':'31','fr':'8','de':'5','el':'16','he':'22','hi':'42','hu':'15','is':'6','id':'54','it':'9','ja':'11','ko':'4','lv':'21','lt':'19','mk':'35','ms':'55','no':'3','pl':'26','pt':'32','ro':'13','ru':'27','sr':'36','sk':'37','sl':'1','es':'28','sv':'25','th':'44','tr':'30','uk':'46','vi':'51','hr':'38'}
langPrefs2Legendas = {'por':'1','eng':'2','spa':'3','fr':'4','de':'5','jap':'6','dan':'7','nl':'8','swe':'9','pt':'10','ar':'11','cz':'12','zh':'13','ko':'14','bulg':'15','it':'16','pl':'17'}
isPack = '-'
mediaCopies = {}
username = Prefs["username"]
password = Prefs["password"]

MATCH = 6

def getCookie():
	global TVSession
	TVSession = requests.Session()
	TVSession.mount('http://', requests.adapters.HTTPAdapter(pool_connections=3600, pool_maxsize=3600, max_retries=3))
	# fetch the login page
	TVSession.get(LEGENDAS_LOGIN_PAGE)
	# Log("Biscoitos GET: " + repr(TVSession.cookies))
	# post to the login form
	TVSession.post(LEGENDAS_LOGIN_PAGE, data={'data[User][username]': username, 'data[User][password]': password, 'data[lembrar]': 'on'})
	# Log("Biscoitos POST: " + repr(TVSession.cookies))
	Data.SaveObject('Cookies',TVSession.cookies)
	return TVSession

def Start():
	if username == None or password == None:
		Log("Usuário e/ou senha indefinidos")
		raise SystemExit()
	HTTP.ClearCache()
	HTTP.CacheTime = 10800
	# HTTP.Headers['User-agent'] = OS_PLEX_USERAGENT
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
	HTTP.Headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	HTTP.Headers['Accept-Language'] = 'en-US,en;q=0.8,pt-br;q=0.5,pt;q=0.3'
	HTTP.Headers['Accept-Encoding'] = 'gzip, deflate'
	HTTP.Headers['DNT'] = '1'
	HTTP.Headers['Connection'] = 'keep-alive'
	if Data.Exists('Cookies'):
		global TVSession
		TVSession = requests.Session()
		HTTP.Headers['Cookies'] = Data.LoadObject('Cookies')
	else:
		getCookie()

	# HTTP.RandomizeUserAgent()
	Log("START CALLED")

def ValidatePrefs():
	if username == None or password == None:
		Log("Usuário e/ou senha indefinidos")
	return

#Prepare a list of languages we want subs for
# def getLangList():
	# langList = [Prefs["langPref1"]]
	# if(Prefs["langPref2"] != "None"):
		# langList.append(Prefs["langPref2"])

	# return langList

def tvSearch(params, lang):
	# Log("Params: %s" % urllib.urlencode(params))
	# buscaURL = LEGENDAS_SEARCH_PAGE + urllib.urlencode(params)
	Log("Params: " + string.strip(params['Nome'] + ' ' + params['Temp'] + params['Epi'] + ' ' + params['Source'] + ' ' + params['Grupo']))
	buscaURL = LEGENDAS_SEARCH_PAGE + urllib.quote(string.strip(params['Nome'] + ' ' + params['Temp'] + params['Epi'] + ' ' + params['Source'] + ' ' + params['Grupo']))
	# buscaURL = repr(LEGENDAS_SEARCH_PAGE + urllib.quote(params['Nome'] + " s" + repr(params['Temp']) + "e" + repr(params['Epi']) + " " + params['Grupo']))
	#buscaURL = LEGENDAS_SEARCH_PAGE + params['Nome'] + " s" + params['Temp'] + "e" + params['Epi'] + " " + params['Grupo']
	return simpleSearch(buscaURL, lang)

def movieSearch(params, lang):
	# Log("Params: %s" % urllib.urlencode(params))
	# buscaURL = LEGENDAS_SEARCH_PAGE + urllib.urlencode(params)
	Log("Params: " + params['Nome'] + ' ' + params['Ano'] + ' ' + params['Source'] +  ' ' + params['Grupo'])
	buscaURL = LEGENDAS_SEARCH_PAGE + urllib.quote(string.strip(params['Nome'] + ' ' + params['Ano'] + ' ' + params['Source'] + ' ' + params['Grupo']))
	return simpleSearch(buscaURL, lang)


#Do a basic search for the filename and return all sub urls found
def simpleSearch(buscaURL, lang = 'por'):
	# Log(HTTP.Request("http://legendas.tv/legenda/busca/The%20Big%20Bang%20Theory%20s08e05/1/-/-/-", headers = HTTP.Headers))
	# return
	#phantompath = Platform.OS + '/phantomjs'
	# if Platform.OS == 'Windows':
		# phantompath = phantompath + '.exe'
	# Log("buscaURL: %s" % buscaURL)
	subUrls = []
	pages = 0
	global cond
	#Log("RelPath: " + os.path.realpath(__FILE__))
	# elem = HTML.ElementFromURL(buscaURL)

	# Log("PhantomJS in: " + os.path.realpath(os.getcwd() + '/../../../Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath))
	# browser = selenium.webdriver.PhantomJS(os.path.normcase('../../../Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath))
	# browser.implicitly_wait(300)
	# browser.set_page_load_timeout(300)
	#timeout = 10
	#browser.command_executor._commands['setPageLoadTimeout'] = ('POST', '/session/$sessionId/timeouts')
	#browser.execute("setPageLoadTimeout", {'ms':300000, 'type':'page load'})
	#browser.manage().timeouts().pageLoadTimeout(300000,TimeUnit.MILLISECONDS)
	# wait for the page to load
	# def searchNow(buscaURL):
	linksUm = recurSearch(buscaURL + "/1/-/" + str(pages) + "/-")
	cond = len(linksUm)
	while cond == 24:
		pages = pages + 1
		linksDois = recurSearch(buscaURL + "/1/-/" + str(pages) + "/-")
		for link in linksDois:
			linksUm.append(link)
		cond = len(linksDois)
	for link in linksUm:
		subUrls.append(link)
	return list(set(subUrls))

def HTMLElementFromURL(url):
	request = HTTP.Request(url, timeout = 60, sleep = 1, cacheTime = 0)
	
	if 'http-equiv="refresh"' in request.content:
		request = HTTP.Request(url, cacheTime = 0)
	
	return HTML.ElementFromString(request.content)

def recurSearch(buscaURL, urlList=0):
	subUrls = []
	elem = ''
	subpages = ''
	for attempt in range(15):
		try:
			# HTTP.ClearCookies()
			elem = HTML.ElementFromURL(buscaURL, cacheTime=10800, timeout=60, sleep=1)
			# Log(HTML.StringFromElement(elem))
			# browser.get(str(buscaURL))
			# wait for element to show
			# WebDriverWait(browser, 300).until(lambda x: x.find_element_by_id('resultado_busca'))
			# browser.find_element_by_id("resultado_busca")
		except:
			Log("Error. Site may be experiencing some problems. Retrying")
			HTTP.ClearCache()
		else:
			# HTTP.ClearCache()
			# Log("This look serious, maybe we should wait a little longer")
			# raise
			# continue
			break
	else:
		Log("Failed too many times. It must be offline, giving up...")
		raise SystemExit()
		#raise 'TIMEOUT'
		# sys.exit()
		#return subUrls
	# page_source = browser.page_source
	# store it to string variable
	# browser.quit()###
	# Log(page_source)

	# Log("HTML: %s" % elem)
	# subpages = elem.xpath("//div[@class='gallery clearfix list_element']/article/div/div/p[1]/a/@href")
	subpages = elem.xpath("//div[@class='f_left']/p[1]/a/@href")
	Log("Subpages: %d" % len(subpages))
	for subpage in subpages:
		subPageUrl = LEGENDAS_MAIN_PAGE + subpage
		Log("Subpage: %s" % subPageUrl)
		#pageElem = HTML.ElementFromURL(subPageUrl)
		#downloadUrl = getDownloadUrlFromPage(pageElem)
		downloadUrl = subPageUrl.replace("download","downloadarquivo")
		#Log("DownloadURL: %s" % downloadUrl)
		subUrls.append(downloadUrl)
	return subUrls


	# linksUm = searchNow(buscaURL)
	# linksDois = linksUm
	# cond = len(linksUm)
	# pages = 1
	# while cond == 24:
		# linksDois = searchNow(buscaURL + "/-/" + str(pages) + "/-")
		# linksUm.append(linksDois)
		# pages = pages + 1
		# cond = len(linksDois)

	# return linksUm

# def getDownloadUrlFromPage(pageElem):
	# dlPart = pageElem.xpath("//*[@id='resultado_busca']/div/article/div/div/p[1]/a/@href")[0]
	# Log("Result: %s" % dlPart)
	# return LEGENDAS_MAIN_PAGE + dlPart

# def getDownloadUrlFromPage2(pageElem):
	# dlPart = pageElem.xpath("//div[@class='podnapis_tabele_download']//a[contains(@href,'download')]/@href")[0]
	# return LEGENDAS_MAIN_PAGE + dlPart

# def getDownloadUrlFromPage1(pageElem):
	# dlPart = None
	# funcName = None
	# dlScriptTag = pageElem.xpath("//script[contains(text(),'download')]/text()")[0]
	# Log("dlScriptTag: %s" % dlScriptTag)
	# p = re.compile("'.*'")
	# m = p.search(dlScriptTag)
	# if (m != None):
		# dlPart = m.group()
		# dlPart = dlPart[1:len(dlPart) - 1]
		# Log("dlPart: %s" % dlPart)

	# p = re.compile("\s(\w*)")
	# m = p.search(dlScriptTag)
	# funcName = string.strip(m.group())
	# Log("funcName: :%s" % funcName)

	# argScriptXpath = "//script[contains(text(),'%s')]/text()" % funcName
	# Log("argScriptXpath: %s" % argScriptXpath)
	# argScriptTag = pageElem.xpath(argScriptXpath)[1]
	# Log("argScriptTag: %s" % argScriptTag)

	# p = re.compile("\('(\w+)")
	# m = p.search(argScriptTag)
	# arg = m.group(1)
	# Log("arg: %s" % arg)

	# dlPage = LEGENDAS_MAIN_PAGE + dlPart + arg
	# Log("dlPage: %s" % dlPage)
	# return dlPage

class SubInfo():
	def __init__(self, lang, url, sub, name):
		self.lang = lang
		self.url = url
		self.sub = sub
		self.name = name
		self.ext = string.split(self.name, '.')[-1]


def doSearch(data, lang, isTvShow):
	if(isTvShow):
		return tvSearch(data, lang)

	return movieSearch(data, lang)

def searchSubs(data, isTvShow, lang='por'):
	global MATCH
	subUrls = []
	d = {'Temp':'','Epi':'','Source':'','Grupo':'','Ano':'','Nome':string.split(data['Filename'].lower(),os.sep)[-1][:-4]}
	if not ' ' in data['Filename']:
		Log("Searching for filename")
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		# if not subUrls or len(subUrls) < 5:
		if len(subUrls) < 5:
			# Log("Replacing dots with spaces: " % len(subUrls))
			# d['Nome'] = d['N%d subs found - ome'].replace('.',' ')
			if "the " in d['Nome'] or "The " in d['Nome'] or "the." in d['Nome'] or "The." in d['Nome']:
				Log("%d subs found - Removing 'The' prefix" % len(subUrls))
				d['Nome'] = re.sub("(?i)the.","", d['Nome'],1)
				subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		if d['Nome'] != d['Nome'].translate(None,"'\"!?:()"):
		# if not subUrls and d['Nome'] != d['Nome'].translate(None,"'\"!?:"):
			Log("%d subs found - Stripping special characters: " % len(subUrls))
			d['Nome'] = d['Nome'].translate(None,"'\"!?:()")
			subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		if ' ' in d['Nome'] and len(subUrls) < 5:
		# if not subUrls and ' ' in d['Nome'] and len(subUrls) < 5:
			Log("%d subs found - Replacing spaces with dots: " % len(subUrls))
			d['Nome'] = d['Nome'].replace(' ','.')
			subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		if subUrls and MATCH == 1:
			return subUrls

	if isTvShow and d['Temp'] == 's00':
		d = dict(data) # make a copy so that we still include release group for other searches
		Log("Special episode, let's report that")
		d['Temp'] = 'Special'
		d['Epi'] = ''
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		if not subUrls:
			Log("Special episode, removing s##e## and hoping for the best")
			d['Temp'] = ''
			subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
			if not subUrls:
				d['Source'] = ''
				d['Grupo'] = ''
				Log("We need to go deeper")
				subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))

	d = dict(data) # make a copy so that we still include release group for other searches
	# d['Source'] = ''
	# d['Grupo'] = ''
	subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))

	if d['Nome'] != d['Nome'].translate(None,"'\"!?:()"):
	# if not subUrls and d['Nome'] != d['Nome'].translate(None,"'\"!?:"):
		Log("%d subs found - Stripping special characters: " % len(subUrls))
		d['Nome'] = d['Nome'].translate(None,"'\"!?:()")
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	if '.' in d['Nome'] and len(subUrls) < 5:
	# if not subUrls and '.' in d['Nome'] and len(subUrls) < 5:
		Log("%d subs found - Replacing dots with spaces: " % len(subUrls))
		d['Nome'] = d['Nome'].replace('.',' ')
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	# if not subUrls and isTvShow:
		# Log("%d subs found - Spacing Season Episode" % len(subUrls))
		# d['Temp'] = d['Temp'] + ' '
		# subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	if isTvShow and len(subUrls) < 5:
		d['Grupo'] = ''
		d['Source'] = ''
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		d = dict(data) # make a copy so that we still include release group for other searches
	if data['Source'] and len(subUrls) < 5:
	# if d['Source'] and not subUrls and len(subUrls) < 5:
		# Log("%d subs found - Adding source type" % len(subUrls))
		Log("%d subs found - Removing source type" % len(subUrls))
		d['Grupo'] = data['Grupo']
		d['Source'] = ''
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	if data['Grupo'] and len(subUrls) < 5:
	# if data['Grupo'] and not subUrls and len(subUrls) < 5:
		# Log("%d subs found - Removing release group" % len(subUrls))
		Log("%d subs found - Going for source type" % len(subUrls))
		# del d['Grupo']
		d['Grupo'] = ''
		d['Source'] = data['Source']
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	if isTvShow and len(subUrls) < 1:
		d['Grupo'] = ''
		d['Source'] = ''
		d['Epi'] = ''
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
		d = dict(data) # make a copy so that we still include release group for other searches
	if not isTvShow and len(subUrls) < 5:
	# if not subUrls and not isTvShow:
		Log("%d subs found - Removing Year" % len(subUrls))
		d['Ano'] = ''
		subUrls = subUrls + list(set(doSearch(d, lang, isTvShow)) - set(subUrls))
	Log(repr(subUrls))
	if data['Downloaded']:
		Log(repr(data['Downloaded']))
	return subUrls

def checkArchive(subsArchive,legExt,subUrl,data):
	global MATCH
	subArchive = []
	for parseA in subsArchive:
		# Log(parseA)
		if legExt == "rar":
			nameA = parseA.filename
		elif legExt == "zip":
			nameA = parseA
		# Log('\n Archive:' + string.split(data['Filename'],os.sep)[-1] + ' | Filename \n' + nameA + ' | subtitle')
		data['Filename'] = data['Filename'].strip('"')
		# Log("Match: %d" % MATCH)
		# Log(nameA + ' ' + repr(data))
		if not '.srt' in nameA:
			Log("%s | NOT a subtitle" % nameA)
			continue
		if MATCH > 1:
			if data['Filename'].lower()[:-4] == nameA.lower()[:-4]:
				Log('Perfect match! \n' + data['Filename'] + ' | Filename \n' + nameA + ' | subtitle')
				subArchive = [parseA]
				subUrls = [subUrl]
				MATCH = 1
				Log("Match: %d" % MATCH)
				break
		if MATCH > 2:
			if data['Filename'].lower()[:-4] in nameA.lower():
				Log('Perfect"ish" match! \n' + data['Filename'] + ' | Filename \n' + nameA + ' | subtitle')
				subArchive = [parseA]
				subUrls = [subUrl]
				MATCH = 2
				Log("Match: %d" % MATCH)
				continue
		if MATCH > 3:
			if len(data['Grupo']) >= 2:
				if data['Nome'].lower() in nameA.lower() or data['Nome'].replace('.',' ').lower() in nameA.lower() or data['Nome'].replace('.',' ').translate(None,"'\"!?:").lower() in nameA.lower() or data['Nome'].replace(' ','.').lower() in nameA.lower() or data['Nome'].replace(' ','.').translate(None,"'\"!?:").lower() in nameA.lower():
					if data['Temp'] in nameA.lower():
						if data['Epi'] in nameA.lower():
							if data['Grupo'].lower().strip() in nameA.lower():
								Log('Decent match! \n' + data['Filename'] + ' | Filename \n' + nameA + ' | subtitle')
								subArchive = [parseA]
								MATCH = 3
								Log("Match: %d" % MATCH)
								continue
		if MATCH > 4:
			if data['Nome'].lower() in nameA.lower() or data['Nome'].replace('.',' ').lower() in nameA.lower() or data['Nome'].replace('.',' ').translate(None,"'\"!?:").lower() in nameA.lower() or data['Nome'].replace(' ','.').lower() in nameA.lower() or data['Nome'].replace(' ','.').translate(None,"'\"!?:").lower() in nameA.lower():
				if data['Temp'] in nameA.lower():
					if data['Epi'] in nameA.lower():
						if data['Source'].lower().strip() in nameA.lower() and len(data['Source']) >= 2:
							Log('"Meh" match! \n' + data['Filename'] + ' | Filename \n' + nameA + ' | subtitle')
							if MATCH > 3:
								# subArchive = [parseA]
								subArchive.append(parseA)
							MATCH = 4
							Log("Match: %d" % MATCH)
							continue
		if MATCH > 5:
			subArchive = []
			Log("Match: %d" % MATCH)
			# MATCH = 6
		Log('Nothing matches - disregarding \n' + data['Filename'] + ' | Filename \n' + nameA + ' | subtitle')
		# if parseA in subArchive:
			# subArchive.remove(parseA)

	return subArchive

def getSubsForPart(data, isTvShow=True):
	global MATCH
	MATCH = 6
	siList = []
	# for lang in getLangList():
		#Log("Lang: %s,%s" % (lang, langPrefs2Legendas[lang]))
		# data['Lang'] = langPrefs2Legendas[lang]
	data['Lang'] = "por"
	lang = data['Lang']
	subUrls = searchSubs(data, isTvShow)
	# subUrls = ['local']
	if not subUrls:
		Log("No subtitles found =(")
	else:
		# tmpSubUrls = subUrls
		for subUrl in subUrls:
			if data['Filename'] in Dict and subUrl in Dict[data['Filename']]:
				Log("Nothing new")
				continue
			if MATCH == 1:
				Log ("Perfection achieved")
				break
			if (subUrl in s for s in data['Downloaded']) and data['Downloaded']:
			# if subUrl in data['Downloaded']:
				Log("Been there, done that")
				continue
			#Log(HTTP.Request(subUrl, headers))
			#subArchive = Archive.ZipFromURL(subUrl)
			# Data.Save("downRar", subUrl)
			# downRar = Data.Load("downRar")
			# Log(downRar)
			#subArchive.write(rarfile.RarFile(subUrl))
			#logStr = urllib.urlretrieve(subUrl)
			# logStr = subUrl
			# Log("170...")
			# Log(str(logStr))
			#downRar.write(logStr)
			# archive.write(rarfile.RarFile(downRar))
			#archive = rarfile.RarFile(str(logStr))
			global TVSession
			if not TVSession.cookies:
				TVSession.cookies = Data.LoadObject('Cookies')
				# getCookie()
			archurl = TVSession.get(subUrl).url
			try:
				# archurl = 'G:\\Plex\\Data\\Plex Media Server\\Plug-in Support\\Data\\com.plexapp.agents.legendastv\\templeg.rar'
				# dload = TVSession.get(archurl).content
				# dload = urllib.urlopen(subUrl)
				# archurl = dload.geturl()
				legExt = string.split(archurl,'.')[-1].strip('"')
				Log("Getting subtitle from: %s" % archurl)
				if legExt == "rar":
					req = HTTP.Request(archurl, headers=TVSession.headers, cacheTime = 300)
					# Log("URL: " + repr(req.headers))
					dload = req.content
					for attempt in range(15):
						try:
							Data.Save('templeg.rar',dload)
							# urllib.urlretrieve(subUrl, 'templeg.rar')
						except:
							Log("ERROR. Retrying...")
						else:
							break
					else:
						Log("Failed too many times. Giving up...")
					archive = rarfile.RarFile('DataItems/templeg.rar')
					# archive = UnRAR2.RarFile('templeg.rar')
					subArchive = archive.infolist()
					Log("RAR Items: %s" % len(subArchive))
					Log(archive.namelist())
				elif legExt == "zip":
					for attempt in range(15):
						try:
							subArchive = Archive.ZipFromURL(archurl)
							archive = subArchive
						except:
							Log("ERROR. Retrying...")
						else:
							break
					else:
						Log("Failed too many times. Giving up...")
				else:
					Log('Unkown file format: %s' % legExt)
					getCookie()
					continue
			except:
				Log("Error downloading subtitle")
				continue
			#Data.Save("LegRar.rar", Leg)
			# archive.write(rarfile.RarFile,"LegRar.rar")
			# tmpSubArchive = subArchive
			subArchive = checkArchive(subArchive,legExt,subUrl,data)
			# Log("Match: %d" % MATCH)
			# Log("subArchive: " + repr(subArchive))
			for parse in subArchive:
				# subData = '/><=ó'
				if legExt == "rar":
					name = parse.filename
				elif legExt == "zip":
					name = parse

				if not '.srt' in name:
				#if name in['Legendas.tv.url','Legendas.tv.txt','Créditos.txt']:
					# Log("Ignoring garbage: %s" % name)
					continue
				Log("Name in pack: %s" % name)
				# if '/' in name or '\\' in name or 'MACOSX' in name:
					# Log("Ignoring folder")
					# continue
				#legFile = tempfile.NamedTemporaryFile(suffix='.srt', prefix=name, delete=False)

				if legExt == "rar":
					#legFile = archive.extract(name)
					legFile = archive.read_files(name)
					#Log(legFile)
					#Log("Temp: %s" % repr(legFile[0][1]))
					subData = legFile[0][1]
					#archive.destruct()
					##archive.extract(name)
					#legZip = zipfile.ZipFile('templeg.zip', 'w')
					#legZip.write(name.encode("latin-1"))
					## if os.sep in name:
						## name = string.split(name,os.sep)[-1]
						## Log("Removing folder from filename: %s" % name)
					#subData = legZip.read(name)
					#legZip.close()
					# Data.Save("LegFile", archive.extract(name))
					#archive.extract(name, Data.SaveObject("LegFile"))
					#subData = open(name)
					# subData = Data.Load("LegFile")
					# subData.write(archive.extract(name))
					#subData = legFile.file
				elif legExt == "zip":
					try:
						subData = archive[name]
					except:
						Log("Oops!")
						subData = 0
				else:
					Log("Wait, wat?")
				Log(repr(subData))
				subReg = subUrl + '.' + legExt + '/score=' + str(MATCH) + '&leg=' + name
				si = SubInfo(lang, subReg, subData, name)
				# si = SubInfo(lang, subUrl, subData, name)
				#Log(repr(si))
				siList.insert(0,si)
				Dict[data['Filename']] = subReg
				# siList.append(si)
				# Data.Remove("LegFile")
				#legFile.close()
				#if legExt == "rar":
					#os.unlink(name)
					#os.unlink('templeg.zip')

			if legExt == "rar":
				# os.unlink('templeg.rar')
				Data.Remove("templeg.rar")
	return siList

def getReleaseGroup(filename):
	# tmpFile = string.replace(filename, '-', '.')
	group = ''
	separators = ['.','-','[']
	for sep in separators:
		if sep in filename:
			group = string.split(filename[:-4],sep)[-1]
	#splitName = string.split(splitName,'.')[-2]
	group = group.translate(None,'[-].')
	# if '.' in group or ' ' in group:
		# group = ''
	
	#NEWSTUFF
	#tranTab = string.maketrans('[-]','.. ')
	## if tmpFile != filename:
		## tmpFile = string.strip(']').replace(filename, '[', '.')
	#tmpFile = filename.translate(tranTab)
	#if ".." in tmpFile:
		#tmpFile = tmpFile.replace("..",".")
	#splitName = string.split(tmpFile, '.')
	## splitName = string.split(splitFileName[-1], '.')
	#group = splitName[-2].strip()
	## Log("Filename: %s \r\n tmpFile: %s \r\n splitName: %s \r\n Group: %s" % (repr(filename),repr(tmpFile),repr(splitName),repr(group)))
	return group

def getVideoSource(filename):
	sources = ['HDTV','WEB-DL','WEBDL','WEB DL','WEB.DL','WEBRIP','Web-Rip','Web Rip','Web.Rip','DVD','BDR','BDRip','BRRip','Blu-Ray','Blu.Ray','BluRay']
	vsource = ''
	for source in sources:
		if source.lower() in filename.lower():
			vsource = source
	return vsource

class LegendasTVAgentMovies(Agent.Movies):
	name = 'Legendas.tv'
	languages = [Locale.Language.English]
	primary_provider = False
	# contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):
		Log("MOVIE SEARCH CALLED")
		mediaCopy = copy.copy(media.primary_metadata)
		uuid = String.UUID()
		mediaCopies[uuid] = mediaCopy
		results.Append(MetadataSearchResult(id = uuid, score = 100))

	def update(self, metadata, media, lang):
		Log("MOVIE UPDATE CALLED")
		mc = mediaCopies[metadata.id]
		for item in media.items:
			for part in item.parts:
				# Log("Title: %s" % media.title)
				# Log("Filename: %s" % part.file)
				# Log("Year: %s" % mc.year)
				# Log("Release group %s" % getReleaseGroup(part.file))

				data = {}
				data['Nome'] = str(media.title)
				if mc.original_title:
					data['Nome'] = str(mc.original_title).translate(None,":")
				if ' ' in data['Nome']:
					data['Nome'] = '"' + data['Nome'].translate(None,":") + '"'
				data['Grupo'] = getReleaseGroup(string.split(str(part.file),os.sep)[-1])
				data['Ano'] = str(mc.year)
				data['Filename'] = string.split(str(part.file),os.sep)[-1]
				data['Source'] = getVideoSource(string.split(str(part.file),os.sep)[-1])
				data['Temp'] = ''
				data['Epi'] = ''
				Log("File: '%s' " % data['Filename'])
				Log("Movie: '%s'" % data['Nome'])
				Log("Year: %s" % data['Ano'])
				Log("Video Source: '%s'" % data['Source'])
				Log("Release Group: '%s'" % data['Grupo'])
				data['Downloaded'] = []
				siList = 0
				if len(list(part.subtitles)) < 1:
					siList = getSubsForPart(data, False)
				for lng in part.subtitles:
					Log("Existing sub lang: " + repr(lng))
					porta = list(part.subtitles[lng])
					for subsubs in porta:
						Log("Existing sub: " + repr(subsubs))
						data['Downloaded'].append(subsubs)
						if ('score=1' in subsubs) or ('score=2' in subsubs) or ('score=3' in subsubs):
							Log("Good enough already")
						else:
							siList = getSubsForPart(data, False)
						# part.subtitles['pt'][subsubs] = Proxy.Media('')
					if len(porta) < 1:
						siList = getSubsForPart(data, False)

				if siList:
					for si in siList:
						part.subtitles[Locale.Language.Match(si.lang)][si.url] = Proxy.Media(si.sub, ext=si.ext, format=si.ext) 

		del(mediaCopies[metadata.id])


class LegendasTVAgentTvShows(Agent.TV_Shows):
	name = 'Legendas.tv'
	languages = [Locale.Language.English]
	primary_provider = False
	# contributes_to = ['com.plexapp.agents.thetvdb','com.plexapp.agents.the-movie-database']

	def search(self, results, media, lang):
		Log("TV SEARCH CALLED")
		results.Append(MetadataSearchResult(id = 'null', score = 100))

	def update(self, metadata, media, lang):
		Log("TvUpdate. Lang %s" % lang)
		for season in media.seasons:
			for episode in media.seasons[season].episodes:
				for item in media.seasons[season].episodes[episode].items:
					for part in item.parts:
						data = {}
						data['Nome'] = str(media.title).translate(None,":")
						# if ' ' in data['Nome']:
							# data['Nome'] = '"' + data['Nome'] + '"'
						data['Temp'] = "s" + str(season).rjust(2,str("0"))
						data['Epi'] = "e" + str(episode).rjust(2,str("0"))
						data['Source'] = getVideoSource(string.split(str(part.file),os.sep)[-1])
						data['Grupo'] = getReleaseGroup(string.split(str(part.file),os.sep)[-1])
						data['Filename'] = string.split(str(part.file),os.sep)[-1]
						if ' ' in data['Filename']:
							data['Filename'] = '"' + data['Filename'] + '"'
						Log("File: '%s'" % data['Filename'])
						Log("Show: '%s'" % data['Nome'])
						Log("Season: '%s', Ep: '%s'" % (data['Temp'], data['Epi']))
						Log("Video Source: '%s'" % data['Source'])
						Log("Release Group: '%s'" % data['Grupo'])
						data['Downloaded'] = []
						siList = 0
						if len(list(part.subtitles)) < 1:
							siList = getSubsForPart(data)
						for lng in part.subtitles:
							Log("Existing sub lang: " + repr(lng))
							porta = list(part.subtitles[lng])
							if len(porta) < 1:
								siList = getSubsForPart(data)
							else:
								for subsubs in porta:
									Log("Existing sub: " + repr(subsubs))
									data['Downloaded'].append(subsubs)
									if ('score=1' in subsubs) or ('score=2' in subsubs) or ('score=3' in subsubs):
										Log("Good enough already")
									else:
										siList = getSubsForPart(data)
									# part.subtitles['pt'][subsubs] = Proxy.Media('')

						if siList:
							for si in siList:
								part.subtitles[Locale.Language.Match(si.lang)][si.url] = Proxy.Media(si.sub, 0, ext=si.ext, format=si.ext)