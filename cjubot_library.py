# made by Koo Minku
# CJU Library ChatBot
# class and library file : cjubot_library

from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("This is main")

# 검색한 개수 출력
def bookCount(url):
    print(url)
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    page = bs.find("p", {"class": "searchCnt"})
    # 순수 페이지 숫자만 추출
    count = page.get_text().replace("\n", "").split(' ')[1][:-1]
    return int(count)
'''
# 페이지 당 책 이름 출력
def bookTitle(url):
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    title_all = bs.findAll("dd", {"class": "title"})
    for title in title_all:
        print(title.a.get_text())
        
    return 0
'''
# 페이지 당 책  정보 출력
def bookInfo(url):
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    #제목 전부 추출
    title_all = bs.findAll("dd", {"class": "title"})
    
    # 책 정보 태그 추출 - 여기서 작가, 출판사 정보 빼내옴
    book = bs.findAll("li", {"class": "items"})
    bookDict, num={}, 1
    """
    for i in book:
        #작가 추출해서 리스트에 추가
        bookAuthor.append(i.dl.find("dd", {"class", "info"}))
        #출판사 추출해서 리스트에 추가
        bookMaker.append(i.dl.findAll("dd", {"class", "info"})[1])
        
        
    # 한 페이지에 10개 정보 있음. 딕셔너리에 제목 작가 출판사 정보 담음
    for r in range(10):
        bookDict[num] = [title_all[r].a.get_text(), \
                        bookAuthor[r].get_text(), bookMaker[r].get_text()]
        num+=1
    """
    for i in book:
        book_one = i.dl.findAll("dd", {"class", "info"})
        bookDict[num] = [title_all[num-1].a.get_text(), \
                        book_one[0].get_text(), book_one[1].get_text()]
        num+=1
    
    return bookDict
    
    