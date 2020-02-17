# 2020.02.12 project start
# made by Koo Minku
# CJU Library ChatBot

from urllib.request import urlopen
#from urllib.parse   import quote # for URL 한글 인코딩
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from cjubot_library import *


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
            

#bookSearch('')
class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CJU Library ChatBot') #GUI 제목
        self.setWindowIcon(QIcon('mtd_logo.PNG')) #아이콘 설정, 16x16, PNG 파일
        self.move(600, 300) #화면에서의 위치
        self.resize(400, 300) #어플의 크기
        #self.setGeometry(600, 300, 400, 300) /  move + resize 합친것
        
        btn1 = QPushButton("버튼 시도", self) #버튼 객체 추가
        btn1.move(10,15) #화면에서 버튼 위치
        
        btn2 = QPushButton("버튼TWO", self)
        btn2.move(115,15) 
        
        
        self.show() #화면에 표시

if __name__ == '__main__':
    print("open app")
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

    
