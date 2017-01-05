#!/usr/bin/python2.7
'''
abuscript.py
Version 1.10.14
Require: Python2.7 and lower version
It support all platforms(Linux, Windows, Mac)
Usage: python abuscript.py https://2ch.hk/b/res/143636089.html | Easy way
Usage: python abuscript.py -b e <-- 'boards' | To download full board
Usage: python abuscript.py https://2ch.hk/b/res/143636089.html -w || -p || -g  | To download only webm|picture|gifs
May be in future GUI version

WARNING: Will downloaded to the directory with abuscript
'''

import argparse
import os
import re
import urllib2
import time
import json
from sys import argv
# Copyright

abuscript_version = '1.10.14'
Cookie = 'usercode_auth=35f8469792fdfbf797bbdf48bab4a3ad'

def get_all_threads(board):
    """
    Get all threads in board
    use static Cookie
    Using json
    """
    try:
    	opener = urllib2.build_opener()
    	opener.addheaders.append(("Cookie", Cookie))
    	catalog = opener.open("https://2ch.hk/" + board + "/catalog.json").read()
    	threads = json.loads(catalog)
    	threads_url = []
    	for num in threads["threads"]:
        	threads_url.append("https://2ch.hk/" + board + "/res/" + num["num"] + ".html")
    	return threads_url

    except urllib2.HTTPError:
    	print ' Board not found \n Check it'
    	exit()

def download_board(board):
    '''
    Geting all thread in board
    and download
    '''
    threads = get_all_threads(board)
    for item in threads:
        download_thread(item)

def isExist(name_file):
    '''
    Function verify files exist
    '''
    if os.path.isfile(name_file):
        return True
    else:
        return False

def download_file(url, dirname):
    '''
    Download files
    with use urllib2
    '''
    opener = urllib2.build_opener()
    opener.addheaders.append(("Cookie", Cookie))
    data = opener.open(url)
    with open(dirname + "/" + url.split("/")[-1], "wb") as out:
        out.write(data.read())

def get_pattern():
    '''
    Filter input arguments
    '''
    pattern = "(?:"
    if args.webm_switch:
        pattern += "webm|"
    if args.picture_switch:
        pattern += "png|jpg|"
    if args.gif_switch:
        pattern += "gif|"
    if pattern != "(?:":
        pattern = pattern[:-1] + ")"
    else:
        pattern = "(?:webm|png|jpg|gif)"
    return pattern

def download_thread(url):
    '''
    Create folder and download threads
    '''
    try:
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie", Cookie))
        thread = opener.open(url)
        #Make folder name
        #Spit boards
        folder_name = url.split("/")[-1][:-5]
    	board = url.split("/")[3]
    	pattern = get_pattern()

        thread_media = re.findall(r'href="(/' + board + '/src/[^"]*' + pattern + ")", \
        thread.read().decode('utf-8'))
        thread_media = fix_array(thread_media)
        if not os.path.isdir(folder_name):
        #Verify exist folder
        	os.makedirs(folder_name)
        	print"Create folder " + folder_name
    	else:
        	print"Searching"

        for i, item in enumerate(thread_media):
            filename = item.split("/")[-1]
            media_url = "https://2ch.hk" + item
            if isExist(folder_name + "/" + filename):
                continue
            print "Downloading " + filename + " (" + str(i + 1) + " of " + \
            str(len(thread_media)) + ")"
            download_file(media_url, folder_name)
        #auto update every 10 iterations
        if not args.board_name:
            time.sleep(10)
            print 'To the out, Press Ctrl + C'
            download_thread(url)
    except urllib2.URLError:
        print' Thread not found \n Check link'
        exit()
    except KeyboardInterrupt:
        print'Stoped'
        exit()
    except Exception, e:
        print'Excetion: ' + e

def fix_array(array):
#Checking for dublicat
   	return list(set(array))

def __ARGS__():
    ar = argparse.ArgumentParser(
    	description=" \n",
    	usage="python abuscript.py [link] [args]",
    	version="version {}".format(abuscript_version),
    	epilog="Easy-to-Use download webm's, pictures or gifs \n \
    	Files will downloaded in dir with script \n \
    	after full downloading,\
     	will monitoring for new files ")
    ar.add_argument('link',nargs="?", metavar='link',type=str,help="Thread link")
    ar.add_argument("-w","--webm",action="store_true",dest='webm_switch',default=False,help="Only webm's")
    ar.add_argument("-p","--picture",action="store_true",dest='picture_switch',default=False,help="Only pictures")
    ar.add_argument("-g","--gif",action="store_true",dest='gif_switch',default=False,help="Only gifs")
    ar.add_argument('-b','--board',metavar="board",dest='board_name',default=0,help='Download all threads from board \n \
    Example abuscript -b e')
    ar.add_argument('--cookie',metavar='Cookie',dest='Cookie',default=Cookie,help='set Cookie, \
    if dont work hidden boards')

    global args
    args = ar.parse_args()
    options = vars(args)
    link = options['link']
    board = args.board_name
    #If no arguments print help
    if board == 0 and not link:
    	ar.print_help()
    	exit()

    if board:
        download_board(board)
    else:
        download_thread(link)

if __name__ == '__main__':
   __ARGS__()
