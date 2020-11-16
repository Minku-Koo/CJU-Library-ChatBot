# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot
# developer E-mail : corleone@kakao.com

from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from cjubot_library import *
from PyQt5.QtCore import * 
from PyQt5 import QtCore

class MyApp(QWidget):
    
    #키보드 키 판별하여 엔터 추출
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyRelease and obj is self.inputTextBox:
            if event.key() == QtCore.Qt.Key_Return and self.inputTextBox.hasFocus():
                print('Enter pressed')
                self.TextInput_click() # enter누르면 실행
        return super().eventFilter(obj, event)
        
    def __init__(self):
        super().__init__()
        self.centerHeight = 650  #중앙 채팅창 높이
        self.widgetHeight = 0 #시작 높이 
        self.lb_style = lb_styles #라벨 스타일
        self.initUI()
        
    #스크롤 조정, 라벨 추가할 때마다 중앙라벨 높이 증가
    def scrollSetting(self, size):
        self.widgetHeight+=(size)
        if self.widgetHeight >= 650: #스크롤바 늘려주기
            self.centerHeight=self.widgetHeight
            self.lb_center.setFixedHeight(self.centerHeight)
        
    #라벨 추가 함수, size변수 지금 필요없음
    def labelPlus(self, text, fontSize , size):
        label = QLabel(text)
        label.setFont(QFont('굴림',fontSize))
        label.setStyleSheet(self.lb_style)
        
        text_list = text.split('\n')
        print(text_list)
        max_size, max_str=0, ''
        #텍스트 세로값 설정
        for e in text_list:
            if len(e) >= max_size:
                max_str =e
                max_size = len(e)
        #텍스트 가로값 추출
        input_width = label.fontMetrics().boundingRect( max_str ).width()+10
        
        scrollHeightPlus = len(text_list) *21
        label.setFixedHeight(scrollHeightPlus)
        label.setFixedWidth(input_width)
        centerLayout.addWidget(label)
        
        self.scrollSetting(scrollHeightPlus)
        self.vbar.setValue(self.vbar.maximum())
        
    #도서 검색 메인 '
    def bookSearch(self, name):
        
        self.labelPlus('어떤 방법으로 검색하시겠습니까?', 9, 20)
        
        self.keyword_btn = QPushButton("키워드 검색", self) #버튼 객체 추가
        self.keyword_btn.clicked.connect(self.keyword_btn_click)
        self.keyword_btn.setStyleSheet(bt_styles)
        
        self.allsame_btn = QPushButton("완전일치 검색", self) #버튼 객체 추가
        self.allsame_btn.clicked.connect(self.allsame_btn_click)
        self.allsame_btn.setStyleSheet(bt_styles)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        self.start_btn.setStyleSheet(bt_styles)
        
        bookstartLayout = QHBoxLayout()
        bookstartLayout.addWidget(self.keyword_btn)
        bookstartLayout.addWidget(self.allsame_btn)
        bookstartLayout.addWidget(self.start_btn)
        self.scrollSetting(35)
        
        self.vbar.setValue(self.vbar.maximum())
        centerLayout.addLayout(bookstartLayout)
        
        
    def book(self, n): #도서 검색 결과를 가지고 출력 분류
    
        self.searchBy = n
        #도서 검색 리스트 결과 받음
        self.bookListResult = bookListSearch(n, self.bookName, 0)
        if self.bookListResult[0] <0:
            txt = '좀 더 구체적으로 검색해주세요'
            self.labelPlus(txt, 7 , 50)
        # 검색 도서가 10개 미만일 경우 -- 바로 도서 선택
        elif 10 >= self.bookListResult[0] and self.bookListResult[0] >0:
            bookList = self.bookListResult[2]
            for booklist in bookList: #전체출력 
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                bookAll = QLabel(txt) # 텍스트 합쳐서 입력
                self.labelPlus(txt, 7 , 50)
            
            print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
            txt='출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.'
            self.labelPlus(txt, 8 , 30)
            
        # 도서 검색 결과가 없는 경우 - 다시 진행
        elif self.bookListResult[0]==0:
            txt='검색 결과가 없습니다.'
            self.labelPlus(txt, 9 , 20)
            
        else: #검색 결과 10개 이상일 경우
            print("총 "+str(self.bookListResult[0])+"건의 도서가 검색되었습니다.")
            print("출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.")
            print("0번은 전체 출력\n다시 검색하실 수 있습니다.")
            
            bookList = self.bookListResult[2]
            for booklist in bookList: #상위 10개 출력
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                self.labelPlus(txt, 7 , 50)
                
            
            bookText3 = "총 "+str(self.bookListResult[0])+\
                        "건의 도서가 검색되었습니다."
            self.labelPlus(bookText3, 9 , 50)
            
            bookText4 = '출력한 도서 중 원하는 도서가 있으면 번호를 입력해주세요.'
            self.labelPlus(bookText4, 9 , 50)
            
            bookText5 = '0번은 전체 출력\n다시 검색하실 수 있습니다.'
            self.labelPlus(bookText5, 9 , 50)
            
 
    def keyword_btn_click(self):
        print('keyword_btn_click')
        self.book('1')
        
    def allsame_btn_click(self):
        print('allsame_btn_click')
        self.book('2')
        
    def bookNum_click(self): #10개 미만 도서 선택
        self.selectBook = self.inputTextBox.toPlainText().strip()
        self.selectBook.replace(' ','')
        self.selectBook.replace('\n','')
        self.selectBook.replace('\r','')
        
        if self.selectBook == '0':  #전체출력
            bookList = bookListSearch(self.searchBy, self.bookName, 100)[2]
            for booklist in bookList: #전체출력 
                txt = booklist[0]+'\n'+booklist[1]+'\n'+booklist[2]
                self.labelPlus(txt, 7 , 50)
                
        elif self.selectBook.isdigit() : #도서 선택, 상세정보 출력
            code = bookCode(self.bookListResult[1], int(self.selectBook))
            bookDetail = bookDetailSearch(code)
            
            txt = "제목 : "+str(bookDetail[0]) +"\n저자 : "+str(bookDetail[1]) +\
            "\n출판사 : "+str(bookDetail[2]) +\
            "\n도서 위치 : "+str(bookDetail[3]) +\
            "\n대출 여부 : "+str(bookDetail[4])
            self.scrollSetting(70)
            self.labelPlus(txt, 8 , 100)
            
        else:
            print(self.selectBook)
        return self.selectBook
    
    #키보드 입력 이벤트, 필요없음
    def keyPressEvent(self, qKeyEvent):
        print(qKeyEvent.key())
        if qKeyEvent.key() == QtCore.Qt.Key_Return: 
            print('Enter pressed')
        else:
            super().keyPressEvent(qKeyEvent)
    
    #GUI 설정
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
        #lb_head.setMaximumSize(55000,90) #라벨 최대사이즈
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
                              "background-color: white;"
                            )
        
        
        self.lb_bottom = QLabel()
        self.inputTextBox = QTextEdit()
        self.inputTextBox.setAcceptRichText(False)
        self.inputTextBox.setFixedHeight(70) #라벨 최대사이즈
        #self.lb_bottom.addWidget(inputTextBox)
        self.TextInputButton = QPushButton("입 력", self) #버튼 객체 추가
        self.TextInputButton.clicked.connect(self.TextInput_click)
        #self.TextInputButton.keyPressEvent = self.keyPressEvent()
        #self.inputTextBox.returnPressed.connect(self.TextInput_click)
        # 텍스트 박스 keypress 
        self.inputTextBox.installEventFilter(self)
        self.TextInputButton.setStyleSheet("color : #0B1580;" #버튼 꾸미기
                              "border-style: solid;"
                              "border-width: 3px;"
                              #"border-color: black;"
                              "border-radius: 3px;"
                              "border-color:#406BE5;"
                              "background-color: #5FCEED;"
                              "font-size: 22px;"
                              'height: 60px;'
                              "width: 100px;"
                            )
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.inputTextBox)
        self.bottomLayout.addWidget(self.TextInputButton)
        
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
        self.vbar = self.scroll.verticalScrollBar()
        
        #레이아웃에 라벨 추가
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(lb_head)
        self.mainLayout.addWidget(self.scroll) #라벨 말고 qscrollarea를 입력해야함
        self.mainLayout.addLayout(self.bottomLayout)
        
        self.mainLayout.setAlignment(Qt.AlignTop)
        
        self.setLayout(self.mainLayout) #main layout
        
        self.show() #화면에 표시
        
    def center(self): #어플을 화면 중심에 위치시키는 함수
        qr = self.frameGeometry() #창의 위치 크기 정보 불러옴
        cp = QDesktopWidget().availableGeometry().center() #화면 가운데 위치 식별
        qr.moveCenter(cp) #화면 중심으로 이동
        self.move(qr.topLeft())
        
    # 텍스트 박스 클릭 함수
    def TextInput_click(self):
        print(self.inputTextBox.toPlainText())
        #텍스트 박스 읽어오기
        self.userText = self.inputTextBox.toPlainText()[:-1]
        
        self.userText = self.userText.replace(' ','')
        self.userText = self.userText.replace('\n','')
        
        lb_user_text = QLabel( self.userText) #입력한 텍스트 
        
        lb_user_text.setFont(QFont('굴림',10))
        lb_user_text.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #F3DA80"
                            )
        if self.userText != "": #무언가 입력되었다면
            emptyLabel = QLabel() # 빈 라벨 추가 for 오른쪽 정렬
            textSetLayout = QGridLayout()
            textSetLayout.addWidget(emptyLabel, 0, 0)
            textSetLayout.addWidget(lb_user_text, 0, 1)
            lb_user_text.setAlignment(Qt.AlignRight)
            
            text_list = self.userText.split('\n')
            
            #입력 텍스트 가로, 세로 길이 설정
            input_width = lb_user_text.fontMetrics().boundingRect( self.userText ).width()+10
            input_height = len(text_list) *22
            
            lb_user_text.setFixedWidth(input_width) #글자수 만큼 넓이 계산
            lb_user_text.setFixedHeight(input_height) #글자수 만큼 넓이 계산
            centerLayout.addLayout(textSetLayout) #레이아웃에 입력한 텍스트 출력
            # 아주 중요한 크기 구하는 메서드
            self.scrollSetting(28)
        
        self.mainText(self.userText)
        self.inputTextBox.clear() # textEdit clear
        
    # 입력받은 텍스트 판별하고 출력해주는 아주 아주 중요한 것
    def mainText(self, text):
        print("text main")
        if text.isdigit() and len(text) <2: # 도서 선택 경우 
            self.bookNum_click()
            return 0
            
        if len(text.replace(' ', '').replace('\n','')) <1: #아무것도 입력 안함
            return 0
            
        self.bookName = text[1:]
        if text[0] == '!': #도서검색
            self.bookSearch(text[1:])
            return 0
            
        #키워드 분석 
        useTime_text = ['이용시간', '시간', '몇시', '언제', '열어'
                        '몉시','언재','열러','time','tlrks', 'auctl', 'djswp']
        useInfra_text = ["어떻",  "어떤",'어떠ㄴ','어떡']
        way_text = ["어디", '찾아가', '버스', '택시', '가는길', '얼마나', '어떻게',\
                    'djel','qjtm','bus','taxi','djfaksk','djEJgrp','어뜨케','차자가']
                    
        study_text = {"논문":"paperGo", '상호대차':"loanChange", '원몬복사':"bookCopy",
                '논문제출':"paperGo", '학위논문':"paperGo", 'keris':"keris_loan",
                'KERIS':"keris_loan",'충북대':"cheongjuUniv_loan", '서원대':"cheongjuUniv_loan",
                '청주교대':"cheongjuUniv_loan",'paper':"paperGo", 
                "shsans":"paperGo", 'tkdgheock':"loanChange", 'dnjsansqhrtk':"bookCopy",
                'shsanswpcnf':"paperGo", 'gkrdnlshsans':"paperGo",
                '대차':"loanChange", '원문':"bookCopy",
                 '책나래':"booknarae", '도서복사':"bookCopy",'책복사':"bookCopy",
                 "대출":"loanBook","연장":"loanBook", "연체":"lateReturn"
                 }
        infra_text = {
        '자료실': 'referenceRoom_', '열람실': 'readingRoom_', 
        '스터디룸': 'studyRoom_', '출력': 'copyPrint_', '노트북': 'notebookRoom_', 
        'wkfy': 'referenceRoom_', 'duffka': 'readingRoom_', 
        'tmxjelfna': 'studyRoom_', 'cnffur': 'copyPrint_', 'shxmqnr': 'notebookRoom_', 
        'referenc': 'referenceRoom_', 'read': 'readingRoom_', 
        'study': 'studyRoom_', 'print': 'copyPrint_', 'notebook': 'notebookRoom_', 
        '복사': 'copyPrint_','멀티미디어':'multimedia_', '정보검색':'infoRounge_',
        '모바일':"monileApp_", '대출반납기':'selfReturn_', '반납':"selfReturn_", '자가대출':"selfReturn_",
        'copy': 'copyPrint_','multi':'multimedia_', 'inform':'infoRounge_',
        'mobile':"monileApp_", 'return':'selfReturn_', 'self':"selfReturn_", 'qksskq':"selfReturn_",
        'qhrtk': 'copyPrint_','ajfxl':'multimedia_', 'wjdqh':'infoRounge_',
        'ahqkdlf':"monileApp_", 'app':'monileApp_', 'qksskq':"selfReturn_", 
        '대출반납':"selfReturn_"}
        
        extra_text = {
            '찢어':'책은 찢으면 안돼요. 도서관 물건은 내 물건처럼',
            '맨유':'맨유우승가자',
            '훔치':'훔치면 깜빵가요. 조심하세요.',
            '몰래':'허튼짓 하다가 골로 갑니다',
            '담배':'담배는 밖에서 알아서 피세요',
            '흡연':'담배는 밖에서 알아서 피세요',
            '술':'술은 술집에서 드세요 제발',
            '침입':'세콤은 강력하답니다',
            '배고파':'밥을 드세요',
            '목말':'물을 드세요',
            '시발':'어머 욕 하지마요',
            '시바':'욕은 싫어요',
            'ㅅㅂ':'욕설은 자제하고 다시 말하죠',
            '에휴':'왜 한숨을 쉬어요',
            '어휴':'한숨 쉬지 마세요',
            '잠온다':'집가서 주무세요',
            '졸려':'도서관에는 침대가 없어요',
            '졸리':'도서관에서 자면 혼나요',
            '노래':'제가 제일 좋아하는 노래는 it ain`t me입니다',
            '누구':'전 청주도서관 도우미 챗봇이예요'
        }
        
        text = text.replace(" ", "").replace('\n','')
        result = ''
        
        for txt in extra_text: #아무말 검사
            if txt in text:
                result += 'F-'
                break
        
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
        
        if len(resultList) == 0: #아무것도 알아듣지 못한 경우
            print('cannot read')
            self.labelPlus("뭐라는구요?", 8, 20)
            self.scrollSetting(15)
        
        # 시설이름/연구학습지원 이름만 있을 경우
        elif  len(resultList[-1]) >1 :  # 이름일 경우
            print_text = chatAnalysis(resultList[-1])
            print(print_text)
            #텍스트 출력
            self.labelPlus(print_text[0], 8, print_text[1])
            #self.scrollSetting(80)
            self.scrollSetting(15)
            
            
        elif len(resultList[0]) ==1: # 시간 또는 시설 alphabet만 있을 경우
            if resultList[0]=='T': #시간 혼자
                self.useTime_click()
            elif 'E' in resultList: # E 가 리스트에 있을 경우 / 출입방법
                self.enter_click()
            elif 'W' in resultList: # W 가 리스트에 있을 경우 / 오시는길 바로 출력
                self.findWay_click()
            elif 'F' in resultList:
                for txt in extra_text: #아무말 검사
                    if txt in text:
                        self.labelPlus(extra_text[txt], 8, 20)
                        self.scrollSetting(15)
                        print('anything say')
                        break
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
        txt = '09시~20시(학기중 평일), 18시(방학중 평일), 23시(시험기간중 평일)'
        self.labelPlus(txt, 9,30)
        self.useTime_click()
        
    def studyRoom_click(self): 
        print("스터디룸")
        txt='2층 1~8호 : 09시~00시\
\n이외 : 09시~20시(학기중), 23시(시험기간), 18시(방학중)' 
        self.labelPlus(txt,9, 30)
        self.useTime_click()
        
    def notebookRoom_click(self, link): 
        print("노트북 열람실")
        txt='1층 복사실 :09시~18시, 방학중 휴실\
\n정보검색라운지 :연중 06시~24시'
        self.labelPlus(txt,9, 30)
        self.useTime_click()
        
    def multimedia_click(self): 
        print("멀티미디어 감상실")
        self.labelPlus('09시~20시(학기) 18시(방학)',9, 20)
        self.useTime_click()
        
    def readingRoom_click(self): 
        print("제 1~3 열람실")
        txt = '제1~3열람실 : 연중무휴 24시간 순환개방\
\n대학원열람실 : 06시~00시'
        self.labelPlus(txt,9, 20)
        #self.scrollSetting(5)
        self.useTime_click()
        
    def infoRounge_click(self): 
        print("정보검색라운지")
        txt ='09시~00시'
        self.labelPlus(txt,9, 20)
        self.useTime_click()
        
    def copyPrint_click(self): 
        print("복사/출력실")
        txt = '1층 복사실 : 09시~18시, 방학중 휴실\n\
정보검색라운지 : 연중 06시~24시\n\
3~4층 자료실: 09시~20시(학기중), 23시(시험기간), 18시(방학중)'
        self.labelPlus(txt,9, 20)
        self.useTime_click()
        
    def start_btn_click(self):
        print('처음으로')
        self.startMessage() #최초 출력 함수 
    
    def useTime_click(self): #이용시간 클릭 하면 나타나는 레이아웃
        print("use time button click")
        #이용시간 메뉴 텍스트 설정
        useTimeText1 ='이용을 원하시는 시설을 클릭해주세요.'
        self.labelPlus(useTimeText1, 10,20)
        
        useTimeLayout = QGridLayout() # 버튼 집합 레이아웃 설정
        
        self.referenceRoom = QPushButton("제 1~3 자료실", self) #버튼 객체 추가
        self.referenceRoom.clicked.connect(self.referenceRoom_click)
        self.referenceRoom.setStyleSheet(bt_styles)
        
        self.studyRoom = QPushButton("스터디룸", self) #버튼 객체 추가
        self.studyRoom.clicked.connect(self.studyRoom_click)
        self.studyRoom.setStyleSheet(bt_styles)
        
        self.notebookRoom = QPushButton("노트북 열람실", self) #버튼 객체 추가
        self.notebookRoom.clicked.connect(self.notebookRoom_click)
        self.notebookRoom.setStyleSheet(bt_styles)
        
        self.multimedia = QPushButton("멀티미디어 감상실", self) #버튼 객체 추가
        self.multimedia.clicked.connect(self.multimedia_click)
        self.multimedia.setStyleSheet(bt_styles)
        
        self.readingRoom = QPushButton("제 1~3 열람실", self) #버튼 객체 추가
        self.readingRoom.clicked.connect(self.readingRoom_click)
        self.readingRoom.setStyleSheet(bt_styles)
        
        self.infoRounge = QPushButton("정보검색라운지", self) #버튼 객체 추가
        self.infoRounge.clicked.connect(self.infoRounge_click)
        self.infoRounge.setStyleSheet(bt_styles)
        
        self.copyPrint = QPushButton("복사/출력실", self) #버튼 객체 추가
        self.copyPrint.clicked.connect(self.copyPrint_click)
        self.copyPrint.setStyleSheet(bt_styles)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        self.start_btn.setStyleSheet(bt_styles)
        
        #그리드 레이아웃에 버튼 위치 배치
        useTimeLayout.addWidget(self.referenceRoom, 0, 0)
        useTimeLayout.addWidget(self.studyRoom, 0, 1)
        useTimeLayout.addWidget(self.notebookRoom, 0, 2)
        useTimeLayout.addWidget(self.multimedia, 0, 3)
        useTimeLayout.addWidget(self.readingRoom, 1, 0)
        useTimeLayout.addWidget(self.infoRounge, 1, 1)
        useTimeLayout.addWidget(self.copyPrint, 1, 2)
        useTimeLayout.addWidget(self.start_btn, 1, 3)
        
        self.scrollSetting(58)
        useTimeLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 이용시간 버튼 집합 레이아웃 추가
        centerLayout.addLayout(useTimeLayout)
        self.vbar.setValue(self.vbar.maximum())
    
    def findWay_click(self):  #오시는길
        print("findWay_click button click")
        #오시는길 텍스트 설정
        txt1 = '<버스>\n1. 청주고속터미널-시내버스(청주대 방면) 40분\n'
        txt2 = '2. 청주시외버스터미널-시외버스(충주,괴산방면 \n북청주터미널 경유 버스) 25분\n'
        txt3 = '3. 북청주터미널-청대정문(도보 7분)'
        #findWayText1.setMaximumSize(450,90)
        self.labelPlus(txt1 + txt2+txt3,9, 20)
        
        findWayText = '<택시>\n가경동 청주터미널 앞 택시 승강장 이용(약 25분)\n\
북청주터미널에서 정문까지 7분, 예술대학 10분'
        self.labelPlus(findWayText,9, 20)
        
        #centerlayout에 출입안내 버튼 집합 레이아웃 추가
        self.startMessage() #최초 출력 함수 

    #--------------------------------------------------------------------
    
    def enter_click(self):#출입 안내
        print("enter_click button click")
        #이용시간 메뉴 텍스트 설정
        txt1 = '도서관 출입문에 출입통제시스템이 설치되어\n'
        txt2 = '학생증 또는 모바일 이용증이 있어야 출입 할 수 있으니\n도서관에 올 때는 학생증을 지참하여야 합니다.'
        self.labelPlus(txt1+txt2,9, 20)
        
        enterText ='<출입방법>\n입구통제기의 스캐너에 학생증(모바일 이용증) 스캐닝 → 녹색램프 → 입장'
        self.labelPlus(enterText,9, 20)
        #centerlayout에 출입안내 버튼 집합 레이아웃 추가
        self.startMessage() #최초 출력 함수 
    
    #--------------------------------------------------------------------
    
    def studyHelp_click(self): #연구학습지원 버튼
        print("studyHelp_click button click")
        #시설 안내 메뉴 텍스트 설정
        txt = '원하시는 연구학습 내용을 선택하세요.'
        self.labelPlus(txt,9, 20)
        #버튼 집합
        studyHelpLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        
        self.loanChange = QPushButton("상호 대차", self) #버튼 객체 추가
        self.loanChange.clicked.connect(self.loanChange_click)
        self.loanChange.setStyleSheet(bt_styles)
        
        self.bookCopy = QPushButton("원문 복사", self) #버튼 객체 추가
        self.bookCopy.clicked.connect(self.bookCopy_click)
        self.bookCopy.setStyleSheet(bt_styles)
        
        self.paperGo = QPushButton("학위 논문 제출", self) #버튼 객체 추가
        self.paperGo.clicked.connect(self.paperGo_click)
        self.paperGo.setStyleSheet(bt_styles)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        self.start_btn.setStyleSheet(bt_styles)
        
        #레이아웃에 버튼 위치 배치
        studyHelpLayout.addWidget(self.loanChange)
        studyHelpLayout.addWidget(self.bookCopy)
        studyHelpLayout.addWidget(self.paperGo)
        studyHelpLayout.addWidget(self.start_btn)
        
        self.scrollSetting(28)
        #self.scroll.ensureVisible( 0 , self.widgetHeight+40, 0 , 0 ) 
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addLayout(studyHelpLayout)
        self.vbar.setValue(self.vbar.maximum())
        
    #  #  #  #  #  #  #  #  #  #  #  #  #
    # 연구학습지원 클릭 이벤트 버튼 #
    #   #  #  #  #  #  #   #  #  #  #  #
    
    def loanChange_click(self): #상호대차 버튼
        print('loanChange_click click')
        txt1 = "상호대차는 우리 도서관에 없는 도서를\n타 도서관에서 대여 신청할 수 있는 서비스입니다."
        txt2 = '\n원하시는 상호대차 방법을 선택하세요'
        self.labelPlus(txt1+txt2,9, 20)
        
        #버튼 집합
        loanChangeLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        
        self.keris_loan = QPushButton("KERIS 상호대차", self) #버튼 객체 추가
        self.keris_loan.clicked.connect(self.keris_loan_click)
        self.keris_loan.setStyleSheet(bt_styles)
        
        self.cheongjuUniv_loan = QPushButton("청주권 대학도서관", self) #버튼 객체 추가
        self.cheongjuUniv_loan.clicked.connect(self.cheongjuUniv_loan_click)
        self.cheongjuUniv_loan.setStyleSheet(bt_styles)
        
        self.booknarae_loan = QPushButton("책나래", self) #버튼 객체 추가
        self.booknarae_loan.clicked.connect(self.booknarae_loan_click)
        self.booknarae_loan.setStyleSheet(bt_styles)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        self.start_btn.setStyleSheet(bt_styles)
        
        loanChangeLayout.addWidget(self.keris_loan)
        loanChangeLayout.addWidget(self.cheongjuUniv_loan)
        loanChangeLayout.addWidget(self.booknarae_loan)
        loanChangeLayout.addWidget(self.start_btn)
        
        self.scrollSetting(38)
        centerLayout.addLayout(loanChangeLayout)
        self.vbar.setValue(self.vbar.maximum())
        
    def keris_loan_click(self): # keris 상호대차
        print('keris_loan btn click')
        txt1 = "이용대상 : 학부생, 대학원생, 교직원, 지역주민 회원\n"
        txt2 = '<신청방법>\n1. 도서관 홈페이지 로그인 - 도서관 서비스 - 상호대차에서 검색\n'
        txt3 = "2. RISS 홈페이지 가입 - 소속도서관 청주대학교로 설정 - 기관 승인 확인\n"
        txt4 = "대출 규정 : 3책 15일"
        self.labelPlus(txt1+txt2+txt3+txt4, 9,90)
        self.loanChange_click()
        
    def cheongjuUniv_loan_click(self): #청주권 대학도서관 상호대차
        print('cheongjuUniv_loan_click btn click')
        txt1 = "이용대상 : 학부생, 대학원생, 교직원(재학생만 해당)\n"
        txt2 = '<신청방법>\n홈페이지 - 도서관 서비스 - 타도서관 이용의뢰서\n'
        txt3 = " - 신청 - MyLibrary - 타도서관 이용의뢰서 - 출력"
        txt4 = "대출 규정 : 2책 10일"
        self.labelPlus(txt1+txt2+txt3+txt4, 9,90)
        self.loanChange_click()
        
    def booknarae_loan_click(self): #책나래 상호대차
        print('booknarae_loan_click btn click')
        txt1 = "이용대상 : 등록장애인, 거동불편자, 국가유공자\n"
        txt2 = '<이용대상>\n도서관 방문이 어려운 장애인 등을 위하여 이용자가 필요로 하는\n'
        txt3 = "도서관 자료를 우체국 택배를 이용하여 무료로 집까지 제공해주는 서비스\n"
        txt4 = "대출 규정 : 제공 도서관 규정에 따름\n"
        txt5 = "<이용 절차>\n거주지역 도서관과 책나래 홈페이지 회원가입 후 나의 도서관 등록\n"
        txt6 = "회원가입 승인 - 책나래에서 자료 검색 후 대출 신청 - 대출 처리 - 자료 배송"
        
        self.labelPlus(txt1+txt2+txt3+txt4+txt5+txt6, 9,160)
        self.loanChange_click()
        
    #--------------------------------------------------------------------
    def bookCopy_click(self): #원문복사 버튼
        print('bookCopy_click click')
        txt1 = "우리 도서관이 소장하지 않은 자료를 협력기관에 복사 의뢰하여 제공받는 유료 서비스입니다.\n"
        txt2 = '<제공정책>\n단행본 및 학위논문 : 저작권보호로 50% 미만 제공\n'
        txt3 = "학술지 : 학술지 수록논문 단위로 제공\n"
        txt4 = "<이용요금>\n일반우편 : 기본요금(우송료)+복사비 정당 70원/4~6일 소요\n"
        txt5 = "빠른우편 : 기본요금(우송료)+복사비 정당 70원/3~5일 소요\n"
        txt6 = "전자우편 : 복사비 정당 100원/1~2일 소요"
        self.labelPlus(txt1+txt2+txt3+txt4+txt5+txt6, 9,160)
        
        txt7="<신청방법>\n도서관 홈페이지 : 로그인 - 도서관서비스 - 원문복사에서 검색 혹은 직접입력\n"
        txt8="RISS 직접 신청 : 홈페이지 로그인 - 검색 - 복사/대출 신청"
        self.labelPlus(txt7+txt8, 9,160)
        
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
        self.labelPlus(txt1+txt2+txt3+txt4+txt5+txt6, 9,160)
        
        txt7="<인쇄본 제출>\n제출장소 : 중앙도서관 학술정보지원팀(도서관5층)\n"
        txt8="제출기간 : 매년 6월, 12월 제출공고일에 제출"
        txt9="제출부수 : 학위논문 인쇄본 4부(하드커버)"
        txt10="제출서류 : 학위논문저작물이용허락서(제출), 학위논문제출확인서(제시)-확인 날인"
        paperGo_loanText2 = QLabel(txt7+txt8+txt9+txt10)
        self.labelPlus(txt7+txt8+txt9+txt10, 9,160)
        
        self.studyHelp_click()
    
    #--------------------------------------------------------------------
    
    def infra_click(self): #시설 안내
        print("infra_click button click")
        #시설 안내 메뉴 텍스트 설정
        txt = '이용을 원하시는 시설을 클릭하세요.'
        self.labelPlus(txt, 9,90)
        #버튼 집합
        infraMenuLayout = QGridLayout() # 버튼 집합 레이아웃 설정
        
        self.monileApp = QPushButton("모바일 이용증", self) #버튼 객체 추가
        self.monileApp.clicked.connect(self.monileApp_infra_click)
        self.monileApp.setStyleSheet(bt_styles)
        
        self.studyinfra = QPushButton("열람실", self) #버튼 객체 추가
        self.studyinfra.clicked.connect(self.readingRoom_infra_click)
        self.studyinfra.setStyleSheet(bt_styles)
        
        self.groupstudyRoom = QPushButton("그룹 스터디룸", self) #버튼 객체 추가
        self.groupstudyRoom.clicked.connect(self.studyRoom_infra_click)
        self.groupstudyRoom.setStyleSheet(bt_styles)
        
        self.mulitmedia_infra = QPushButton("멀티미디어 감상실", self) #버튼 객체 추가
        self.mulitmedia_infra.clicked.connect(self.mulitmedia_infra_click)
        self.mulitmedia_infra.setStyleSheet(bt_styles)
        
        self.infoRounge_infra = QPushButton("정보검색라운지", self) #버튼 객체 추가
        self.infoRounge_infra.clicked.connect(self.infoRounge_infra_click)
        self.infoRounge_infra.setStyleSheet(bt_styles)
        
        self.selfReturn = QPushButton("자가대출반납기", self) #버튼 객체 추가
        self.selfReturn.clicked.connect(self.selfReturn_infra_click)
        self.selfReturn.setStyleSheet(bt_styles)
        
        self.copyPrint_infra = QPushButton("복사/출력실", self) #버튼 객체 추가
        self.copyPrint_infra.clicked.connect(self.copyPrint_infra_click)
        self.copyPrint_infra.setStyleSheet(bt_styles)
        
        self.start_btn = QPushButton("처음으로", self) #버튼 객체 추가
        self.start_btn.clicked.connect(self.start_btn_click)
        self.start_btn.setStyleSheet(bt_styles)
        
        #그리드 레이아웃에 버튼 위치 배치
        infraMenuLayout.addWidget(self.monileApp, 0, 0)
        infraMenuLayout.addWidget(self.studyinfra, 0, 1)
        infraMenuLayout.addWidget(self.groupstudyRoom, 0, 2)
        infraMenuLayout.addWidget(self.mulitmedia_infra, 0, 3)
        infraMenuLayout.addWidget(self.infoRounge_infra, 1, 0)
        infraMenuLayout.addWidget(self.selfReturn, 1, 1)
        infraMenuLayout.addWidget(self.copyPrint_infra, 1, 2)
        infraMenuLayout.addWidget(self.start_btn, 1, 3)
        
        
        
        self.scrollSetting(40)
        #self.scroll.ensureVisible( 0 , self.widgetHeight+70, 0 , 0 ) 
        centerLayout.setAlignment(Qt.AlignTop)
        centerLayout.addLayout(infraMenuLayout)
        self.vbar.setValue(self.vbar.maximum())
    
    #  #  #  #  #  #  #  #  #  #  #  #
    # 시설 안내 클릭 이벤트 버튼 #
    #   #  #  #  #  #  #   #  #  #  #
    
    def monileApp_infra_click(self): #모바일 이용증
        print("monileApp_click button click")
        txt1 = ' Play 스토어(안드로이드폰), App Store(아이폰)에서\n\
청주대학교 중앙도서관’으로 검색한 후 ‘청주대학교 중앙도서관’앱을 설치하여 사용'
        txt2 = '모바일 이용증 재발급 횟수는 제한이 없으나,\n\
최종 발급된 모바일 이용증만 사용할 수 있습니다.'
        txt3 = '스마트폰마다 1개의 모바일 이용증만 발급이 가능하며,\n\
종합정보시스템의 개인정보에 등록된 전화번호와 실제 사용 전화번호가\n\
다를 경우에는 다음 날부터 사용할 수 있습니다.'
        self.labelPlus(txt1+txt2+txt3, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    def readingRoom_infra_click(self): #열람실
        print("readingRoom_infra_click button click")
        txt1 = """도서관 내 열람실은 재학 중인 학생들의 학업의 용도로 사용할 수 있습니다.
중앙도서관·열람실(일반, 노트북, 대학원열람실)은 좌석발급기 및 모바일 좌석관리를 이용하여 좌석을 발급하여 이용할 수 있습니다."""
        txt2 ="\n제1~3열람실 : 1층 / 820석 / 연중무휴 24시간 순환개방"
        txt3 = """\n<배정>\nMobile : 청주대학교 중앙도서관 App → 로그인 → 열람좌석 에서 배정 및 가배정
좌석 발급기 : 원하는 좌석 클릭 → 학생증 또는 모바일 이용증 인증 → 배정 확인
1회 이용시간 : 6시간 (시험기간중엔 4시간으로 변경)\n좌석배정 후 퇴실 미반납 3회 누석시 2일간 자리배정불가"""
        self.labelPlus(txt1+txt2+txt3, 8, 3)
        self.scrollSetting(16)
        self.infra_click()
        
    def studyRoom_infra_click(self): # 그룹 스터디룸
        print("studyRoom_infra_click button click")
        txt1 = """학생들의 학습형태에 맞는 다양한 형태의 실을 제공하며, 그룹스터디, 회의, 발표 등의 용도로 사용할 수 있으며.
각 실별 LED 모니터를 설치하여 멀티미디어를 통한 자유로운 협업공간으로 재학중인 학부/대학원생만 이용 가능합니다."""
        txt2 = """\n<예약>\nPC : 도서관 홈페이지 → 도서관시설 → 로그인 → 그룹스터디룸
Mobile : 청주대학교 중앙도서관 App → 로그인 → 그룹스터디룸
예약은 이용하려는 날 7일 전부터 당일까지 가능
예약 후, 이용하려는 날 예약 해당시간부터 20분 이내에\n 해당 그룹스터디룸 인증기에 학생증 또는 모바일 이용증으로 인증 후 사용
이용시간은 2시간이며, 2회연장이용가능(1회 연장시 1시간)"""
        self.labelPlus(txt1+txt2, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    def mulitmedia_infra_click(self): #멀티미디어 감상실
        print("mulitmedia_infra_click button click")
        txt1 = "멀티미디어 자료의 대출 및 열람을 지원하는 공간으로 영상, 음악 감상을 할 수 있는 독립적인 공간 확보"
        txt2 = """\n<배정>\n좌석발급기에서 원하는 좌석 클릭 → 학생증 및 모바일 이용증 인증 → 확인
1회 이용시간 : 3시간
<예약>\n만실시 좌석배정기 또는 중앙도서관 App에서 멀티미디어실 버튼 클릭 후 예약 버튼 클릭
→ 좌석 배정 Push Message 수신 → Push Message에 안내된 좌석에서 이용"""
        self.labelPlus(txt1+txt2, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    def infoRounge_infra_click(self): #정보검색라운지
        print("infoRounge_infra_click button click")
        txt = """\n<배정>\n정보검색라운지내 빈좌석PC에서 로그인 후 이용
이용시간은 2시간이며, 1회 연장이용 가능
<예약>\n만실시 정보검색라운지 앞의 Kiosk 또는 청주대학교 중앙도서관 App에서 멀티미디어실 버튼 클릭 후 
예약 버튼 클릭 → 좌석 배정 Push Message 수신 → Push Message에 안내된 좌석에서 
학생증 또는 모바일 이용증 인증 / 도서관 비밀번호 입력 후 이용
20분 이내에 로그인 안했을 시 예약이 자동 취소됩니다."""
        self.labelPlus(txt, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    def selfReturn_infra_click(self): #자가대출반납기
        print("selfReturn_click button click")
        txt1 = "1회에 최대 3권 대출 및 반납 가능"
        txt2 = "\n자가대출반납기에서는 본책만 대출가능"
        txt3 = """\n3~4층 남,북쪽 : 09시 ~ 20시(학기중), 23시(시험기간), 18시(방학) / 대출+반납
5층 남쪽 : 3~4층과 시간 동일 / 대출+반납
1층 로비 : 연중 24시간 / 반납"""
        self.labelPlus(txt1+txt2+txt3, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    def copyPrint_infra_click(self): #복사 출력실
        print("copyPrint_infra_click button click")
        txt1 = "\n1층 복사실 : 유인복사 3대(칼라1대, 흑백2대)"
        txt2 = """\n정보검색라운지 : 무인, 4대(칼라1대, 흑백3대),
3~4층 자료실: 무인, 층별 각 1대"""
        self.labelPlus(txt1+txt2, 8, 3)
        self.scrollSetting(15)
        self.infra_click()
        
    #--------------------------------------------------------------------

    #시작  메시지
    def startMessage(self):
        print('start')
        
        start_set = starter() #스타터 클래스 불러옴
        #중앙 라벨에 centerlayout을 레이아웃으로 설정
        self.lb_center.setLayout(start_set.start_def())
        
        self.scrollSetting(130)
        self.vbar.setValue(self.vbar.maximum())
        #메뉴 버튼에 클릭 이벤트 설정
        start_set.useTime_btn.clicked.connect(self.useTime_click)
        start_set.enter_btn.clicked.connect(self.enter_click)
        start_set.infra_btn.clicked.connect(self.infra_click)
        start_set.findWay_btn.clicked.connect(self.findWay_click)
        start_set.studyHelp_btn.clicked.connect(self.studyHelp_click)
    
    #--------------------------------------------------------------------

# 시작 메시지 + 메뉴 버튼 클래스 
class starter():

    def __init__(self):
        super().__init__()
        
    #시작하자마자 뜨는 메뉴 버튼 집합 함수
    def startMsg(self):
        btnSetLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        self.useTime_btn = QPushButton("이용 시간") #이용시간 버튼 객체 추가
        self.useTime_btn.setStyleSheet(bt_styles)
        btnSetLayout.addWidget(self.useTime_btn) #버튼집합 레이아웃에 버튼 추가
        self.useTime_btn.setFixedWidth(90)
        
        self.enter_btn = QPushButton("출입 안내") #버튼 객체 추가
        self.enter_btn.setStyleSheet(bt_styles)
        btnSetLayout.addWidget(self.enter_btn)
        self.enter_btn.setFixedWidth(90)
        
        self.infra_btn = QPushButton("시설 안내")
        self.infra_btn.setStyleSheet(bt_styles)
        btnSetLayout.addWidget(self.infra_btn)
        self.infra_btn.setFixedWidth(90)
        
        self.studyHelp_btn = QPushButton("연구학습지원")
        self.studyHelp_btn.setStyleSheet(bt_styles)
        btnSetLayout.addWidget(self.studyHelp_btn)
        self.studyHelp_btn.setFixedWidth(90)
        
        self.findWay_btn = QPushButton("오시는 길") 
        self.findWay_btn.setStyleSheet(bt_styles)
        btnSetLayout.addWidget(self.findWay_btn)
        self.findWay_btn.setFixedWidth(90)
        
        
        return btnSetLayout #버튼 집합 레이아웃 반환
    
    #시작하자 마자 뜨는 이용 방법 텍스트 라벨 반환 함수
    def startText(self):
        startText1 = QLabel('안녕하세요')
        startText1.setFont(QFont('굴림',10))
        startText1.setStyleSheet(lb_styles) #라벨 꾸미기 
        input_width = startText1.fontMetrics().boundingRect( '안녕하세요' ).width()+10
        startText1.setFixedWidth(input_width)
        
        txt = '원하시는 버튼을 클릭해주세요.\n채팅으로 검색하셔도 됩니다.'
        startText2 = QLabel(txt)
        startText2.setFont(QFont('굴림',10))
        startText2.setStyleSheet(lb_styles)
        input_width = startText2.fontMetrics().boundingRect( '원하시는 버튼을 클릭해주세요.' ).width()+10
        startText2.setFixedWidth(input_width)
        
        txt='도서검색을 하시려면 앞에 !를 붙여주세요.'
        startText3 = QLabel(txt)
        startText3.setFont(QFont('굴림',10))
        startText3.setStyleSheet(lb_styles)
        input_width = startText3.fontMetrics().boundingRect( txt ).width()+10
        startText3.setFixedWidth(input_width)
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
    centerLayout = QVBoxLayout()
    lb_styles = ("color : black;" #라벨 꾸미기
                  "border-style: solid;"
                  "border-width: 1px;"
                  "border-color: black;"
                  "border-radius: 2px;"
                  #"background-color: #CEF6E3;"
                  "background-color:#D5E8F6;"
                  #"color: #C0DDEE;"
                )
    bt_styles = (#"background-color: #D5D5F2;" #버튼 꾸미기
                 "background-color: white;" 
                 "border-color: #5215E3;"
                 "color: #1212DD;"
                 "border-style: solid;"
                 #"border-radius: 1px;"
                 "border-width: 1px;"
                )
    app = QApplication(sys.argv)
    ex = MyApp()
    start = ex.startMessage()
    sys.exit(app.exec_())
    
    
