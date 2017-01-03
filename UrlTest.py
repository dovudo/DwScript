import urllib2
import re
if __name__ == '__main__':
    url_link = "https://2ch.hk/b/res/143545998.html"
    try:
        URL = urllib2.urlopen(url_link)
       #soup = re.findall(r'.jpg',URL.read().decode("utf-8"))
        for m in re.findall(r'href="([^"]*(?:webm|png|jpg|gif))', URL.read().decode('utf-8')):
            print(m)
        #print(soup)
    except urllib2.HTTPError:
        print("Thread not found")
        exit()
