import argparse
import os
import re
import urllib2
import time
import json
# Copyright
#Function verify files exist

def get_all_threads(board):
    catalog = urllib2.urlopen("https://2ch.hk/" + board + "/catalog.json").read()
    threads = json.loads(catalog)
    threads_url = []
    for num in threads["threads"]:
        threads_url.append("https://2ch.hk/" + board + "/res/" + num["num"] + ".html")
    return threads_url

def download_board(board):
    threads = get_all_threads(board)
    for item in threads:
        download_thread(item)

def isExist(name_file):
    if os.path.isfile(name_file):
        return True
    else:
        return False

def download_file(url, dirname):
    data = urllib2.urlopen(url)
    with open(dirname + "/" + url.split("/")[-1], "wb") as out:
        out.write(data.read())

def get_pattern():
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
    folder = url.split("/")[-1][:-5]
    pattern = get_pattern()
    if not os.path.isdir(folder):
        os.makedirs(folder)
        print "Create folder " + folder
    else:
        print "Thread sleep updating"
    thread = urllib2.urlopen(url)
    thread_media = re.findall(r'href="([^"]*' + pattern + ")", thread.read().decode('utf-8'))
    thread_media = fix_array(thread_media)
    for i, item in enumerate(thread_media):
        filename = item.split("/")[-1]
        media_url = "https://2ch.hk" + item
        if isExist(folder + "/" + filename):
            continue
        print "Downloading " + filename + " (" + str(i + 1) + " of " + str(len(thread_media)) + ")"
        download_file(media_url, folder)

    #auto update in iteration
    if not args.board_switch:
        time.sleep(10)
        print 'To the out, Press Ctrl + C'
        download_thread(url)

def fix_array(array):
    for i, item in enumerate(array):
        if i % 2 == 0:
            del array[i]
    return array

if __name__ == '__main__':
    ar = argparse.ArgumentParser("python abuscript.py https://2ch.hk/b/res/123405664.html",epilog="Easy-to-Use download webm's, pictures or gifs \n Files will downloaded in dir with abuscript")
    ar.add_argument('--version',action='version', version='version 1.0')
    ar.add_argument('link', metavar='link',type=str,help="Thread link")
    ar.add_argument("-w","--webm",action="store_true",dest='webm_switch',default=False,help="Only webm's")
    ar.add_argument("-p","--picture",action="store_true",dest='picture_switch',default=False,help="Only pictures")
    ar.add_argument("-g","--gif",action="store_true",dest='gif_switch',default=False,help="Only gifs")
    ar.add_argument("-a",'--all',action="store_true", dest='all_switch',default=True,help="Download all files (Default)")
    ar.add_argument('-b','--board',metavar="board",dest='board_switch',default="0",help='Download all threads from board \n Example abuscript -b e')
    ar.add_argument('-t','--thread',action='store_true',dest='thread_switch',default=False,help='Download by number, only with -b (--board)')
    global args
    args = ar.parse_args()
    options = vars(args)
    link = options['link']
    board = args.board_switch
    if board:
        download_board(board)
    else:
        download_thread(link)
