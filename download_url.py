import re
import requests
from bs4 import BeautifulSoup


def getHtml(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    try:
        response = requests.get(url,timeout=40,headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        import traceback
        traceback.print_exc()


def DownLoadPaper(url,papername):
    try:
        soup = BeautifulSoup(getHtml(str(url[:-1])), 'html.parser')
        result = soup.body.find_all('iframe')
        downloadUrl = result[-1].attrs['src'].split('?')[0]
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
        response = requests.get(downloadUrl, timeout=80, headers=headers)

        with open(papername,'ab+') as f:
            print('Start download file: ', papername, '\n')
            f.write(response.content)
    except:
        import traceback
        with open('errorLog','ab+') as f:
            traceback.print_exc(file=f)


    
with open("url.txt", "r") as f:   
    baseUrl = 'http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='      
    print('Beginning!')
    n=1
    line = f.readline()
    while line:
       if n == 1:
          rule = r'"(.*?)"'
          slotList=re.findall(rule, line)
       if n == 2:
          num=(line[-8:])
          newUrl = baseUrl+str(num)
          #print(newUrl)
          papername=slotList[0][:-1]+'_'+str(num)
          rstr = r"[\=\(\)\,\/\\\:\*\?\？\"\<\>\|\'']"
          papername=re.sub(rstr, '', papername)
          papername=papername[:-1]+'.pdf'
          print('Number: ', line[-8:])
          DownLoadPaper(newUrl,papername)
       line = f.readline()
       n=n+1
       if len(line)<5:
          n=0
    print('All End')

      
      
    

