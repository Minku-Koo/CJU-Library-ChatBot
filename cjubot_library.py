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
    try:
        count = page.get_text().replace("\n", "").split(' ')[1][:-1]
    except(AttributeError):
        print('none type')
        count = 0
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
   #if num == 100:
        #print("몇 번째 도서를 선택하시겠습니까?")
        #num = int( input(" >>> ") )
        #@@@@@@@@@@@@@@
        #이거도 GUI에서 입력받기 
    
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
    
    #GUI 출력 위한 리스트 객체
    gui_list, oneBook = [], []
    # 검색된 책 목록 출력
    for i in range(repeat):
        #URL 갱신
        url = url_listFront +str(pageNumber) +URL_end
        pageNumber +=1 #page 번호 추가
        info = bookListInfo(url) #페이지 당 도서 정보 딕셔너리
        for p in info: #10개씩 출력
            print(info[p][0]+'\n'+info[p][2]) #제목 / 출판사
            print(info[p][1]+"\n") #저자
            gui_list.append(info[p])
    #  총 검색 도서 개수 / URL를 리스트로 반환
    return [bookList, url_listFront +'1'+URL_end, gui_list]
    
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
    try:
        bookTitle = bookHead.find("h3").get_text() #제목
    except(AttributeError):
        print('none type')
        bookTitle = '정보 없음'
    
    try:
        bookAuthor = bookHead.find("p").get_text() #저자
    except(AttributeError):
        print('none type')
        bookAuthor = '정보 없음'
    
        
    bookMakerList = bs.findAll("th", {"scope": "row"}) #도서정보 종합 리스트
    bookMaker = "정보 없음" #출판사 정보 없을 경우
    for book in bookMakerList:
        if book.get_text() == "발행사항": #출판사 정보 있을 경우
            bookMaker = book.next_sibling.get_text().split(",")[0].split(": ")[-1]
            break
    
    try:
        bookLocation = bs.find("td", {"class": "callNum"}).get_text() #도서관에서 도서 위치
    except(AttributeError):
        print('none type')
        bookLocation = '정보 없음'
    
    try:
        bookRental = bs.find("span", {"class": "status available"}).get_text() #대출가능여부
    except(AttributeError):
        print('none type')
        bookRental = '정보 없음'
        
        
    
    bookDetail = [bookTitle, bookAuthor, \
                bookMaker, bookLocation, bookRental]
    print(bookDetail)
    return bookDetail
    
    
#자연어 분석한 결과 입력하면  함수 이름 텍스트로 반환
def chatAnalysis( where):
    print('analasis start')
    if where[-1] == '_': #시설
        return infra_func(where)
    else: #연구학습지원
        return studyHelp_func(where)
    
#시설 안내 텍스트 함수
def infra_func(name):
    if name=='referenceRoom_':
        print('referenceRoom_')
        txt1 = "제1~3자료실 : 3~5층/n09시~20시(학기중 평일) 18시(방학중 평일) 23시(시험기간중 평일)"
        txt2 ="\n제 1자료실 : 총류(000), 철학(100), 종교(200), 사회과학(300)"
        txt3 ="\n제 2자료실 : 자연과학(400), 기술과학(500), 예술(600), 어학(700), 역사(900)"
        txt4 ="\n제 3자료실 : 문학(800)"
        return [txt1+ txt2+ txt3+ txt4, 80]
        
    elif name=='readingRoom_':
        print('readingRoom_')
        txt1 = """도서관 내 열람실은 재학 중인 학생들의 학업의 용도로 사용할 수 있습니다.
중앙도서관·열람실(일반, 노트북, 대학원열람실)은 좌석발급기 및 모바일 좌석관리를 이용하여 좌석을 발급하여 이용할 수 있습니다."""
        txt2 ="""\n제1~3열람실 : 1층 / 820석 / 연중무휴 24시간 순환개방
대학원열람실 : 2층 / 40석 / 06시~00시\n"""
        txt3 = """\n<배정>\nMobile : 청주대학교 중앙도서관 App → 로그인 → 열람좌석 에서 배정 및 가배정
좌석 발급기 : 원하는 좌석 클릭 → 학생증 또는 모바일 이용증 인증 → 배정 확인
1회 이용시간 : 6시간 (시험기간중엔 4시간으로 변경)\n좌석배정 후 퇴실 미반납 3회 누석시 2일간 자리배정불가"""
        txt4 = """\n<퇴실>\nMobile : 청주대학교 중앙도서관 App → 메인 화면에서 배정취소 버튼 클릭 → 퇴실 확인
좌석 발급기 : 퇴실 버튼 클릭 → 학생증 또는 모바일 이용증 인증 → 퇴실 확인"""
        return [txt1+ txt2+ txt3+ txt4, 150]
        
    elif name=='studyRoom_':
        print('studyRoom_')
        txt1 = """학생들의 학습형태에 맞는 다양한 형태의 실을 제공하며, 그룹스터디, 회의, 발표 등의 용도로 사용할 수 있으며.
각 실별 LED 모니터를 설치하여 멀티미디어를 통한 자유로운 협업공간으로 재학중인 학부/대학원생만 이용 가능합니다."""
        txt2 = """\n총 12개 스터디룸 / 48인치 모니터 보유 /
2층 : 1~8호 / 스터디룸 당 6~ 12명 인원 수용 / 09시 ~ 00시
3~4층 : 9~12호 / 6~8명 수용 / 09시~기간별로 시간 상이"""
        txt3 = """\n학생들의 학습형태에 맞는 다양한 형태의 실을 제공하며, 그룹스터디, 회의, 발표 등의 용도로 사용할 수 있으며.
각 실별 LED 모니터를 설치하여 멀티미디어를 통한 자유로운 협업공간으로 재학중인 학부/대학원생만 이용 가능합니다."""
        txt4 = """\n<예약>\nPC : 도서관 홈페이지 → 도서관시설 → 로그인 → 그룹스터디룸
Mobile : 청주대학교 중앙도서관 App → 로그인 → 그룹스터디룸
예약은 이용하려는 날 7일 전부터 당일까지 가능
예약 후, 이용하려는 날 예약 해당시간부터 20분 이내에\n 해당 그룹스터디룸 인증기에 학생증 또는 모바일 이용증으로 인증 후 사용
이용시간은 2시간이며, 2회연장이용가능(1회 연장시 1시간)"""
        return [txt1+ txt2+ txt3+ txt4, 230]
        
    elif name=='copyPrint_':
        print('copyPrint_')
        txt1 = "출력/복사/스캔/FAX/PC 이용 가능한 일체형 네트워크시스템"
        txt2 = "\n1층 복사실 : 유인복사 3대(칼라1대, 흑백2대) / 09시~18시, 방학중 휴실"
        txt3 = """\n정보검색라운지 : 무인, 4대(칼라1대, 흑백3대), 연중 06시~24시
3~4층 자료실: 무인, 층별 각 1대, 09시~기간별 종료시간 상이"""
        return [txt1+ txt2+ txt3, 140]
        
    elif name=='notebookRoom_':
        print('notebookRoom_')
        txt1 = "노트북열람실은 좌석발급기 및 모바일 좌석관리를 이용하여 좌석을 발급하여 이용할 수 있습니다."
        txt2 = "\n1층 복사실 : 유인복사 3대(칼라1대, 흑백2대) / 09시~18시, 방학중 휴실"
        txt3 = """\n정보검색라운지 : 무인, 4대(칼라1대, 흑백3대), 연중 06시~24시
3~4층 자료실: 무인, 층별 각 1대, 09시~기간별 종료시간 상이"""
        return [txt1+ txt2+ txt3, 140]
        
    elif name=='multimedia_':
        print('multimedia_')
        txt1 = "멀티미디어 자료의 대출 및 열람을 지원하는 공간으로 영상, 음악 감상을 할 수 있는 독립적인 공간 확보"
        txt2 = "\n2층 / 1인용 32석, 2인용 9실, 3인용 5실 / 09시~20시(학기) 18시(방학)"
        txt3 = """\n<배정>\n좌석발급기에서 원하는 좌석 클릭 → 학생증 및 모바일 이용증 인증 → 확인
1회 이용시간 : 3시간
<예약>\n만실시 좌석배정기 또는 중앙도서관 App에서 멀티미디어실 버튼 클릭 후 예약 버튼 클릭
→ 좌석 배정 Push Message 수신 → Push Message에 안내된 좌석에서 이용
<퇴실>\n좌석발급기에서 퇴실 버튼 클릭 → 학생증 및 모바일 이용증 인증 → 퇴실 확인"""
        return [txt1+ txt2+ txt3, 180]
        
    elif name=='infoRounge_':
        print('infoRounge_')
        txt1 = "디지털인프라를 기반으로 정보검색과 문서작성 서비스를 제공하는 공간"
        txt2 = "\n1층 / 164석 / 09시~00시"
        txt3 = """\n<배정>\n정보검색라운지내 빈좌석PC에서 로그인 후 이용
이용시간은 2시간이며, 1회 연장이용 가능
<예약>\n만실시 정보검색라운지 앞의 Kiosk 또는 청주대학교 중앙도서관 App에서 멀티미디어실 버튼 클릭 후 
예약 버튼 클릭 → 좌석 배정 Push Message 수신 → Push Message에 안내된 좌석에서 
학생증 또는 모바일 이용증 인증 / 도서관 비밀번호 입력 후 이용
20분 이내에 로그인 안했을 시 예약이 자동 취소됩니다."""
        return [txt1+ txt2+ txt3, 180]
        
    elif name=='monileApp_':
        print('monileApp_')
        txt1 = """스마트폰을 이용하여 모바일이용증을 발급받은 후
도서관 출입, 좌석배정, 그룹스터디룸 인증 및 도서 대출 등에 사용할 수 있습니다.\n"""
        txt2 = '''초기 비밀번호는 2012년까지 등록 이용자는 "주민등록번호 뒤 7자리",
2013년 등록 이용자부터는 "주민등록번호 앞 6자리"\n'''
        txt3 = """<발급방법>\n스마트폰의 Play 스토어(안드로이드폰), App Store(아이폰)에서
‘청주대학교 중앙도서관’으로 검색한 후 ‘청주대학교 중앙도서관’앱을 설치하여 사용합니다.\n"""
        txt4 = """<발급 취소>\n청주대학교 클리커 홈페이지로 접속하여 로그인한 후,
[App 등록관리] 메뉴에서 [중지신청] 버튼을 눌러 취소할 수 있습니다.
앱을 통해 일일 1회 취소가능하며 2회 시, 관리자에게 문의하여 취소하시기 바랍니다."""
        return [txt1+ txt2+ txt3+ txt4, 150]
        
    else : #selfReturn_
        print('selfReturn_')
        txt1 = "1회에 최대 3권 대출 및 반납 가능\n딸림자료는 1층 이용자서비스센터에서 대출 및 반납"
        txt2 = "\n자가대출반납기에서는 본책만 대출가능"
        txt3 = """\n3~4층 남,북쪽 : 09시 ~ 20시(학기중), 23시(시험기간), 18시(방학) / 대출+반납
5층 남쪽 : 3~4층과 시간 동일 / 대출+반납
1층 로비 : 연중 24시간 / 반납"""
        return [txt1+ txt2+ txt3, 140]
        
#연구학습지원 텍스트 출력 함수
def studyHelp_func(name):
    if name=='paperGo':
        print('paperGo')
        return ['paperGo',20]
        
    elif name=='loanChange':
        print('loanChange')
        return ['loanChange',20]
        
    elif name=='bookCopy':
        print('bookCopy')
        return ['bookCopy',20]
        
    elif name=='keris_loan':
        print('keris_loan')
        return ['keris_loan',20]
        
    elif name=='cheongjuUniv_loan':
        print('cheongjuUniv_loan')
        return ['cheongjuUniv_loan',20]
        
    elif name=='booknarae':
        print('booknarae')
        return ['booknarae',20]

