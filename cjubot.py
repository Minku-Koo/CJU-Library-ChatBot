# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot

from urllib.request import urlopen
from urllib.parse   import quote # for URL 한글 인코딩
from bs4 import BeautifulSoup
from cjubot_library import bookCount,  bookInfo

#name = input(" >>> ")
name = "이외수"
# 1페이지부터 시작 
pageNumber = 1

#URL 앞쪽
url_front = "https://library.cju.ac.kr/search/tot/result?pn="
#키워드로 검색
keyword_end = "&folder_id=null&q="+quote(name)+"&st=EXCT&si=TOTAL"
#전체일치 검색
allSame_end = "&folder_id=null&q="+quote(name)+"&st=KWRD&si=TOTAL"
# URL 조합 / 앞쪽 + 페이지번호 + 무엇으로 검색
url = url_front+ str(pageNumber) + keyword_end

print(bookCount(url))
'''
getHTML = urlopen(url)
bs = BeautifulSoup(getHTML, "html.parser")

#작가 추출하기
bookAuthor = bs.findAll("li", {"class": "items"})
for i in bookAuthor:
    auth =  i.dl.find("dd", {"class", "info"})
    print(auth)
'''

for i in range(2):
    #URL 갱신
    url = url_front +str(pageNumber) +keyword_end
    pageNumber +=1 #page 번호 추가
    #bookTitle(url)
    info = bookInfo(url)
    for p in info:
        print(info[p][0])
        print(info[p][2])
        print(info[p][1]+"\n")