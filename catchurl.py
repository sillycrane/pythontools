# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import getopt,sys
import lxml
import urllib

def print_help():
    print("\tusage:catchurl.py -k <keywords> -d <down> -u <up> -o <filename>")
    print("\tusage:catchurl.py --key <keywords> --down <down> --up <up> --outfile <filename>")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:d:u:o:", ["key=", "num=","down=","up=","outfile="])
    except getopt.GetoptError:
        print_help()
        sys.exit()
    for opt,arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ('-k','--key'):
            key = arg
        elif opt in ('-o','--outfile'):
            outfile = arg
        elif opt in ('-d', '--down'):
            down = arg
        elif opt in ('-u', '--up'):
            up = arg
    print("---start---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    file=open(outfile,"w+")
    all=[]
    for page in range(int(down),int(up),10):
        #intitle:Powered By DedeCMS_V57
        inurl="https://www.baidu.com/s?wd="+key+"&pn="+str(page)
        res = requests.get(url = inurl,headers=headers)
        print("[*]"+res.url)
        soup = BeautifulSoup(res.content,'lxml')
        tagh3 = soup.find_all('h3')
        for h3 in tagh3:
            href = h3.find('a').get('href')
            baidu_url = requests.get(url=href, headers=headers, allow_redirects=False, timeout=3)
            real_url = baidu_url.headers['Location']
            if real_url.startswith('http'):
                pro,url=urllib.splittype(real_url)
                host,rest=urllib.splithost(url)
                final=pro+"://"+host
                if final not in all:
                    all.append(final)
                    print(' [+]' + final)
                    file.write(final+'\n')

if __name__=='__main__':
    main(sys.argv[1:])
    print("---end---")