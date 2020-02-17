# made by Koo Minku
# CJU Library ChatBot
# class and library file : cjubot_library

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse   import quote # for URL 한글 인코딩

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
    
# 도서 총 리스트 검색 / 무엇으로 검색 / 도서 이름/ 전체출력여부 (전체출력 print_all ==100)
def bookListSearch(searchBy, name, print_all): 
    #URL 앞쪽
    url_listFront = "https://library.cju.ac.kr/search/tot/result?pn="
    #키워드로 검색
    keyword_end = "&folder_id=null&q="+quote(name)+"&st=KWRD&si=TOTAL"
    #전체일치 검색
    allSame_end = "&folder_id=null&q="+quote(name)+"&st=EXCT&si=TOTAL"
    # 1페이지부터 시작 
    pageNumber = 1

    # URL 조합 / 앞쪽 + 페이지번호 + 무엇으로 검색
    if searchBy == '1':
        URL_end = keyword_end
    else:
        URL_end = allSame_end
    
    url = url_listFront+ str(pageNumber) + URL_end
    repeat =1  # 출력 횟수 
    bookList = bookListCount(url) # 도서 검색 총 개수
    
    #전체출력의 경우
    if print_all == 100:
        repeat = int(bookList/10)+1
        if bookList%10 == 0: # 10의 배수일 경우
            repeat -=1
    
    # 검색된 책 목록 출력
    for i in range(repeat):
        #URL 갱신
        url = url_listFront +str(pageNumber) +URL_end
        pageNumber +=1 #page 번호 추가
        info = bookListInfo(url) #페이지 당 도서 정보 딕셔너리
        for p in info: #10개씩 출력
            print(info[p][0]+'\n'+info[p][2]) #제목 / 출판사
            print(info[p][1]+"\n") #저자
    #  총 검색 도서 개수 / URL를 리스트로 반환
    return [bookList, url_listFront +'1'+URL_end]
    
# 책 선택하고 책 상세정보 출력 
def bookDetailSearch(code):
    #책 상세정보 URL 앞쪽
    url_bookDetail_front = "https://library.cju.ac.kr/search/detail/"
    url = url_bookDetail_front+code #URL 조합
    #도서 선택에서 인덱스 에러 경우
    if code =='err':
        return 0
    
    getHTML = urlopen(url)
    bs = BeautifulSoup(getHTML, "html.parser")
    
    bookHead = bs.find("div", {"class": "profileHeader"}) #제목+저자
    bookTitle = bookHead.find("h3").get_text() #제목
    bookAuthor = bookHead.find("p").get_text() #저자
    bookMakerList = bs.findAll("th", {"scope": "row"}) #도서정보 종합 리스트
    bookMaker = "정보 없음" #출판사 정보 없을 경우
    for book in bookMakerList:
        if book.get_text() == "발행사항": #출판사 정보 있을 경우
            bookMaker = book.next_sibling.get_text().split(",")[0].split(": ")[-1]
            break
            
    bookLocation = bs.find("td", {"class": "callNum"}).get_text() #도서관에서 도서 위치
    bookRental = bs.find("span", {"class": "status available"}).get_text() #대출가능여부
    
    bookDetail = [bookTitle, bookAuthor, \
                bookMaker, bookLocation, bookRental]
    print(bookDetail)
    return bookDetail
    
    
    