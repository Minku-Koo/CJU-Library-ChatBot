# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot
# developer E-mail : corleone@kakao.com

from urllib.request import urlopen
#from urllib.parse   import quote # for URL 한글 인코딩
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont,QPalette
from cjubot_library import *
from PyQt5.QtCore import QDate, Qt ,QSize# QT 날짜 모듈

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.centerHeight = 650
        self.widgetHeight = 50 #스타팅 메시지 기본 50
        self.lb_style = lb_styles
        self.initUI()
        
    #스크롤 조정
    def scrollSetting(self, size):
        self.widgetHeight+=size
        if self.widgetHeight >= 650: #스크롤바 늘려주기
            self.centerHeight+=size
            self.lb_center.setFixedHeight(self.centerHeight)
        
    #도서 검색 메인 / 최초 검색 시도 시 name == '' 
    def bookSearch(self, name):
        #CMD에서만 활용할 경우
        '''
        #CMD에서만 활용할 경우
        if name=='': #최초 검색일 경우
            print("검색 내용을 입력하세요.")
            name = input(" >>> ")
        
        print("어떤 방법으로 검색하시겠습니까?")
        print("1. 키워드 검색\n2. 완전일치 검색")
        searchBy = input(" >>> ")
        #잘못된 입력 경우 - 다시 시도
        if searchBy != '1' and searchBy != '2':
            bookSearch('')
        '''
        bookstartText = QLabel('어떤 방법으로 검색하시겠습니까?') # 텍스트 합쳐서 입력
        bookstartText.setFont(QFont('굴림',9))
        bookstartText.setStyleSheet(self.lb_style)
        
        self.keyword_btn = QPushButton("키워드 검색", self) #버튼 객체 추가
        self.keyword_btn.clicked.connect(self.keyword_btn_click)
        
        self.allsame_btn = QPushButton("완전일치 검색", self) #버튼 객체 추가
        self.allsame_btn.clicked.connect(self.allsame_btn_click)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        
        bookstartLayout = QHBoxLayout()
        bookstartLayout.addWidget(self.keyword_btn)
        bookstartLayout.addWidget(self.allsame_btn)
        bookstartLayout.addWidget(self.start_btn)
        self.scrollSetting(50)
        
        centerLayout.addLayout(bookstartLayout)
        
        
    def book(self, n):
        self.searchBy = n
        #도서 검색 리스트 결과 받음
        self.bookListResult = bookListSearch(n, self.bookName, 0)
        # original : bookListResult = bookListSearch(searchBy, name, 0)
        # 검색 도서가 10개 미만일 경우 -- 바로 도서 선택
        if 10 >= self.bookListResult[0] and self.bookListResult[0] >0:
            bookList = self.bookListResult[2]
            for booklist in bookList: #전체출력 
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                bookAll = QLabel(txt) # 텍스트 합쳐서 입력
                bookAll.setFont(QFont('굴림',7))
                bookAll.setStyleSheet(self.lb_style)
                bookAll.setFixedHeight(50)
                centerLayout.addWidget(bookAll)
                self.scrollSetting(50)
            
            print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
            bookText1 = QLabel('출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.') # 텍스트 합쳐서 입력
            bookText1.setFont(QFont('굴림',9))
            bookText1.setStyleSheet(self.lb_style)
            centerLayout.addWidget(bookText1)
            self.scrollSetting(40)
            
            
            #code = bookCode(bookListResult[1], 100)
            #bookDetailSearch(code)
            '''
            self.selectBook = self.inputTextBox.toPlainText()
            self.selectBook.replace(' ','')
            if self.selectBook.isdigit() :
                code = bookCode(bookListResult[1], self.selectBook)
                bookDetailSearch(code)
            else:
                print('숫자아님 ㅅㄱ')
            '''
        # 도서 검색 결과가 없는 경우 - 다시 진행
        elif self.bookListResult[0]==0:
            self.bookSearch('')
            #@@@@@@@@@@@@@@
            #이거말고 검색 결과 없다는 텍스트만 출력
            bookText2 = QLabel('검색 결과가 없습니다.') # 텍스트 합쳐서 입력
            bookText2.setFont(QFont('굴림',9))
            bookText2.setStyleSheet(self.lb_style)
            centerLayout.addWidget(bookText2)
            
        else: #검색 결과 10개 이상일 경우
            print("총 "+str(self.bookListResult[0])+"건의 도서가 검색되었습니다.")
            print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
            print("0번은 전체 출력\n다시 검색하실 수 있습니다.")
            
            bookList = self.bookListResult[2]
            for booklist in bookList: #상위 10개 출력
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                bookAll = QLabel(txt) # 텍스트 합쳐서 입력
                bookAll.setFont(QFont('굴림',7))
                bookAll.setStyleSheet(self.lb_style)
                bookAll.setFixedHeight(50)
                centerLayout.addWidget(bookAll)
                
                self.scrollSetting(50)
            
            bookText3 = QLabel("총 "+str(self.bookListResult[0])+\
                        "건의 도서가 검색되었습니다.") # 텍스트 합쳐서 입력
            bookText3.setFont(QFont('굴림',9))
            bookText3.setStyleSheet(self.lb_style)
            
            bookText4 = QLabel('출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.') # 텍스트 합쳐서 입력
            bookText4.setFont(QFont('굴림',9))
            bookText4.setStyleSheet(self.lb_style)
            
            bookText5 = QLabel('0번은 전체 출력\n다시 검색하실 수 있습니다.') # 텍스트 합쳐서 입력
            bookText5.setFont(QFont('굴림',9))
            bookText5.setStyleSheet(self.lb_style)
            
            centerLayout.addWidget(bookText3)
            centerLayout.addWidget(bookText4)
            centerLayout.addWidget(bookText5)
            #bookAll.setFixedHeight(40)
            self.scrollSetting(40)
            
            
            
            
            #num = input(" >>> ")
            #num ='1'
            #@@@@@@@@@@@@@@
            #도서 번호 입력 or 전체출력 텍스트로 입력받기
            '''
            if num.isdigit(): # 도서 선택 or 전체 출력
                if num == '0': #전체 출력
                    bookListSearch(num, name, 100)
                else: #도서 선택
                    code = bookCode(self.bookListResult[1], int(num))
                    bookDetailSearch(code)
            '''
    def keyword_btn_click(self):
        print('keyword_btn_click')
        self.book('1')
        
    def allsame_btn_click(self):
        print('allsame_btn_click')
        self.book('2')
        
    def bookNum_click(self): #10개 미만 도서 선택
        self.selectBook = self.inputTextBox.toPlainText()
        self.selectBook.replace(' ','').replace('\n','')
        
        if self.selectBook == '0':
            print('this is zero')
            bookList = bookListSearch(self.searchBy, self.bookName, 100)[2]
            for booklist in bookList: #전체출력 
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                bookAll = QLabel(txt) # 텍스트 합쳐서 입력
                bookAll.setFont(QFont('굴림',7))
                bookAll.setStyleSheet(self.lb_style)
                centerLayout.addWidget(bookAll)
                bookAll.setFixedHeight(40)
                self.scrollSetting(40)
                
            
        elif self.selectBook.isdigit() :
            code = bookCode(self.bookListResult[1], int(self.selectBook))
            bookDetail = bookDetailSearch(code)
            
            txt = "제목 : "+str(bookDetail[0]) +"\n저자 : "+str(bookDetail[1]) +\
            "\n출판사 : "+str(bookDetail[2]) +\
            "\n도서 위치 : "+str(bookDetail[3]) +\
            "\n대출 여부 : "+str(bookDetail[4])
            book1 = QLabel(txt) # 텍스트 합쳐서 입력
            book1.setFont(QFont('굴림',9))
            book1.setStyleSheet(self.lb_style)
            book1.setFixedHeight(60)
            centerLayout.addWidget(book1)
            self.scrollSetting(60)
        else:
            print('숫자아님 ㅅㄱ')
        return self.selectBook
    
    def initUI(self): # main user interface 
        self.setWindowTitle('CJU Library ChatBot') #GUI 제목
        self.setWindowIcon(QIcon('mtd_logo.PNG')) #아이콘 설정, 16x16, PNG 파일
        #self.move(600, 300) #화면에서의 위치
        #self.resize(550, 800) #어플의 크기
        self.setFixedSize(550, 800)  #창 크기 고정
        self.center() #위치를 화면 중앙에 배치 
        #self.setGeometry(600, 300, 400, 300) /  move + resize 합친것
        
        #화면 구성/ Layout
        lb_head = QLabel('청주대학교 도서관 챗봇', self) #라벨 텍스트
        lb_head.setAlignment(Qt.AlignCenter)
        lb_head.setMaximumSize(55000,90) #라벨 최대사이즈
        lb_head.setStyleSheet("color : #E0F2F7;" #라벨 꾸미기
                              #"border-style: solid;"
                              #"border-width: 2px;"
                              #"border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #0040FF;"
                            )
        #라벨 폰트 설정 /  ( font / size / bold )  
        lb_head.setFont(QFont('굴림',17, QFont.Bold))
        
        self.lb_center = QLabel()
        #self.lb_center.setFixedSize(550,650)
        
        self.lb_center.setFixedHeight(self.centerHeight)
        #self.lb_center.setMinimumSize(QSize(550, 500))
        #self.lb_center.setMaximumSize(550,660) #라벨 최대사이즈
        self.lb_center.setAlignment(Qt.AlignCenter)
        self.lb_center.setStyleSheet("color : black;" #라벨 꾸미기
                              #"border-style: solid;"
                              #"border-width: 3px;"
                              #"border-color: black;"
                              #"border-radius: 2px;"
                              #"background-color: orange;"
                            )
        
        
        self.lb_bottom = QLabel()
        self.inputTextBox = QTextEdit()
        self.inputTextBox.setAcceptRichText(False)
        self.inputTextBox.setFixedHeight(70) #라벨 최대사이즈
        #self.lb_bottom.addWidget(inputTextBox)
        self.TextInputButton = QPushButton("입력", self) #버튼 객체 추가
        self.TextInputButton.clicked.connect(self.TextInput_click)
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.inputTextBox)
        self.bottomLayout.addWidget(self.TextInputButton)
        
        #chatBox = QVBoxLayout() #수직 박스 레이아웃
        #chatBox.addWidget(lb_head)
        #chatBox.addStretch(1) #빈공간 설정
        #lb_center 라벨에 스크롤 설정
        self.scroll = QScrollArea()
        #QMainWindow().setCentralWidget(self.scroll)
        #self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn) # vertical 스크롤바 항상 on
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) # vertical 스크롤바 필요시 on
        #self.setCentralWidget(self.scroll)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) # horizon 스크롤 항상 off
        self.scroll.setWidget(self.lb_center) # scroll area에 라벨 추가 
        self.scroll.setFixedHeight(650) # 스크롤창 고정 세로 크기 
        self.scroll.setWidgetResizable(True)
        #self.setCentralWidget(self.scroll)
        
        
        
        
        #레이아웃에 라벨 추가
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(lb_head)
        self.mainLayout.addWidget(self.scroll) #라벨 말고 qscrollarea를 입력해야함
        self.mainLayout.addLayout(self.bottomLayout)
        
        #self.mainLayout.addWidget(self.inputTextBox)
        self.mainLayout.setAlignment(Qt.AlignTop)
        
        
        
        print('-=-=')
        self.setLayout(self.mainLayout) #main layout
        #self.layout_1.addWidget(self.lb_head, alignment=Qt.AlignTop)
        
        
        self.show() #화면에 표시
        
    def center(self): #어플을 화면 중심에 위치시키는 함수
        qr = self.frameGeometry() #창의 위치 크기 정보 불러옴
        cp = QDesktopWidget().availableGeometry().center() #화면 가운데 위치 식별
        qr.moveCenter(cp) #화면 중심으로 이동
        self.move(qr.topLeft())
        
    # 텍스트 박스 클릭 함수
    def TextInput_click(self):
        print("hello text")
        print(self.inputTextBox.toPlainText())
        self.userText = self.inputTextBox.toPlainText().replace('\n','')
        lb_user_text = QLabel(self.inputTextBox.toPlainText()) #입력한 텍스트 
        
        lb_user_text.setFont(QFont('굴림',10))
        lb_user_text.setStyleSheet(self.lb_style)
        if self.userText != "":
            centerLayout.addWidget(lb_user_text) #레이아웃에 입력한 텍스트 출력
        
        self.mainText(self.userText)
        self.inputTextBox.clear() # textEdit clear
        
    # 입력받은 텍스트 판별하고 출력해주는 아주 아주 중요한 것
    def mainText(self, text):
        print("text main")
        if text.isdigit() and len(text) <2: # 도서 선택 경우 
            self.bookNum_click()
            return 0
            
        #elif text.isdigit() and text == '0':
            #전체출력
            #return 0
        
        
        self.bookName = text[1:]
        if text[0] == '!': #도서검색
            print('book search')
            print(text[1:])
            self.bookSearch(text[1:])
            return 0
            
        
        useTime_text = ['이용시간', '시간', '몇시', '언제', '열어']
        useInfra_text = ["어떻",  "어떤"]
        way_text = ["어디", '찾아가', '버스', '택시', '가는길', '얼마나', '어떻게']
        study_text = {"논문":"paperGo", '상호대차':"loanChange", '원몬복사':"bookCopy",
                '논문제출':"paperGo", '학위논문':"paperGo", 'keris':"keris_loan",
                'KERIS':"keris_loan",'충북대':"cheongjuUniv_loan", '서원대':"cheongjuUniv_loan",
                '청주교대':"cheongjuUniv_loan",
                 '책나래':"booknarae", '도서복사':"bookCopy",'책복사':"bookCopy"}
        infra_text = {
        '자료실': 'referenceRoom_', '열람실': 'readingRoom_', 
        '스터디룸': 'studyRoom_', '출력': 'copyPrint_', '노트북': 'notebookRoom_', 
        '복사': 'copyPrint_','멀티미디어':'multimedia_', '정보검색':'infoRounge_',
        '모바일':"monileApp_", '대출반납기':'selfReturn_', '반납':"selfReturn_", '자가대출':"selfReturn_",
        '대출반납':"selfReturn_"}
        
        text = text.replace(" ", "").replace('\n','')
        result = ''
        for txt in useTime_text: #이용시간 묻는지 검사
            if txt in text:
                result += 'T-'
                break
                
        for txt in useInfra_text: #시설 묻는지 검사
            if txt in text:
                result += 'F-'
                break
                
        for txt in way_text: #오는길 묻는지 검사
            if txt in text:
                result += 'W-'
                break
        
        #출입 방법 검사 
        if '출입' in text or '입장' in text or '들어가' in text:
            result += 'E-'
        
        for txt in study_text: #연구학습지원 묻는지 검사
            if txt in text:
                result += study_text[txt]+'-'
                break
        
        for txt in infra_text.keys(): #시설 이름 있는지 검사
            if txt in text:
                result += infra_text[txt]+'-'
                break
        print(result)
        #-------------------자연어 검사 끝
        
        resultList = result.split('-') # - 로 끊어서 리스트 입력
        resultList.remove("") # 리스트 내 공백 제거
        print(resultList)
        
        if len(resultList) == 0: #아무것도 알아듣지 못한 경우
            print('cannot read')
        
        # 시설이름/연구학습지원 이름만 있을 경우
        elif  len(resultList[-1]) >1 :  # 이름일 경우
            print_text = chatAnalysis(resultList[-1])
            print(print_text)
            #텍스트 출력
            #for txt in print_text[0]:
            AnalysisText = QLabel(print_text[0]) # 텍스트 합쳐서 입력
            AnalysisText.setFont(QFont('굴림',8))
            AnalysisText.setStyleSheet(self.lb_style)
            AnalysisText.setFixedHeight(print_text[1])
            centerLayout.addWidget(AnalysisText)
            self.scrollSetting(print_text[1])
            
            
        elif len(resultList[0]) ==1: # 시간 또는 시설 alphabet만 있을 경우
            if resultList[0]=='T': #시간 혼자
                self.useTime_click()
            elif 'W' in resultList: # E 가 리스트에 있을 경우 / 출입방법
                self.enter_click()
            elif 'W' in resultList: # W 가 리스트에 있을 경우 / 오시는길 바로 출력
                self.findWay_click()
            else : #시설 혼자
                self.infra_click()
            
        else : #이건 무슨 경우인지 모르겟는경우 
            print('what the fuck??')
            
        
        
    #--------------------------------------------------------------------
    
    #  #  #  #  #  #  #  #  #  #  #  #
    # 이용시간 클릭 이벤트 버튼 #
    #   #  #  #  #  #  #   #  #  #  #
    
    def referenceRoom_click(self): 
        print("제1~3자료실")
        useTimeLabel = QLabel('09시~20시(학기중 평일), 18시(방학중 평일), 23시(시험기간중 평일)') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def studyRoom_click(self): 
        print("스터디룸")
        useTimeLabel = QLabel('2층 1~8호 : 09시~00시\
\n이외 : 09시~20시(학기중), 23시(시험기간), 18시(방학중)') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def notebookRoom_click(self): 
        print("노트북 열람실")
        useTimeLabel = QLabel('1층 복사실 :09시~18시, 방학중 휴실\
\n정보검색라운지 :연중 06시~24시') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def multimedia_click(self): 
        print("멀티미디어 감상실")
        useTimeLabel = QLabel('09시~20시(학기) 18시(방학)') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def readingRoom_click(self): 
        print("제 1~3 열람실")
        useTimeLabel = QLabel('제1~3열람실 : 연중무휴 24시간 순환개방\
\n대학원열람실 : 06시~00시') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def infoRounge_click(self): 
        print("정보검색라운지")
        useTimeLabel = QLabel('09시~00시') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def copyPrint_click(self): 
        print("복사/출력실")
        useTimeLabel = QLabel('1층 복사실 : 09시~18시, 방학중 휴실\n\
정보검색라운지 : 연중 06시~24시\n\
3~4층 자료실: 09시~20시(학기중), 23시(시험기간), 18시(방학중)') # 텍스트 합쳐서 입력
        useTimeLabel.setFont(QFont('굴림',9))
        useTimeLabel.setStyleSheet(self.lb_style)
        self.scrollSetting(30)
        centerLayout.addWidget(useTimeLabel)
        self.useTime_click()
        
    def start_btn_click(self):
        print('처음으로')
        self.startMessage() #최초 출력 함수 
    
    def useTime_click(self): #이용시간 클릭 하면 나타나는 레이아웃
        print("use time button click")
        #이용시간 메뉴 텍스트 설정
        useTimeText1 = QLabel('이용을 원하시는 시설을 클릭해주세요.')
        #useTimeText1.setMaximumSize(330,30)
        
        
        #useTimeText1.setFixedHeight(30)
        #useTimeText1.setFixedSize(300, 30)
        useTimeText1.setFont(QFont('굴림',11))
        useTimeText1.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        centerLayout.addWidget(useTimeText1) #레이아웃에 텍스트 입력
        useTimeLayout = QGridLayout() # 버튼 집합 레이아웃 설정
        
        self.referenceRoom = QPushButton("제 1~3 자료실", self) #버튼 객체 추가
        self.referenceRoom.clicked.connect(self.referenceRoom_click)
        
        self.studyRoom = QPushButton("스터디룸", self) #버튼 객체 추가
        self.studyRoom.clicked.connect(self.studyRoom_click)
        
        self.notebookRoom = QPushButton("노트북 열람실", self) #버튼 객체 추가
        self.notebookRoom.clicked.connect(self.notebookRoom_click)
        
        self.multimedia = QPushButton("멀티미디어 감상실", self) #버튼 객체 추가
        self.multimedia.clicked.connect(self.multimedia_click)
        
        self.readingRoom = QPushButton("제 1~3 열람실", self) #버튼 객체 추가
        self.readingRoom.clicked.connect(self.readingRoom_click)
        
        self.infoRounge = QPushButton("정보검색라운지", self) #버튼 객체 추가
        self.infoRounge.clicked.connect(self.infoRounge_click)
        
        self.copyPrint = QPushButton("복사/출력실", self) #버튼 객체 추가
        self.copyPrint.clicked.connect(self.copyPrint_click)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        
        #그리드 레이아웃에 버튼 위치 배치
        useTimeLayout.addWidget(self.referenceRoom, 0, 0)
        useTimeLayout.addWidget(self.studyRoom, 0, 1)
        useTimeLayout.addWidget(self.notebookRoom, 0, 2)
        useTimeLayout.addWidget(self.multimedia, 0, 3)
        useTimeLayout.addWidget(self.readingRoom, 1, 0)
        useTimeLayout.addWidget(self.infoRounge, 1, 1)
        useTimeLayout.addWidget(self.copyPrint, 1, 2)
        useTimeLayout.addWidget(self.start_btn, 1, 3)
        
        self.scrollSetting(100)
        
        useTimeLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 이용시간 버튼 집합 레이아웃 추가
        centerLayout.addLayout(useTimeLayout)
    
    def findWay_click(self):  #오시는길
        print("findWay_click button click")
        #오시는길 텍스트 설정
        txt1 = '<버스>\n1. 청주고속터미널-시내버스(청주대 방면) 40분\n'
        txt2 = '2. 청주시외버스터미널-시외버스(충주,괴산방면 북청주터미널 경유 버스) 25분\n'
        txt3 = '3. 북청주터미널-청대정문(도보 7분)'
        findWayText1 = QLabel(txt1 + txt2+txt3) # 텍스트 합쳐서 입력
        #findWayText1.setMaximumSize(450,90)
        findWayText1.setFont(QFont('굴림',10))
        findWayText1.setStyleSheet(self.lb_style)
        
        findWayText2 = QLabel('<택시>\n가경동 청주터미널 앞 택시 승강장 이용(약 25분)\n북청주터미널에서 정문까지 7분, 예술대학 10분')
        #findWayText2.setMaximumSize(520,60)
        findWayText2.setFont(QFont('굴림',9))
        findWayText2.setStyleSheet(self.lb_style)
                            
        centerLayout.addWidget(findWayText1) #레이아웃에 텍스트 입력
        centerLayout.addWidget(findWayText2)
        self.scrollSetting(130)
        centerLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 출입안내 버튼 집합 레이아웃 추가
        self.startMessage() #최초 출력 함수 

    #--------------------------------------------------------------------
    
    def enter_click(self):#출입 안내
        print("enter_click button click")
        #이용시간 메뉴 텍스트 설정
        txt1 = '도서관 출입문에 출입통제시스템이 설치되어\n'
        txt2 = '학생증 또는 모바일 이용증이 있어야 출입 할 수 있으니\n도서관에 올 때는 학생증을 지참하여야 합니다.'
        enterText1 = QLabel(txt1 + txt2) # 텍스트 합쳐서 입력
        #enterText1.setMaximumSize(450,100)
        
        #findWayText1.setFixedHeight(100)
        #findWayText1.setFixedSize(450, 100)
        enterText1.setFont(QFont('굴림',10))
        enterText1.setStyleSheet(self.lb_style)
        enterText2 = QLabel('<출입방법>\n입구통제기의 스캐너에 학생증(모바일 이용증) 스캐닝 → 녹색램프 → 입장')
        enterText2.setMaximumSize(520,60)
        #findWayText2.setFixedHeight(60)
        #findWayText2.setFixedSize(520, 60)
        enterText2.setFont(QFont('굴림',9))
        enterText2.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
                            
        centerLayout.addWidget(enterText1) #레이아웃에 텍스트 입력
        centerLayout.addWidget(enterText2)
        self.scrollSetting(150)
        centerLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 출입안내 버튼 집합 레이아웃 추가
        self.startMessage() #최초 출력 함수 
    
    #--------------------------------------------------------------------
    
    def studyHelp_click(self): #연구학습지원 버튼
        print("studyHelp_click button click")
        #시설 안내 메뉴 텍스트 설정
        txt = '원하시는 연구학습 내용을 선택하세요.'
        studyHelpText = QLabel(txt)
        #studyHelpText.setMaximumSize(380,30)
        studyHelpText.setFont(QFont('굴림',10))
        studyHelpText.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        #버튼 집합
        studyHelpLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        
        self.loanChange = QPushButton("상호 대차", self) #버튼 객체 추가
        self.loanChange.clicked.connect(self.loanChange_click)
        
        self.bookCopy = QPushButton("원문 복사", self) #버튼 객체 추가
        self.bookCopy.clicked.connect(self.bookCopy_click)
        
        self.paperGo = QPushButton("학위 논문 제출", self) #버튼 객체 추가
        self.paperGo.clicked.connect(self.paperGo_click)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        
        #레이아웃에 버튼 위치 배치
        studyHelpLayout.addWidget(self.loanChange)
        studyHelpLayout.addWidget(self.bookCopy)
        studyHelpLayout.addWidget(self.paperGo)
        studyHelpLayout.addWidget(self.start_btn)
        
        
        
        self.widgetHeight+=50
        if self.widgetHeight >= 650: #스크롤바 늘려주기
            self.centerHeight+=50
            self.lb_center.setFixedHeight(self.centerHeight)
        centerLayout.addWidget(studyHelpText)
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addLayout(studyHelpLayout)
        
    #  #  #  #  #  #  #  #  #  #  #  #  #
    # 연구학습지원 클릭 이벤트 버튼 #
    #   #  #  #  #  #  #   #  #  #  #  #
    
    def loanChange_click(self): #상호대차 버튼
        print('loanChange_click click')
        txt1 = "상호대차는 우리 도서관에 없는 도서를\n타 도서관에서 대여 신청할 수 있는 서비스입니다."
        txt2 = '\n원하시는 상호대차 방법을 선택하세요'
        loanChangeText = QLabel(txt1+txt2)
        #loanChangeText.setMaximumSize(400,60)
        loanChangeText.setFont(QFont('굴림',10))
        loanChangeText.setStyleSheet(self.lb_style)
        
        #버튼 집합
        loanChangeLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        
        self.keris_loan = QPushButton("KERIS 상호대차", self) #버튼 객체 추가
        self.keris_loan.clicked.connect(self.keris_loan_click)
        
        self.cheongjuUniv_loan = QPushButton("청주권 대학도서관", self) #버튼 객체 추가
        self.cheongjuUniv_loan.clicked.connect(self.cheongjuUniv_loan_click)
        
        self.booknarae_loan = QPushButton("책나래", self) #버튼 객체 추가
        self.booknarae_loan.clicked.connect(self.booknarae_loan_click)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        
        centerLayout.addWidget(loanChangeText)
        loanChangeLayout.addWidget(self.keris_loan)
        loanChangeLayout.addWidget(self.cheongjuUniv_loan)
        loanChangeLayout.addWidget(self.booknarae_loan)
        loanChangeLayout.addWidget(self.start_btn)
        
        self.scrollSetting(100)
        
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addLayout(loanChangeLayout)
        
    def keris_loan_click(self): # keris 상호대차
        print('keris_loan btn click')
        txt1 = "이용대상 : 학부생, 대학원생, 교직원, 지역주민 회원\n"
        txt2 = '<신청방법>\n1. 도서관 홈페이지 로그인 - 도서관 서비스 - 상호대차에서 검색\n'
        txt3 = "2. RISS 홈페이지 가입 - 소속도서관 청주대학교로 설정 - 기관 승인 확인"
        txt4 = "대출 규정 : 3책 15일"
        keris_loanText = QLabel(txt1+txt2+txt3+txt4)
        #keris_loanText.setMaximumSize(520,100)
        keris_loanText.setFont(QFont('굴림',10))
        keris_loanText.setStyleSheet(self.lb_style)
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addWidget(keris_loanText)
        self.loanChange_click()
        
        self.scrollSetting(110)
        
    def cheongjuUniv_loan_click(self): #청주권 대학도서관 상호대차
        print('cheongjuUniv_loan_click btn click')
        txt1 = "이용대상 : 학부생, 대학원생, 교직원(재학생만 해당)\n"
        txt2 = '<신청방법>\n홈페이지 - 도서관 서비스 - 타도서관 이용의뢰서\n'
        txt3 = " - 신청 - MyLibrary - 타도서관 이용의뢰서 - 출력"
        txt4 = "대출 규정 : 2책 10일"
        cheongjuUniv_loanText = QLabel(txt1+txt2+txt3+txt4)
        #cheongjuUniv_loanText.setMaximumSize(520,100)
        cheongjuUniv_loanText.setFont(QFont('굴림',10))
        cheongjuUniv_loanText.setStyleSheet(self.lb_style)
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addWidget(cheongjuUniv_loanText)
        self.loanChange_click()
        
        self.scrollSetting(110)
        
    def booknarae_loan_click(self): #책나래 상호대차
        print('booknarae_loan_click btn click')
        txt1 = "이용대상 : 등록장애인, 거동불편자, 국가유공자\n"
        txt2 = '<이용대상>\n도서관 방문이 어려운 장애인 등을 위하여 이용자가 필요로 하는\n'
        txt3 = "도서관 자료를 우체국 택배를 이용하여 무료로 집까지 제공해주는 서비스\n"
        txt4 = "대출 규정 : 제공 도서관 규정에 따름\n"
        txt5 = "<이용 절차>\n거주지역 도서관과 책나래 홈페이지 회원가입 후 나의 도서관 등록\n"
        txt6 = "회원가입 승인 - 책나래에서 자료 검색 후 대출 신청 - 대출 처리 - 자료 배송"
        cheongjuUniv_loanText = QLabel(txt1+txt2+txt3+txt4+txt5+txt6)
        #cheongjuUniv_loanText.setMaximumSize(520,220)
        cheongjuUniv_loanText.setFont(QFont('굴림',10))
        cheongjuUniv_loanText.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addWidget(cheongjuUniv_loanText)
        self.loanChange_click()
        
        self.scrollSetting(230)
        
    
    #--------------------------------------------------------------------
    def bookCopy_click(self): #원문복사 버튼
        print('bookCopy_click click')
        txt1 = "우리 도서관이 소장하지 않은 자료를 협력기관에 복사 의뢰하여 제공받는 유료 서비스입니다.\n"
        txt2 = '<제공정책>\n단행본 및 학위논문 : 저작권보호로 50% 미만 제공\n'
        txt3 = "학술지 : 학술지 수록논문 단위로 제공\n"
        txt4 = "<이용요금>\n일반우편 : 기본요금(우송료)+복사비 정당 70원/4~6일 소요\n"
        txt5 = "빠른우편 : 기본요금(우송료)+복사비 정당 70원/3~5일 소요\n"
        txt6 = "전자우편 : 복사비 정당 100원/1~2일 소요"
        bookCopy_loanText1 = QLabel(txt1+txt2+txt3+txt4+txt5+txt6)
        #bookCopy_loanText1.setMaximumSize(520,250)
        bookCopy_loanText1.setFont(QFont('굴림',9))
        bookCopy_loanText1.setStyleSheet(self.lb_style)
        
        txt7="<신청방법>\n도서관 홈페이지 : 로그인 - 도서관서비스 - 원문복사에서 검색 혹은 직접입력\n"
        txt8="RISS 직접 신청 : 홈페이지 로그인 - 검색 - 복사/대출 신청"
        bookCopy_loanText2 = QLabel(txt7+txt8)
        #bookCopy_loanText2.setMaximumSize(520,100)
        bookCopy_loanText2.setFont(QFont('굴림',10))
        bookCopy_loanText2.setStyleSheet(self.lb_style)
        
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addWidget(bookCopy_loanText1)
        centerLayout.addWidget(bookCopy_loanText2)
        
        self.scrollSetting(240)
        
        self.studyHelp_click()
        
        
    #--------------------------------------------------------------------    
    def paperGo_click(self): #학위논문제출 버튼
        print('paperGo_click click')
        txt1 = "<온라인 제출>\n"
        txt2 = '제출주소 : 청주대학교 dCollection 홈페이지(http://cju.dcollection.net)에서 로그인 후 pdf파일 제출\n'
        txt3 = "로그인방법 : 제출자 로그인인증(아이디-학번, 이름, 이메일주소 입력하여 인증후 로그인)\n"
        txt4 = "제출기간 : 매년 6월, 12월 제출공고일에 제출\n"
        txt5 = "유의사항 : 원문 pdf파일에 반드시 인준지 심사위원 이름, 인장 날인이 포함됨\n"
        txt6 = "제출순서 : 온라인 제출 → 검증 → 승인완료 → 학위논문저작물이용허락서, 학위논문제출확인서 출력"
        paperGo_loanText1 = QLabel(txt1+txt2+txt3+txt4+txt5+txt6)
        #paperGo_loanText1.setMaximumSize(520,250)
        paperGo_loanText1.setFont(QFont('굴림',9))
        paperGo_loanText1.setStyleSheet(self.lb_style)
        
        txt7="<인쇄본 제출>\n제출장소 : 중앙도서관 학술정보지원팀(도서관5층)\n"
        txt8="제출기간 : 매년 6월, 12월 제출공고일에 제출"
        txt9="제출부수 : 학위논문 인쇄본 4부(하드커버)"
        txt10="제출서류 : 학위논문저작물이용허락서(제출), 학위논문제출확인서(제시)-확인 날인"
        paperGo_loanText2 = QLabel(txt7+txt8+txt9+txt10)
        #paperGo_loanText2.setMaximumSize(520,150)
        paperGo_loanText2.setFont(QFont('굴림',10))
        paperGo_loanText2.setStyleSheet(self.lb_style)
        
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addWidget(paperGo_loanText1)
        centerLayout.addWidget(paperGo_loanText2)
        
        self.scrollSetting(230)
        
        self.studyHelp_click()
    
    #--------------------------------------------------------------------
    
    def infra_click(self): #시설 안내
        print("infra_click button click")
        #시설 안내 메뉴 텍스트 설정
        txt = '이용을 원하시는 시설을 클릭하세요.'
        infraText = QLabel(txt)
        infraText.setMaximumSize(450,30)
        infraText.setFont(QFont('굴림',10))
        infraText.setStyleSheet(self.lb_style)
        #버튼 집합
        infraMenuLayout = QGridLayout() # 버튼 집합 레이아웃 설정
        
        self.monileApp = QPushButton("모바일 이용증", self) #버튼 객체 추가
        self.monileApp.clicked.connect(self.monileApp_infra_click)
        
        self.studyinfra = QPushButton("열람실", self) #버튼 객체 추가
        self.studyinfra.clicked.connect(self.readingRoom_infra_click)
        
        self.groupstudyRoom = QPushButton("그룹 스터디룸", self) #버튼 객체 추가
        self.groupstudyRoom.clicked.connect(self.studyRoom_infra_click)
        
        self.mulitmedia_infra = QPushButton("멀티미디어 감상실", self) #버튼 객체 추가
        self.mulitmedia_infra.clicked.connect(self.mulitmedia_infra_click)
        
        self.infoRounge_infra = QPushButton("정보검색라운지", self) #버튼 객체 추가
        self.infoRounge_infra.clicked.connect(self.infoRounge_infra_click)
        
        self.selfReturn = QPushButton("자가대출반납기", self) #버튼 객체 추가
        self.selfReturn.clicked.connect(self.selfReturn_infra_click)
        
        self.copyPrint_infra = QPushButton("복사/출력실", self) #버튼 객체 추가
        self.copyPrint_infra.clicked.connect(self.copyPrint_infra_click)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        
        #그리드 레이아웃에 버튼 위치 배치
        infraMenuLayout.addWidget(self.monileApp, 0, 0)
        infraMenuLayout.addWidget(self.studyinfra, 0, 1)
        infraMenuLayout.addWidget(self.groupstudyRoom, 0, 2)
        infraMenuLayout.addWidget(self.mulitmedia_infra, 0, 3)
        infraMenuLayout.addWidget(self.infoRounge_infra, 1, 0)
        infraMenuLayout.addWidget(self.selfReturn, 1, 1)
        infraMenuLayout.addWidget(self.copyPrint_infra, 1, 2)
        infraMenuLayout.addWidget(self.start_btn, 1, 3)
        
        
        
        self.scrollSetting(90)
        centerLayout.addWidget(infraText)
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addLayout(infraMenuLayout)
    
    #  #  #  #  #  #  #  #  #  #  #  #
    # 시설 안내 클릭 이벤트 버튼 #
    #   #  #  #  #  #  #   #  #  #  #
    
    def monileApp_infra_click(self): #모바일 이용증
        print("monileApp_click button click")
        self.infra_click()
        
    def readingRoom_infra_click(self): #열람실
        print("readingRoom_infra_click button click")
        self.infra_click()
        
    def studyRoom_infra_click(self): # 그룹 스터디룸
        print("studyRoom_infra_click button click")
        self.infra_click()
        
    def mulitmedia_infra_click(self): #멀티미디어 감상실
        print("mulitmedia_infra_click button click")
        self.infra_click()
        
    def infoRounge_infra_click(self): #정보검색라운지
        print("infoRounge_infra_click button click")
        self.infra_click()
        
    def selfReturn_infra_click(self): #자가대출반납기
        print("selfReturn_click button click")
        self.infra_click()
        
    def copyPrint_infra_click(self): #복사 출력실
        print("copyPrint_infra_click button click")
        self.infra_click()
    #--------------------------------------------------------------------

    #시작하자마자 뜨는 메시지
    def startMessage(self):
        print('start')
        
        start_set = starter() #스타터 클래스 불러옴
        #중앙 라벨에 centerlayout을 레이아웃으로 설정
        self.lb_center.setLayout(start_set.start_def())
        
        self.scrollSetting(70)
        
        #메뉴 버튼에 클릭 이벤트 설정
        start_set.useTime_btn.clicked.connect(self.useTime_click)
        start_set.enter_btn.clicked.connect(self.enter_click)
        start_set.infra_btn.clicked.connect(self.infra_click)
        start_set.findWay_btn.clicked.connect(self.findWay_click)
        start_set.studyHelp_btn.clicked.connect(self.studyHelp_click)
    
    #--------------------------------------------------------------------

class starter():

    def __init__(self):
        super().__init__()
        
    #시작하자마자 뜨는 메뉴 버튼 집합 함수
    def startMsg(self):
        btnSetLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        self.useTime_btn = QPushButton("이용 시간") #이용시간 버튼 객체 추가
        #self.useTime_btn.clicked.connect(myap.useTime_click())
        btnSetLayout.addWidget(self.useTime_btn) #버튼집합 레이아웃에 버튼 추가
        
        self.enter_btn = QPushButton("출입 안내") #찾아오는 길 버튼 객체 추가
        #self.enter_btn.clicked.connect(myap.enter_click())
        btnSetLayout.addWidget(self.enter_btn)
        
        self.infra_btn = QPushButton("시설 안내")
        #infra_btn.clicked.connect(myap.infra_click)
        btnSetLayout.addWidget(self.infra_btn)
        
        self.studyHelp_btn = QPushButton("연구학습지원") 
        #studyHelp_btn.clicked.connect(myap.studyHelp_click)
        btnSetLayout.addWidget(self.studyHelp_btn)
        
        self.findWay_btn = QPushButton("오시는 길") 
        #findWay_btn.clicked.connect(myap.findWay_click)
        btnSetLayout.addWidget(self.findWay_btn)
        
        return btnSetLayout #버튼 집합 레이아웃 반환
    
    #시작하자 마자 뜨는 이용 방법 텍스트 라벨 반환 함수
    def startText(self):
        startText1 = QLabel('안녕하세요')
        #startText1.setMaximumSize(150,30)
        startText1.setFont(QFont('굴림',11))
        startText1.setStyleSheet(lb_styles) #라벨 꾸미기 
        
        startText2 = QLabel('원하시는 버튼을 클릭해주세요.\n채팅으로 검색하셔도 됩니다.')
        #startText2.setMaximumSize(260,50)
        startText2.setFont(QFont('굴림',11))
        startText2.setStyleSheet(lb_styles)
        
        startText3 = QLabel('도서검색을 하시려면 앞에 !를 붙여주세요.')
        #startText2.setMaximumSize(260,50)
        startText3.setFont(QFont('굴림',11))
        startText3.setStyleSheet(lb_styles)
        #텍스트 라벨 2개를 리스트 형태로 반환
        return [startText1, startText2, startText3]
    
    #스타터 클래스 메인 함수 / 위 2개 함수를 활용하여 최초 출력 레이아웃 반환
    def start_def(self):
        #텍스트 라벨 추가
        centerLayout.addWidget(self.startText()[0])
        centerLayout.addWidget(self.startText()[1])
        centerLayout.addWidget(self.startText()[2])
        
        #메뉴 버튼 집합 레이아웃 추가
        centerLayout.addLayout(self.startMsg())  #레이아웃 추가  !!!!!!
        centerLayout.setAlignment(Qt.AlignTop)
        # 최초 출력 레이아웃 반환
        return centerLayout

if __name__ == '__main__':
    print("open app")
    #bookSearch('')
    centerLayout = QVBoxLayout()
    lb_styles = ("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
    #centerHeight = 650
    app = QApplication(sys.argv)
    ex = MyApp()
    start = ex.startMessage()
    sys.exit(app.exec_())
    
    
