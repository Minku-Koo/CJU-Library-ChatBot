# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot
# developer E-mail : corleone@kakao.com

from urllib.request import urlopen
#from urllib.parse   import quote # for URL 한글 인코딩
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from cjubot_library import *
from PyQt5.QtCore import QDate, Qt # QT 날짜 모듈



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
            

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CJU Library ChatBot') #GUI 제목
        self.setWindowIcon(QIcon('mtd_logo.PNG')) #아이콘 설정, 16x16, PNG 파일
        #self.move(600, 300) #화면에서의 위치
        #self.resize(550, 800) #어플의 크기
        self.setFixedSize(550, 800)  #창 크기 고정
        self.center() #위치를 화면 중앙에 배치 
        #self.setGeometry(600, 300, 400, 300) /  move + resize 합친것
        
        
        #btn1 = QPushButton("버튼 시도", self) #버튼 객체 추가
        #btn1.move(10,15) #화면에서 버튼 위치
        #btn1.clicked.connect(self.btn1_click)
        
        #btn2 = QPushButton("버튼TWO", self)
        #btn2.move(115,15)
        
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
        self.lb_center.setAlignment(Qt.AlignCenter)
        self.lb_center.setStyleSheet("color : black;" #라벨 꾸미기
                              #"border-style: solid;"
                              #"border-width: 2px;"
                              #"border-color: black;"
                              #"border-radius: 2px;"
                              #"background-color: white;"
                            )
        
        self.lb_bottom = QLabel()
        #lb_bottom.setAlignment(Qt.AlignBottom)
        self.lb_bottom.setMaximumSize(55000,80) #라벨 최대사이즈
        self.lb_bottom.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: black;"
                              #"border-radius: 2px;"
                              "background-color: green;"
                            )
        
        
        #chatBox = QVBoxLayout() #수직 박스 레이아웃
        #chatBox.addWidget(lb_head)
        #chatBox.addStretch(1) #빈공간 설정
        
        #레이아웃에 라벨 추가
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(lb_head)
        self.mainLayout.addWidget(self.lb_center)
        self.mainLayout.addWidget(self.lb_bottom)
        
        self.setLayout(self.mainLayout) #main layout
        #self.layout_1.addWidget(self.lb_head, alignment=Qt.AlignTop)
        
        
        self.show() #화면에 표시
        
    def center(self): #어플을 화면 중심에 위치시키는 함수
        qr = self.frameGeometry() #창의 위치 크기 정보 불러옴
        cp = QDesktopWidget().availableGeometry().center() #화면 가운데 위치 식별
        qr.moveCenter(cp) #화면 중심으로 이동
        self.move(qr.topLeft())
        
    def btn1_click(self): #btn1 클릭이벤트
        print("button click")
    
    def useTime_click(self): #btn1 클릭이벤트
        print("use time button click")
    
    def findWay_click(self):
        print("findWay_click button click")
    
    #시작하자마자 뜨는 메시지
    def startMessage(self):
        print('start')
        startText1 = QLabel('안녕하세요')
        startText1.setMaximumSize(150,30)
        startText1.setFont(QFont('굴림',11))
        startText1.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        
        startText2 = QLabel('원하시는 버튼을 클릭해주세요.\n채팅으로 검색하셔도 됩니다.')
        startText2.setMaximumSize(260,40)
        startText2.setFont(QFont('굴림',11))
        startText2.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        
        self.btnSetLabel = QLabel()
        btnSetLayout = QHBoxLayout()
        
        self.useTime_btn = QPushButton("이용 시간", self) #이용시간 버튼 객체 추가
        self.useTime_btn.clicked.connect(self.useTime_click)
        btnSetLayout.addWidget(self.useTime_btn)
        
        self.findWay_btn = QPushButton("찾아오는 길", self) #찾아오는 길 버튼 객체 추가
        self.findWay_btn.clicked.connect(self.findWay_click)
        btnSetLayout.addWidget(self.findWay_btn)
        
        
        centerLayout = QVBoxLayout()
        centerLayout.addWidget(startText1)
        centerLayout.addWidget(startText2)
        
        #self.btnSetLabel.setLayout(btnSetLayout)
        btnSetLayout.setAlignment(Qt.AlignLeft)
        centerLayout.addLayout(btnSetLayout)  #레이아웃 추가  !!!!!!
        #centerLayout.addWidget(btnSetLayout)
        
        centerLayout.setAlignment(Qt.AlignTop)
        
        self.lb_center.setLayout(centerLayout)
        

if __name__ == '__main__':
    print("open app")
    #bookSearch('')
    app = QApplication(sys.argv)
    ex = MyApp()
    start = ex.startMessage()
    sys.exit(app.exec_())
    
    
