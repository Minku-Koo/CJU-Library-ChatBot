# made by Koo Minku
# CJU Library ChatBot
# class and library file : cjubot_library

from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == "__main__":
    print("This is main")

# 검색한 개수 출력
def bookListCount(url):
    #print(url)
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    page = bs.find("p", {"class": "searchCnt"})
    # 순수 페이지 숫자만 추출
    count = page.get_text().replace("\n", "").split(' ')[1][:-1]
    #총 검색 도서 개수 int로 반환
    return int(count)

# 페이지 당 책  정보 출력
def bookListInfo(url):
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    #제목 전부 추출
    title_all = bs.findAll("dd", {"class": "title"})
    
    # 책 정보 태그 추출 - 여기서 작가, 출판사 정보 빼내옴
    book = bs.findAll("li", {"class": "items"})
    bookDict, num={}, 1
    
    for i in book:
        book_one = i.dl.findAll("dd", {"class", "info"})
        bookDict[num] = [title_all[num-1].a.get_text(), \
                        book_one[0].get_text(), book_one[1].get_text()]
        num+=1
    # 딕셔너리 : (제목 작가 출판사)를 리스트 value로 저장
    return bookDict
    
# 도서 상세정보 위한 책 코드 반환 / 최초 검색은 num == 100 아닌경우는 num == 검색도서번호
def bookCode(url, num):
    if num == 100:
        print("몇 번째 도서를 선택하시겠습니까?")
        num = int( input(" >>> ") )
    
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    book = bs.findAll("li", {"class": "items"})
    #도서 고유 코드를 반환
    try:
        return str(book[num-1]).split("item_")[1][:18]
    except(IndexError):
        print('잘못된 입력입니다.')
        return 'err'
    
    
    
    
    