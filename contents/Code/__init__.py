#hdbits.org

import string, os, urllib, zipfile, re, copy, selenium, selenium.common, selenium.webdriver, selenium.webdriver.support.ui
from unrar import rarfile
from selenium.webdriver.support.ui import WebDriverWait


LEGENDAS_MAIN_PAGE = "http://legendas.tv"
LEGENDAS_SEARCH_PAGE = "http://legendas.tv/busca?q="

OS_PLEX_USERAGENT = 'plexapp.com v9.0'
subtitleExt = ['utf','utf8','utf-8','sub','srt','smi','rt','ssa','aqt','jss','ass','idx']

#langPrefs2Podnapisi = {'sq':'29','ar':'12','be':'50','bs':'10','bg':'33','ca':'53','zh':'17','cs':'7','da':'24','nl':'23','en':'2','et':'20','fi':'31','fr':'8','de':'5','el':'16','he':'22','hi':'42','hu':'15','is':'6','id':'54','it':'9','ja':'11','ko':'4','lv':'21','lt':'19','mk':'35','ms':'55','no':'3','pl':'26','pt':'32','ro':'13','ru':'27','sr':'36','sk':'37','sl':'1','es':'28','sv':'25','th':'44','tr':'30','uk':'46','vi':'51','hr':'38'}
# langPrefs2Legendas = {'por':'1'}
mediaCopies = {}

def Start():
	HTTP.CacheTime = 0
	HTTP.Headers['User-agent'] = OS_PLEX_USERAGENT
	Log("START CALLED")

def ValidatePrefs():
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
	Log("Params: " + string.strip(params['Nome'] + params['Temp'] + params['Epi'] + params['Source'] + params['Grupo']))
	buscaURL = LEGENDAS_SEARCH_PAGE + urllib.quote(string.strip(params['Nome'] + params['Temp'] + params['Epi'] + params['Source'] + params['Grupo']))
	# buscaURL = repr(LEGENDAS_SEARCH_PAGE + urllib.quote(params['Nome'] + " s" + repr(params['Temp']) + "e" + repr(params['Epi']) + " " + params['Grupo']))
	#buscaURL = LEGENDAS_SEARCH_PAGE + params['Nome'] + " s" + params['Temp'] + "e" + params['Epi'] + " " + params['Grupo']
	return simpleSearch(buscaURL, lang)

def movieSearch(params, lang):
	# Log("Params: %s" % urllib.urlencode(params))
	# buscaURL = LEGENDAS_SEARCH_PAGE + urllib.urlencode(params)
	Log("Params: " + params['Nome'] + params['Ano'] + params['Source'] +  params['Grupo'])
	buscaURL = LEGENDAS_SEARCH_PAGE + urllib.quote(params['Nome'] + params['Ano'] + params['Source'] + params['Grupo'])
	return simpleSearch(buscaURL, lang)


#Do a basic search for the filename and return all sub urls found
def simpleSearch(buscaURL, lang = 'por'):
	phantompath = Platform.OS + '/phantomjs'
	if Platform.OS == 'Windows':
		phantompath = phantompath + '.exe'
	Log("buscaURL: %s" % buscaURL)
	subUrls = []
	#Log("RelPath: " + os.path.realpath(__FILE__))
	# elem = HTML.ElementFromURL(buscaURL)
	# snarf = []
	# snarf.append("C:/Users/BrutuZ/AppData/Local/Plex Media Server/Plug-in Support/Data/com.plexapp.agents.legendastv/templeg.rar")
	# Log("Path?: " + os.path.normcase(os.path.normpath(os.path.join(os.path.splitunc(os.getcwd())[1], '../../../Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath))))
	# Log("Rel?: " + os.path.relpath(os.path.normpath('/Users/BrutuZ/AppData/Local/Plex Media Server/Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath), os.path.splitunc(os.getcwd())[1]))
	# return snarf

# def foobar():
	Log("PhantomJS in: " + os.path.realpath(os.getcwd() + '/../../../Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath))
	browser = selenium.webdriver.PhantomJS(os.path.normcase('../../../Plug-ins/LegendasTV.bundle/contents/Libraries/Shared/selenium/webdriver/phantomjs/' + phantompath))
	# wait for the page to load
	try:
		browser.get(str(buscaURL))
		WebDriverWait(browser, 300).until(lambda x: x.find_element_by_id('resultado_busca'))
	except:
		Log("BROWSER TIMED OUT. Site may be experiencing some problems")
		return subUrls
	finally:
		# store it to string variable
		page_source = browser.page_source
	browser.quit()
	# Log(page_source)

	elem = HTML.ElementFromString(page_source)
	# Log("HTML: %s" % elem)
	# subpages = elem.xpath("//div[@class='gallery clearfix list_element']/article/div/div/p[1]/a/@href")
	subpages = elem.xpath("//div[@class='f_left']/p[1]/a/@href")
	Log("Subpages: %s" % subpages)
	for subpage in subpages:
		subPageUrl = LEGENDAS_MAIN_PAGE + subpage
		Log("Subpage: %s" % subPageUrl)
		#pageElem = HTML.ElementFromURL(subPageUrl)
		#downloadUrl = getDownloadUrlFromPage(pageElem)
		downloadUrl = subPageUrl.replace("download","downloadarquivo")
		#Log("DownloadURL: %s" % downloadUrl)
		subUrls.append(downloadUrl)

	return subUrls

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

	#subUrls = doSearch(data, lang, isTvShow)

	d = dict(data) # make a copy so that we still include release group for other searches
	#if not subUrls:
	Log("Searching for filename")
	d['Temp'] = ''
	d['Epi'] = ''
	d['Source'] = ''
	d['Grupo'] = ''
	d['Nome'] = string.split(d['Filename'].lower(),os.sep)[-1][:-4]
	subUrls = doSearch(d, lang, isTvShow)
	if not subUrls and d['Nome'] != d['Nome'].translate(None,"'\"!?:"):
		Log("%d subs found - Stripping special characters: " % len(subUrls))
		d['Nome'] = d['Nome'].translate(None,"'\"!?:")
		subUrls = doSearch(d, lang, isTvShow)
	if not subUrls:
		Log("%d subs found - Replacing dots with spaces: " % len(subUrls))
		d['Nome'] = d['Nome'].replace('.',' ')
		subUrls = doSearch(d, lang, isTvShow)
	d = dict(data) # make a copy so that we still include release group for other searches
	if isTvShow and not subUrls and d['Temp'] == 's00':
		Log("Special episode, removing s##e## and hoping for the best")
		d['Temp'] = ''
		d['Epi'] = ''
		subUrls = doSearch(d, lang, isTvShow)
		if not subUrls:
			Log("We need to go deeper")
			d['Temp'] = ''
			d['Epi'] = ''
			d['Source'] = ''
			d['Grupo'] = ''
			d['Nome'] = string.split(data['Filename'].lower(),os.sep)[-1][:-4]
			subUrls = doSearch(d, lang, isTvShow)
	d = dict(data) # make a copy so that we still include release group for other searches
	#subUrls = doSearch(data, lang, isTvShow)
	if not subUrls and d['Nome'] != d['Nome'].translate(None,"'\"!?:"):
		Log("%d subs found - Stripping special characters: " % len(subUrls))
		d['Nome'] = d['Nome'].translate(None,"'\"!?:")
		subUrls = doSearch(d, lang, isTvShow)
	if not subUrls and '.' in d['Nome']:
		Log("%d subs found - Replacing dots with spaces: " % len(subUrls))
		d['Nome'] = d['Nome'].replace('.',' ')
		subUrls = doSearch(d, lang, isTvShow)
	if not subUrls and isTvShow:
		Log("%d subs found - Spacing Season Episode" % len(subUrls))
		d['Temp'] = d['Temp'] + ' '
		subUrls = doSearch(d, lang, isTvShow)
	if not subUrls:
		Log("%d subs found - Removing release group" % len(subUrls))
		# del d['Grupo']
		d['Grupo'] = ''
		subUrls = doSearch(d, lang, isTvShow)
	if not subUrls and not isTvShow:
		Log("%d subs found - Removing Year" % len(subUrls))
		d['Ano'] = ''
		subUrls = doSearch(d, lang, isTvShow)
	if d['Source'] and not subUrls:
		Log("%d subs found - Removing source type" % len(subUrls))
		d['Source'] = ''
		subUrls = doSearch(d, lang, isTvShow)

	return subUrls

def getSubsForPart(data, isTvShow=True):
	siList = []
	# for lang in getLangList():
		#Log("Lang: %s,%s" % (lang, langPrefs2Legendas[lang]))
		# data['Lang'] = langPrefs2Legendas[lang]
	data['Lang'] = "por"
	lang = data['Lang']

	subUrls = searchSubs(data, isTvShow)
	if not subUrls:
		Log("No subtitles found =(")
	else:
		for subUrl in subUrls:
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
			try:
				archurl = urllib.urlopen(subUrl).geturl()
				Log("Getting subtitle from: %s" % archurl)
				#legExt = string.split(urllib.urlopen(subUrl).info()['Content-Disposition'],'.')[-1].strip('"')
				legExt = string.split(archurl,'.')[-1].strip("'")
				if legExt == "rar":
					urllib.urlretrieve(subUrl, 'templeg.rar')
					archive = rarfile.RarFile('templeg.rar')
					subArchive = archive.infolist()
				elif legExt == "zip":
					subArchive = Archive.ZipFromURL(subUrl)
					archive = subArchive
				else:
					Log('Unkown file format: %s' % subExt)
			except:
				Log("Error downloading subtitle")
				continue
			#Data.Save("LegRar.rar", Leg)
			# archive.write(rarfile.RarFile,"LegRar.rar")
			match = 5
			for parseA in subArchive:
				if legExt == "rar":
					nameA = str(parseA.filename)
				elif legExt == "zip":
					nameA = str(parseA)
				#Log('Archive:' + legExt + '\n' + string.split(data['Filename'].lower(),os.sep)[-1] + ' | Filename \n' + nameA.lower() + ' | subtitle')
				if string.split(data['Filename'].lower(),os.sep)[-1][:-4] == nameA.lower()[:-4]:
					Log('Perfect match! \n' + string.split(data['Filename'],os.sep)[-1] + ' | Filename \n' + nameA + ' | subtitle')
					subArchive = [parseA]
					match = 1
					break
				if data['Grupo'].lower() in nameA.lower():
					Log('Decent match! \n' + string.split(data['Filename'],os.sep)[-1] + ' | Filename \n' + nameA + ' | subtitle')
					subArchive = [parseA]
					match = 2
					continue
				if data['Nome'].lower() in nameA.lower() and data['Temp'].lower() in nameA.lower() and data['Epi'].lower() in nameA.lower() and data['Source'].lower() in nameA.lower():
					Log('"Meh" match! \n' + string.split(data['Filename'],os.sep)[-1] + ' | Filename \n' + nameA + ' | subtitle')
					if match > 2:
						subArchive = [parseA]
					match = 3
					continue
				else:
					Log('Nothing matches - disregarding \n' + string.split(data['Filename'],os.sep)[-1] + ' | Filename \n' + nameA + ' | subtitle')
					match = 4
					continue

			#Log("subArchive: " + str(subArchive))
			for parse in subArchive:
				if legExt == "rar":
					name = str(parse.filename)
				elif legExt == "zip":
					name = str(parse)

				Log("Name in pack: %s" % name)
				if name in ['Legendas.tv.url','Legendas.tv.txt','Créditos.txt']:
					Log("Ignoring link")
					continue
				if os.sep in name or 'MACOSX' in name:
					Log("Ignoring folder")
					continue
				#legFile = tempfile.NamedTemporaryFile(suffix='.srt', prefix=name, delete=False)

				if legExt == "rar":
					legFile = archive.extract(name)
					Log("Temp: " + legFile)
					#archive.extract(name)
					legZip = zipfile.ZipFile('templeg.zip', 'w')
					legZip.write(name)
					# if os.sep in name:
						# name = string.split(name,os.sep)[-1]
						# Log("Removing folder from filename: %s" % name)
					subData = legZip.read(name)
					legZip.close()
					# Data.Save("LegFile", archive.extract(name))
					#archive.extract(name, Data.SaveObject("LegFile"))
					#subData = open(name)
					# subData = Data.Load("LegFile")
					# subData.write(archive.extract(name))
					#subData = legFile.file
				elif legExt == "zip":
					subData = archive[name]
				Log(repr(subData))
				subReg = subUrl + '.' + legExt + '/leg=' + name
				si = SubInfo(lang, subReg, subData, name)
				# si = SubInfo(lang, subUrl, subData, name)
				#Log(repr(si))
				siList.insert(0,si)
				# siList.append(si)
				# Data.Remove("LegFile")
				#legFile.close()
				if legExt == "rar":
					os.unlink(name)
					os.unlink('templeg.zip')

			if legExt == "rar":
				os.unlink('templeg.rar')
			# Data.Remove("downRar")
	return siList

def getReleaseGroup(filename):
	# tmpFile = string.replace(filename, '-', '.')
	tranTab = string.maketrans('[-]','.. ')
	# if tmpFile != filename:
		# tmpFile = string.strip(']').replace(filename, '[', '.')
	tmpFile = filename.translate(tranTab)
	if ".." in tmpFile:
		tmpFile = tmpFile.replace("..",".")
	splitName = string.split(tmpFile, '.')
	# splitName = string.split(splitFileName[-1], '.')
	group = splitName[-2].strip()
	# Log("Filename: %s \r\n tmpFile: %s \r\n splitName: %s \r\n Group: %s" % (repr(filename),repr(tmpFile),repr(splitName),repr(group)))
	return group

def getVideoSource(filename):
	sources = ['HDTV','WEB-DL','WEBDL','WEB DL','WEBRIP','Web-Rip','Web Rip','DVD','BDR','BDRip','BRRip','Blu-Ray','BluRay']
	vsource = ''
	for source in sources:
		if source.lower() in filename.lower():
			vsource = source
	return vsource

class LegendasTVAgentMovies(Agent.Movies):
	name = 'Legendas.tv'
	languages = [Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.imdb']

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
				Log("Title: %s" % media.title)
				Log("Filename: %s" % part.file)
				Log("Year: %s" % mc.year)
				Log("Release group %s" % getReleaseGroup(part.file))

				data = {}
				data['Nome'] = str(media.title).replace(' ','.')
				data['Grupo'] = " " + getReleaseGroup(part.file)
				data['Ano'] = " " + str(mc.year)
				data['Filename'] = part.file
				data['Source'] = " " + getVideoSource(part.file)

				siList = getSubsForPart(data, False)

				if siList:
					for si in siList:
						part.subtitles[Locale.Language.Match(si.lang)][si.url] = Proxy.Media(si.sub, ext=si.ext, format=si.ext) 

		del(mediaCopies[metadata.id])


class LegendasTVAgentTvShows(Agent.TV_Shows):
	name = 'Legendas.tv'
	languages = [Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.thetvdb']

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
						data['Nome'] = str(media.title + ' ').replace(' ','.')
						data['Temp'] = "s" + str(season).rjust(2,str("0"))
						data['Epi'] = "e" + str(episode).rjust(2,str("0"))
						data['Source'] = " " + getVideoSource(part.file)
						data['Grupo'] = " " + getReleaseGroup(part.file)
						data['Filename'] = part.file
						Log("Show: %s" % data['Nome'])
						Log("Season: %s, Ep: %s" % (data['Temp'], data['Epi']))
						Log("Video Source: %s" % data['Source'])
						Log("Release Group: %s" % data['Grupo'])

						siList = getSubsForPart(data)

						if siList:
							for si in siList:
								part.subtitles[Locale.Language.Match(si.lang)][si.url] = Proxy.Media(si.sub, ext=si.ext, format=si.ext) 

