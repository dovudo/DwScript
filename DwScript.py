#!/usr/bin/python3
'''
DwScript.py

It support all platforms(Linux, Windows, Mac)
Usage: python DwScript.py https://2ch.hk/b/res/143636089.html | Easy way
Usage: python DwScript.py -b e <-- 'boards' | To download full board
Usage: python DwScript.py https://2ch.hk/b/res/143636089.html -w || -p || -g  | To download only webm|picture|gifs
May be in future GUI version

WARNING: Will downloaded to the directory with DwScript
'''

import argparse
import os
import re
import urllib.request
import time
import json
from sys import argv

Cookie = 'usercode_auth=35f8469792fdfbf797bbdf48bab4a3ad'

# Create opener, an useful object to retrive files
global opener
opener = urllib.request.build_opener()
opener.addheaders.append(("Cookie", Cookie))

def get_all_threads(board):
    """
    Get all threads in board
    use static Cookie
    Using json
    """
    try:
        catalog = opener.open("https://2ch.hk/" + board + "/catalog.json").read()
        threads = json.loads(catalog)
        threads_url = []
        for num in threads["threads"]:
            threads_url.append("https://2ch.hk/" + board + "/res/" + num["num"] + ".html")
        return threads_url

    except urllib.request.HTTPError:
        print ("Board not found \n Check it")
        exit()

def download_board(board):
    '''
    Geting all thread in board
    and download
    '''
    threads = get_all_threads(board)
    for item in threads:
        download_thread(item)

def download_file(url, dirname):
    '''
    Download files
    with use urllib.request
    '''
    data = opener.open(url)
    filename = url.split("/")[-1]
    try:
        with open(dirname + "/" + filename, "wb") as out:
            out.write(data.read())
    except:
        os.remove(dirname + "/" + filename)
        print("aborted by site")
        download_file(url,dirname)

def get_pattern():
    '''
    Filter input arguments
    '''
    pattern = "(?:"
    if args.webm_switch:
        pattern += "webm|mp4|"
    if args.picture_switch:
        pattern += "png|jpg|"
    if args.gif_switch:
        pattern += "gif|"
    if pattern != "(?:":
        pattern = pattern[:-1] + ")"
    else:
        pattern = "(?:webm|mp4|png|jpg|gif)"
    return pattern

def download_thread(url, file):
    '''
    Create folder and download threads
    '''
    try:
        if file:
            thread = open(file, "r")
        else:
            thread = opener.open(url)
        '''
        Make folder name
        Spit boards
        '''
        folder_name = url.split("/")[-1][:-5]
        board = url.split("/")[3]
        pattern = get_pattern()

        if file:
            thread_media = list(set(re.findall(r'href="(/' + board + '/src/[^"]*' + pattern + ")", \
            thread.read())))
        else:
            thread_media = list(set(re.findall(r'href="(/' + board + '/src/[^"]*' + pattern + ")", \
            thread.read().decode('utf-8'))))

        if not os.path.isdir(folder_name): # Check folder existance
            os.makedirs(folder_name)
            print ("Create folder " + folder_name)
        else:
            print ("Searching")

        for i, item in enumerate(thread_media):
            filename = item.split("/")[-1]
            media_url = "https://2ch.hk" + item
            if os.path.isfile(folder_name + "/" + filename):
                continue
            print ("Downloading " + filename + " (" + str(i + 1) + " of " + str(len(thread_media)) + ")")
            download_file(media_url, folder_name)

        # Realod thread after 30 seconds (if no board mode)
        if not args.board_name:
            print ("I'm sleeping at 30 sec \nPress Ctrl + C, to exit")
            time.sleep(30)
            download_thread(url)

    except urllib.request.URLError:
        print ("Thread not found \n Check link")
        exit()

    except KeyboardInterrupt:
        print ("Stoped")
        exit()

    except Exception:
        print ("Exception: {}, if you find any problems, please send the report to https://github.com/dovudo/DwScript/issues" + Exception)

# Entrypoint args
def __ARGS__():
    ar = argparse.ArgumentParser(
        description=" Easy-to-Use downloader webm's, mp4, pictures or gifs from 2ch.hk",
        usage="python DwScript.py [link] [args]",
        epilog="Files will downloaded in dir with script")
    ar.add_argument('link',nargs="?", metavar='link',type=str,help="Thread link")
    ar.add_argument("-w","--webm",action="store_true",dest='webm_switch',help="Only webms and mp4")
    ar.add_argument("-p","--picture",action="store_true",dest='picture_switch',help="Only pictures")
    ar.add_argument("-g","--gif",action="store_true",dest='gif_switch',help="Only gifs")
    ar.add_argument('-b','--board',metavar="board",dest='board_name',help='Download all threads from board \n \
    Example DwScript -b e')
    ar.add_argument('-f','--file',metavar="file",dest="file_name",help='Source code file')
    ar.add_argument('--cookie',metavar='Cookie',dest='Cookie',default=Cookie,help='set Cookie, \
    if dont work hidden boards')

    global args
    args = ar.parse_args()
    options = vars(args)
    link = options['link']
    board = args.board_name
    file = args.file_name
    #If no arguments print help
    if not board and not link:
        ar.print_help()
        exit()

    if board:
        download_board(board)
    else:
        download_thread(link, file)

if __name__ == '__main__':
   __ARGS__()
