# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot

from urllib.request import urlopen
from urllib.parse   import quote # for URL 한글 인코딩
from bs4 import BeautifulSoup
from cjubot_library import *

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
    

#도서 검색 메인 / 최초 검색 시도 시 name == ''
def bookSearch(name):
    if name=='': #최초 검색일 경우
        print("검색 내용을 입력하세요.")
        name = input(" >>> ")
    
    print("어떤 방법으로 검색하시겠습니까?")
    print("1. 키워드 검색\n2. 완전일치 검색")
    searchBy = input(" >>> ")
    #잘못된 입력 경우 - 다시 시도
    if searchBy != '1' and searchBy != '2':
        bookSearch('')
    #도서 검색 리스트 결과 받음
    bookListResult = bookListSearch(searchBy, name, 0)
    # 검색 도서가 10개 미만일 경우 -- 바로 도서 선택
    if 10 >= bookListResult[0] and bookListResult[0] >0:
        print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
        code = bookCode(bookListResult[1], 100)
        bookDetailSearch(code)
    # 도서 검색 결과가 없는 경우 - 다시 진행
    elif bookListResult[0]==0:
        bookSearch('')
        
    else: #검색 결과 10개 이상일 경우
        print("총 "+str(bookListResult[0])+"건의 도서가 검색되었습니다.")
        print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
        print("0번은 전체 출력\n다시 검색하실 수 있습니다.")
        
        num = input(" >>> ")
        
        if num.isdigit(): # 도서 선택 or 전체 출력
            if num == '0': #전체 출력
                bookListSearch(num, name, 100)
            else: #도서 선택
                code = bookCode(bookListResult[1], int(num))
                bookDetailSearch(code)
        else: #도서 재검색
            bookSearch(num)
            

bookSearch('')


    
