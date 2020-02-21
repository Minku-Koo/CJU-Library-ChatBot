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
        self.lb_center.setMaximumSize(550,660) #라벨 최대사이즈
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
        #lb_center 라벨에 스크롤 설정
        scroll = QScrollArea()
        scroll.setWidget(self.lb_center)
        scroll.setFixedHeight(660)
        scroll.setWidgetResizable(True)
        
        #레이아웃에 라벨 추가
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(lb_head)
        self.mainLayout.addWidget(scroll) #라벨 말고 qscrollarea를 입력해야함
        self.mainLayout.addWidget(self.lb_bottom)
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
        
    def btn1_click(self): #btn1 클릭이벤트
        print("button click")
    
    
    def referenceRoom_click(self): 
        print("제1~3자료실")
        self.useTime_click()
        
    def studyRoom_click(self): 
        print("스터디룸")
        self.useTime_click()
        
    def notebookRoom_click(self): 
        print("노트북 열람실")
        self.useTime_click()
        
    def mulitmedia_click(self): 
        print("멀티미디어 감상실")
        self.useTime_click()
        
    def readingRoom_click(self): 
        print("제 1~3 열람실")
        self.useTime_click()
        
    def infoRounge_click(self): 
        print("정보검색라운지")
        self.useTime_click()
        
    def copyPrint_click(self): 
        print("복사/출력실")
        self.useTime_click()
        
    def start_btn_click(self):
        print('처음으로')
        self.startMessage() #최초 출력 함수 
    
    def useTime_click(self): #이용시간 클릭 하면 나타나는 레이아웃
        print("use time button click")
        #이용시간 메뉴 텍스트 설정
        useTimeText1 = QLabel('이용을 원하시는 시설을 클릭해주세요.')
        useTimeText1.setMaximumSize(330,30)
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
        
        self.mulitmedia = QPushButton("멀티미디어 감상실", self) #버튼 객체 추가
        self.mulitmedia.clicked.connect(self.mulitmedia_click)
        
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
        useTimeLayout.addWidget(self.mulitmedia, 0, 3)
        useTimeLayout.addWidget(self.readingRoom, 1, 0)
        useTimeLayout.addWidget(self.infoRounge, 1, 1)
        useTimeLayout.addWidget(self.copyPrint, 1, 2)
        useTimeLayout.addWidget(self.start_btn, 1, 3)
        
        useTimeLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 이용시간 버튼 집합 레이아웃 추가
        centerLayout.addLayout(useTimeLayout)
    
    def findWay_click(self):
        print("findWay_click button click")
        
        
    def enter_click(self):#출입 안내
        print("enter_click button click")
        #이용시간 메뉴 텍스트 설정
        txt1 = '도서관 출입문에 출입통제시스템이 설치되어\n'
        txt2 = '학생증 또는 모바일 이용증이 있어야 출입 할 수 있으니\n도서관에 올 때는 학생증을 지참하여야 합니다.'
        findWayText1 = QLabel(txt1 + txt2) # 텍스트 합쳐서 입력
        findWayText1.setMaximumSize(450,100)
        findWayText1.setFont(QFont('굴림',10))
        findWayText1.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        findWayText2 = QLabel('<출입방법>\n입구통제기의 스캐너에 학생증(모바일 이용증) 스캐닝 → 녹색램프 → 입장')
        findWayText2.setMaximumSize(520,60)
        findWayText2.setFont(QFont('굴림',9))
        findWayText2.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
                            
        centerLayout.addWidget(findWayText1) #레이아웃에 텍스트 입력
        centerLayout.addWidget(findWayText2)
        
        centerLayout.setAlignment(Qt.AlignTop)
        #centerlayout에 출입안내 버튼 집합 레이아웃 추가
        self.startMessage() #최초 출력 함수 
        
    def studyHelp_click(self):
        print("studyHelp_click button click")
        
    def infra_click(self): #시설 안내
        print("infra_click button click")


    #시작하자마자 뜨는 메시지
    def startMessage(self):
        print('start')
        '''
        self.startText1 = QLabel('안녕하세요')
        self.startText1.setMaximumSize(150,30)
        self.startText1.setFont(QFont('굴림',11))
        self.startText1.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        
        self.startText2 = QLabel('원하시는 버튼을 클릭해주세요.\n채팅으로 검색하셔도 됩니다.')
        self.startText2.setMaximumSize(260,50)
        self.startText2.setFont(QFont('굴림',11))
        self.startText2.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        
        #self.btnSetLabel = QLabel()  # 버튼 집합 라벨 설정
        btnSetLayout = QHBoxLayout() # 버튼 집합 레이아웃 설정
        
        self.useTime_btn = QPushButton("이용 시간", self) #이용시간 버튼 객체 추가
        self.useTime_btn.clicked.connect(self.useTime_click)
        btnSetLayout.addWidget(self.useTime_btn)
        
        self.enter_btn = QPushButton("출입 안내", self) #찾아오는 길 버튼 객체 추가
        self.enter_btn.clicked.connect(self.enter_click)
        btnSetLayout.addWidget(self.enter_btn)
        
        self.infra_btn = QPushButton("시설 안내", self)
        self.infra_btn.clicked.connect(self.infra_click)
        btnSetLayout.addWidget(self.infra_btn)
        
        self.studyHelp_btn = QPushButton("연구학습지원", self) 
        self.studyHelp_btn.clicked.connect(self.studyHelp_click)
        btnSetLayout.addWidget(self.studyHelp_btn)
        
        self.findWay_btn = QPushButton("오시는 길", self) 
        self.findWay_btn.clicked.connect(self.findWay_click)
        btnSetLayout.addWidget(self.findWay_btn)
        '''
        """
        self.centerLayout = QVBoxLayout()
        start_set = starter()
        print('12')
        #self.centerLayout = QVBoxLayout() ###
        self.centerLayout.addWidget(start_set.startText()[0])
        self.centerLayout.addWidget(start_set.startText()[1])
        
        start_set.startMsg().setAlignment(Qt.AlignLeft)
        self.centerLayout.addLayout(start_set.startMsg())  #레이아웃 추가  !!!!!!
        
        start_set.useTime_btn.clicked.connect(self.useTime_click)
        start_set.enter_btn.clicked.connect(self.enter_click)
        start_set.infra_btn.clicked.connect(self.infra_click)
        # 버튼 event클래스 추가
        """
        
        start_set = starter() #스타터 클래스 불러옴
        #중앙 라벨에 centerlayout을 레이아웃으로 설정
        self.lb_center.setLayout(start_set.start_def())
        print('-=66-=')
        #메뉴 버튼에 클릭 이벤트 설정
        start_set.useTime_btn.clicked.connect(self.useTime_click)
        start_set.enter_btn.clicked.connect(self.enter_click)
        start_set.infra_btn.clicked.connect(self.infra_click)
        start_set.findWay_btn.clicked.connect(self.findWay_click)
        start_set.studyHelp_btn.clicked.connect(self.studyHelp_click)
        

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
        startText2.setMaximumSize(260,50)
        startText2.setFont(QFont('굴림',11))
        startText2.setStyleSheet("color : black;" #라벨 꾸미기
                              "border-style: solid;"
                              "border-width: 1px;"
                              "border-color: black;"
                              "border-radius: 2px;"
                              "background-color: #CEF6E3;"
                            )
        #텍스트 라벨 2개를 리스트 형태로 반환
        return [startText1, startText2]
    
    #스타터 클래스 메인 함수 / 위 2개 함수를 활용하여 최초 출력 레이아웃 반환
    def start_def(self):
        #텍스트 라벨 추가
        centerLayout.addWidget(self.startText()[0])
        centerLayout.addWidget(self.startText()[1])
        
        #메뉴 버튼 집합 레이아웃 추가
        centerLayout.addLayout(self.startMsg())  #레이아웃 추가  !!!!!!
        centerLayout.setAlignment(Qt.AlignTop)
        # 최초 출력 레이아웃 반환
        return centerLayout

if __name__ == '__main__':
    print("open app")
    #bookSearch('')
    centerLayout = QVBoxLayout()
    
    app = QApplication(sys.argv)
    ex = MyApp()
    start = ex.startMessage()
    sys.exit(app.exec_())
    
    
