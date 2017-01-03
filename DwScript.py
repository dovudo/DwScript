import argparse
import urllib2
import os
import re
import urllib
def grub(link,dest,directory):
    pattern = "(?:"

    URL = urllib2.urlopen(link)
    args=dest.parse_args()
    print("Created directory " + directory)
    try:
        #Filtering args
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

        # TODO Write board downloader

        #create directory
        if not os.path.isdir(directory):
            os.makedirs(directory)

        #Main download script
        threads_array = re.findall(r'href="([^"]*' + pattern + ")", URL.read().decode('utf-8'))
        for i, m in enumerate(threads_array):
            if i % 2 == 0:
                continue
            print("Downloading " + m.split("/")[4] + " (" + str(i / 2 + 1) + " of " + str(len(threads_array) / 2) + ")")
            #urllib.urlretrieve('https://2ch.hk/' + m)
            data = urllib2.urlopen("https://2ch.hk" + m)
            with open(directory + "/" + m.split("/")[4], "wb") as out:
                out.write(data.read())

    except urllib2.HTTPError:
        print("Thread not found")
        sys.exit()

    except KeyboardInterrupt:
        print("Break stoped")
        exit()
    except Exception, e:
        print(e)
        sys.exit()

if __name__ == '__main__':
    ar = argparse.ArgumentParser("python abuscript.py https://2ch.hk/b/res/123405664.html",epilog="Easy-to-Use download webm's, pictures or gifs \n Files will downloaded in dir with abuscript")
    ar.add_argument('--version',action='version', version='version 1.0')
    ar.add_argument('link', metavar='link',type=str,help="Thread link")
    ar.add_argument("-w","--webm",action="store_true",dest='webm_switch',default=False,help="Only webm's")
    ar.add_argument("-p","--picture",action="store_true",dest='picture_switch',default=False,help="Only pictures")
    ar.add_argument("-g","--gif",action="store_true",dest='gif_switch',default=False,help="Only gifs")
    ar.add_argument("-a",'--all',action="store_true", dest='all_switch',default=True,help="Download all files (Default)")
    ar.add_argument('-b','--board',action='store_true',dest='board_switch',default=False,help='Download all threads from board \n Example abuscript -b e')
    ar.add_argument('-t','--thread',action='store_true',dest='thread_switch',default=False,help='Download by number, only with -b (--board)')
    result = ar.parse_args()
    options = vars(result)
    link = options['link'] #parse link
    #dir_name = re.split(r'[https://2ch.hk/b/res/.html]+',link)
    #dir_name =dir_name[1]
    dir_name = link.split("/")[-1][:-5]
   #dir_name = link.strip('https://2ch.hk/b/res/.html')
    grub(link,ar,dir_name)
