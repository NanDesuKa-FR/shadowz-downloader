# -*- coding: utf-8 -*-

import os
import io
from colorama import Fore, Back, Style
import re
import cloudscraper
import subprocess
from sys import platform
import json
import sys
from clint.textui import progress

def Logo():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('clear')
    elif platform == "win32":
        os.system('cls')
        
    print()
    print(Fore.RED + "                             ██████  ██░ ██  ▄▄▄      ▓█████▄  ▒█████   █     █░▒███████▒")
    print(Fore.RED + "                           ▒██    ▒ ▓██░ ██▒▒████▄    ▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░▒ ▒ ▒ ▄▀░")
    print(Fore.RED + "                           ░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒██░  ██▒▒█░ █ ░█ ░ ▒ ▄▀▒░ ")
    print(Fore.RED + "                             ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░░█░ █ ░█   ▄▀▒   ░")
    print(Fore.RED + "                           ▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░ ████▓▒░░░██▒██▓ ▒███████▒")
    print(Fore.RED + "                           ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒  ░▒▒ ▓░▒░▒")
    print(Fore.RED + "                           ░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░  ░░▒ ▒ ░ ▒")
    print(Fore.RED + "                           ░  ░  ░   ░  ░░ ░  ░   ▒    ░ ░  ░ ░ ░ ░ ▒    ░   ░  ░ ░ ░ ░ ░")
    print(Fore.RED + "                                 ░   ░  ░  ░      ░  ░   ░        ░ ░      ░      ░ ░    ")
    print(Fore.RED + "                                                       ░                        ░        ")
    print(Fore.RED + "                                                                            By NanDesuKa?")

def menu():
    print("\n\n  Make a choice:\n  ------------------------------------\n  1) Download with link\n  2) exit\n  ------------------------------------")
    
def clean_text(name):
	return name.replace('|', ' ').replace('>', ' ').replace('<', ' ').replace('"', ' ').replace('?', ' ').replace('?',' ').replace('*', ' ').replace(':', ' ').replace('/', ' ').replace('\\', ' ')

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400
    
def Downloader(link):
    scraper = cloudscraper.create_scraper()
    content = scraper.get(link, headers={'Cache-Control': 'no-cache'}).text
    title = clean_text((content.split('<meta property="og:title"content="')[1]).split('" />')[0])
    
    ID_FOR_JSON = (content.split('data-vuid="')[1]).split('"')[0]
            
    JSON = scraper.get("https://www.shadowz.fr/api/player-data/json/" + ID_FOR_JSON, headers={'Cache-Control': 'no-cache'}).text
    data = json.loads(JSON)
    mp4 = (data["data"]["mp4"]).replace(" ", "%20")
    hls = (data["data"]["hls"]).replace(" ", "%20")
    
    print("\n\n  Make a choice:\n  ------------------------------------\n  1) Download MP4\n  2) Download M3U8\n  ------------------------------------")
    
    loop = True
    while loop == True:
        reponse = input("  Choose 1 or 2: ")
        if reponse in ['1', '2']:
            Logo()
            print()
            if reponse == "1":
                r = scraper.get(mp4, headers={'Cache-Control': 'no-cache'}, stream=True)
                with open(title + '.mp4', 'wb') as f:
                    total_length = int(r.headers.get('content-length'))
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
                loop = False
            elif reponse == "2":
                commandvostfr = 'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "{url_m3u8}" -c copy -bsf:a aac_adtstoasc -y "{outputName}"'.format(outputName=title + ".mp4", url_m3u8=hls)
                subprocess.call(commandvostfr, shell=True)
                loop = False

    if JSON.find('"subtitles":[') != -1:
        subtitle_url = (((((JSON.split('"subtitles":[')[1]).split('],"')[0]).split('"url":"')[1]).split('",')[0]).replace("\\/", "/")).replace(" ", "%20")
        ass = scraper.get(subtitle_url, headers={'Cache-Control': 'no-cache'}).text
        txt_to_ass = io.open(title + ".vtt", mode="w", encoding="utf-8")
        txt_to_ass.write(str(ass))
        txt_to_ass.close()
        
    sys.exit("Download complete.")
        
    
def DownloadByLink():
    Logo()
    loop = True
    while loop == True:
        link = input("\n\n  Enter link: ")
        try:
            check = re.match(r'(https?://www\.shadowz.fr/content/.+-[\d*]{1,10})', link)[0]
        except:
            console = False
            
        if link:
            loop = False
            Downloader(link)
        else:
            Logo()
            DownloadByLink()
            
if __name__ == "__main__":
    Logo()
    menu()
    loop = True
    while loop == True:
        reponse = input("  Choose 1 or 2: ")
        if reponse in ['1', '2']:
            Logo()
            loop = False
            if reponse == "1":
                DownloadByLink()
            elif reponse == "2":
                sys.exit("Close by User.")
        else:
            Logo()
            menu()