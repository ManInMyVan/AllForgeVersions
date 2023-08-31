import time
start_time = time.time()
import requests
from bs4 import BeautifulSoup
print('Getting supported versions...')
versions=[]
links=[]
files=0
urls=[]
page = BeautifulSoup(requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/').content, "html.parser").find_all("a")
for link in page:
	if link.get('href') and link.get('href').endswith('html') and link.get('href').startswith('index'):
		urls.append('https://files.minecraftforge.net/net/minecraftforge/forge/'+link.get('href'))
	if link.get('href') and link.get('href').endswith('html') and link.get('href').startswith('index'):
		versions.append(link.get('href').replace('.html', '').replace('index_', ''))
page = BeautifulSoup(requests.get(urls[0]).content, "html.parser").find_all("a")
#	Get the latest version, since the selected one is not a link
for link in page:
	if link.get('href') and link.get('href').endswith('html') and link.get('href').startswith('index'):
		urls.append('https://files.minecraftforge.net/net/minecraftforge/forge/'+link.get('href'))
	if link.get('href') and link.get('href').endswith('html') and link.get('href').startswith('index'):
		versions.append(link.get('href').replace('.html', '').replace('index_', ''))
#	Deduplicate the lists
versions = list(dict.fromkeys(versions))
versions.insert(0, versions.pop())
urls = list(dict.fromkeys(urls))
urls.insert(0, urls.pop())
versions_time=time.time()
print('Versions (%d): %s\nDone, took %.3f seconds.\nGetting download links... (This may take a while.)' % (len(versions),str(versions).removeprefix('[').removesuffix(']').replace("'",''),versions_time-start_time))
for url in urls:
	page = BeautifulSoup(requests.get(url).content, "html.parser").find_all("a")
	for link in page:
		if link.get('href') and link.get('href').endswith('.jar'):
			links.append(link.get('href'))
print('Found %d links in %.3f seconds.' % (len(links), time.time()-versions_time))
DoDownload=input('Would you like to download the files? y/n\n')
if DoDownload == 'y':
	while True:
		directory=input('Please specify a directory to download to.\n')
		try:
			open(directory+'\\'+links[0].split('/')[7], 'wb')
		except FileNotFoundError:
			print('That directory is not valid, please try again.')
		else:
			print('Downloading files...')
			download_time=time.time()
			break
	for link in links:
			download=requests.get(link, allow_redirects=True)
			open(directory+'\\'+link.split('/')[7], 'wb').write(download.content)
			files+=1
	print('Downloaded %d files in %.3f seconds.' % (files, time.time()-download_time))
	print('Proccess finished in %.3f seconds.' % time.time()-start_time)