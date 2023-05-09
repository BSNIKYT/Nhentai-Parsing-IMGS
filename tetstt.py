import os
import requests
try:
  from bs4 import BeautifulSoup as bs
except:
  os.system('pip install BeautifulSoup4')
import pandas as pd
import urllib
import os
import shutil
from time import sleep

import sys
import json
from urllib.request import HTTPError
import urllib.request
from time import sleep
import http
import random
from datetime import datetime, timedelta

from requests.exceptions import ConnectionError  #, HTTPSConnectionPool
# from requests.packages.urllib3.exceptions import MaxRetryError
# from requests.packages.urllib3.exceptions import ProxyError as urllib3_ProxyError

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"

prt = f'''{'='*15}- Connection statuses -{'='*15}
{green}- 200 - Success!{white}
{'='*10} HTTP ERROR CODEs: {'='*10}
{red}- 400 - The script was unable to parse the URL.
- 401 - Authorization is needed ... you need to download it manually.
- 402 - Similar to 401, access after payment.
- 403 - Site/Browser/Anti-Virus denied you access to access this URL (perhaps VPN).
- 404 - Not found, or this is an outdated link.
{white}{'='*10} TIMEOUT ERROR CODEs: {'='*10}
{red}- 522 - The connection is not responding (maybe ILV blocked).
- 524 - TCP connection failed. (internal OS errors).
- 526 - Certificate blocking (rather different times, or parental control)
{white}{'='*10} OTHER: {'='*10}
{violet}- 101 - You are disconnected from the Internet.
- 102 - Error processing URL.{white}'''

if str(os.name) == "nt":
  dir_pref = "\\"
else:
  dir_pref = "/"


class InputURLError(Exception):

  def __init__(self, *args):
    if args:
      self.message = args[0]
    else:
      self.message = None

  def __str__(self):
    #print('calling str')
    if self.message:
      return f'InputURLError, {self.message}'
    else:
      return 'InputURLError has been raised'



class RequestError(Exception):

  def __init__(self, *args):
    if args:
      self.message = args[0]
    else:
      self.message = None

  def __str__(self):
    #print('calling str')
    if self.message:
      return f'RequestError, {self.message} '
    else:
      return 'RequestError has been raised'


#url_server = (url.split('/')[2]).split('.')[1]

print(prt)



def download_function(url, name_file):


    url = url.replace(" ", "%20")

    if "?size=" in url:
        ind = url.find("?size=")
    else:
        if "?extra=" in url:
            ind = url.find("?extra=")
        else:
            ind = len(url)

    try:
        urllib.request.urlretrieve(str(url), name_file)
        print(f"{green}[+] 200: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except HTTPError as err_code:print(f"{red}[-] {red}{err_code.code}: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except urllib.error.URLError as err_code:
        if "[WinError 10054]" in str(err_code):print(f"{red}[-] {red}522: {blue}{name_file}{white}  URL: {url[0:ind]}")
        if "[Errno 99]" in str(err_code):print(f"{red}[-] {red}524: {blue}{name_file}{white}  URL: {url[0:ind]}")
        if "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):print(f"{red}[-] {red}526: {blue}{name_file}{white}  URL: {url[0:ind]}")
        if "[Errno 11001]" in str(err_code):print(f"{red}[-] {red}000: {blue}{name_file}{white}  URL: {url[0:ind]}")
        else:print(f"{violet}[?] ___: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except http.client.RemoteDisconnected:
        print(f"{violet}[-] {violet}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except ConnectionResetError:
        print(f"{violet}[-] {violet}101: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except ValueError:
        print(f"{violet}[?] 102: {blue}{name_file}{white}  URL: {url[0:ind]}")
    except Exception as err:
        print(f"{violet}[?] ___: {blue}{name_file}{white}  URL: {url[0:ind]}")

     





def main(url):

  print('\n')
  try:
    name_dir = (url.split('/'))[4]
  except:
    if 'https://nhentai.' not in url:
      print(f'Ссылка {url}  не содержит https://nhentai.[SERVER] .')
      sleep(10)
      raise InputURLError(
        f'https://nhentai.[SERVER] not found in url( {url} ).')

  try:
    os.mkdir(name_dir)
    print(f'[!] Создана папка {name_dir}')
  except FileExistsError:
    print(f'[!] Есть папка {name_dir}')
    pass
  except PermissionError:
    name_dir = ""
    pass

  do = os.getcwd()
  posle = os.getcwd() + dir_pref + name_dir
  os.chdir(posle)
  print(do, ' --> ',posle)

  def find_url_html(url_one):
    try:
      r = requests.get(url_one)
      soup = bs(r.text, "html.parser")

      imgs = soup.find_all('img')
      url_two = ''

      for img in imgs:
        if "https:" in img.get('src'):
          print(f'FIND: {img.get("src")}')
          url_two = img.get('src')
      return url_two
    except:
      print(f'Произошла ошибка с {url}.')

  url_download = []

  try:
    r = requests.get(url)
    if r.status_code == 403:print(f"{red}[-] {red}403: {url}") 
    else:print(f'RequestStatus - {r.status_code}')
  except HTTPError as err_code:print(f"{red}[-] {red}{err_code.code}: {url}")
  except urllib.error.URLError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    else:status_code = '___'
    print(f"{red}[-] {red}{status_code}: {url}")
  except http.client.RemoteDisconnected:
    print(f"{violet}[-] {violet}101: {url}")
  except ConnectionResetError:
    print(f"{violet}[-] {violet}101: {url}")
  except ValueError as err:
    print(f"{violet}[?] 102: {url}")
  except requests.exceptions.SSLError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    else:status_code = '___'
    print(f"{red}[-] {red}{status_code}: {url}")
  except requests.exceptions.ConnectionError as err_code:
    if "[WinError 10054]" in str(err_code):status_code = 522
    elif "[Errno 99]" in str(err_code):status_code = 524
    elif "[SSL: WRONG_VERSION_NUMBER]" in str(err_code):status_code = 526
    else:status_code = '___'
    print(f"{red}[-] {red}{status_code}: {url}")
  except Exception as err:
    print(f"{violet}[?] ___: Exception: {err} | URL:{url}")

    
    
  
  soup = bs(r.text, "html.parser")
  title = str(soup.find_all('h1')).replace('<h1>',
                                             '').replace('</h1>', '').replace(
                                               '[', '').replace(']', '')
  url_server = (url.split('/')[2]).split('.')[1]

  print(title)
  print(f'SERVER: {url_server}')
  
  for name in soup.find_all('a', class_='gallerythumb'):
      url_download.append(find_url_html(f'https://nhentai.{url_server}{name.get("href")}'))

  print(f'Working Directory: {os.getcwd()}')
  i = 0
  for url in url_download:
    i+= 1
    if "mp4" in url:exten = f".mp4"
    else:
        if "gif" in url:exten = f".gif"
        else:
          if "jpg" in url:exten = f".jpg"
          else:
            if "webp" in url:exten = f".webp"
            else:
              if "webm" in url:exten = f".webm"
              else:exten = f".png"

    download_function(url, f'{i}{exten}')

  
  print(white)
  os.chdir(do)


main('https://nhentai.to/g/348217')
