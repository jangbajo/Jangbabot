import sys
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QMessageBox
import pymysql
#from pyqt5_plugins.examplebuttonplugin import QtGui

mylocalhost = ''
myuser = ''
mypasswd = ''
mydb = 'jangba_db'

wait_form_class = uic.loadUiType("/home/pi/work/UI/ui/waitPro.ui")[0]
select_form_class = uic.loadUiType("/home/pi/work/UI/ui/selectPro.ui")[0]
confirm_form_class = uic.loadUiType("/home/pi/work/UI/ui/confirmPro.ui")[0]
find_form_class = uic.loadUiType("/home/pi/work/UI/ui/findPro.ui")[0]
complete_form_class = uic.loadUiType("/home/pi/work/UI/ui/completePro.ui")[0]

global screen
global selectScreen
global goods_count
select_count = 0
goods_list = []  # 상품 리스트
goods_num = [0]
goods_order = [0] # 상품 순서


# waitGoods screen
class waitWindowClass(QMainWindow, wait_form_class):

    def __init__(self):
        super().__init__()

        # db 세팅후 db값 불러오기
        SelectData()

        self.setupUI()
        self.setFixedSize(QSize(800, 430))  # 창크기 고정

        self.show()

    def setupUI(self):

        self.setupUi(self)
        self.setWindowTitle("waitGoods")

        pixmap = QPixmap('/home/pi/work/UI/src/wait2.png')
        self.backLabel.setPixmap(pixmap)

    def mouseButtonKind(self, buttons):
        check = 0

        if buttons & Qt.LeftButton:
            print('LEFT')
            check = 1
        if buttons & Qt.MidButton:
            print('MIDDLE')
            check = 1
        if buttons & Qt.RightButton:
            print('RIGHT')
            check = 1

        return check

    def mousePressEvent(self, e):
        global selectScreen          # 화인 화면 창에서 이전 창(선택 화면) 보이게 해야해서

        if(self.mouseButtonKind(e.buttons()) == 1):
            print("창 넘어감")
            self.close()
            selectScreen = SelectWindowClass()

    def __del__(self):
        print("WaitWindowClass 객체 삭제")


# selectGoods screen
class SelectWindowClass(QMainWindow, select_form_class):

    minus_btn = [0]
    plus_btn = [0]

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setFixedSize(QSize(800, 430))  # 창크기 고정

        self.GObtn.clicked.connect(self.gobtnClick)
        self.BACKbtn.clicked.connect(self.backbtnClick)

        for x in range(goods_count):
            self.minus_btn[x + 1].clicked.connect(lambda stat="False", n=x + 1: self.minusbtnClick(n))
            self.plus_btn[x + 1].clicked.connect(lambda stat="False", n=x + 1: self.plusbtnClick(n))

        self.show()

    def setupUI(self):

        self.setupUi(self)
        self.setWindowTitle("selectGoods")

        # 상품 목록 만들기
        self.goodstableWidget.setRowCount(goods_count)  # 행 개수
        #        self.goodstableWidget.setColumnCount(4)         # 열 개수
        #        self.goodstableWidget.setHorizontalHeaderLabels(['상품명'])    # 행 헤더 변경

        for x in range(goods_count):
            if (int(goods_list[x + 1][3]) == 0):  # 상품 재고수가 없을 경우
                # 상품명 세팅
                state = "(sold out)"  # 상품명에 품절 표시
                self.goodstableWidget.setItem(x, 0, QTableWidgetItem('   ' + goods_list[x + 1][1] + '   ' + state))
                self.goodstableWidget.item(x, 0).setBackground(QtGui.QColor(200, 200, 200))     # 배경색 변경
                self.goodstableWidget.item(x, 0).setForeground(QtGui.QColor(200, 10, 10))       # 글자색 변경
                # 감소 버튼 세팅
                self.minus_btn.insert(x + 1, QPushButton('-'))
                self.minus_btn[x + 1].setDisabled(True)
                self.goodstableWidget.setCellWidget(x, 1, self.minus_btn[x + 1])
                # 상품 수 세팅
                goods_num.insert(x + 1, '0')
                goods_num_text = QTableWidgetItem(goods_num[x + 1])
                goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(x, 2, goods_num_text)
                self.goodstableWidget.item(x, 2).setBackground(QtGui.QColor(200, 200, 200))     # 배경색 변경
                # 추가 버튼 세팅
                self.plus_btn.insert(x + 1, QPushButton('+'))
                self.plus_btn[x + 1].setDisabled(True)
                self.goodstableWidget.setCellWidget(x, 3, self.plus_btn[x + 1])


            else:                               # 상품 재고수가 있을 경우
                # 상품명 세팅
                self.goodstableWidget.setItem(x, 0, QTableWidgetItem('   ' + goods_list[x + 1][1]))
                # 감소 버튼 세팅
                self.minus_btn.insert(x + 1, QPushButton('-'))
                self.goodstableWidget.setCellWidget(x, 1, self.minus_btn[x + 1])
                # 상품 수 세팅
                goods_num.insert(x + 1, '0')
                temp = goods_num[x + 1]
                goods_num_text = QTableWidgetItem(temp)
                goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(x, 2, goods_num_text)
                # 추가 버튼 세팅
                self.plus_btn.insert(x + 1, QPushButton('+'))
                self.goodstableWidget.setCellWidget(x, 3, self.plus_btn[x + 1])
        print(self.goodstableWidget.width())
        self.goodstableWidget.setColumnWidth(0, int(self.goodstableWidget.width() * 15 / 25))
        self.goodstableWidget.setColumnWidth(1, int(self.goodstableWidget.width() * 2 / 25))
        self.goodstableWidget.setColumnWidth(2, int(self.goodstableWidget.width() * 4 / 25))
        self.goodstableWidget.setColumnWidth(3, int(self.goodstableWidget.width() * 2 / 25))
        self.goodstableWidget.resizeRowsToContents()

    def plusbtnClick(self, n):
        print(n, "+버튼이 클릭되었습니다.\n")
        if ((int(goods_list[n][3]) - int(goods_num[n])) > 0):
            goods_num[n] = str(int(goods_num[n]) + 1)
            print(n, goods_num[n], "\n")

            goods_num_text = QTableWidgetItem(goods_num[n])
            goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
            self.goodstableWidget.setItem(n - 1, 2, goods_num_text)
        else:
            inform = "out of stock !\n( only " + str(goods_list[n][3]) + " )"
            QMessageBox.information(self, 'Information', inform)

    def minusbtnClick(self, n):
        print(n, "-버튼이 클릭되었습니다.\n")
        if (int(goods_num[n]) > 0):
            goods_num[n] = str(int(goods_num[n]) - 1)
            print(n, goods_num[n], "\n")

            goods_num_text = QTableWidgetItem(goods_num[n])
            goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
            self.goodstableWidget.setItem(n - 1, 2, goods_num_text)

    # 상품 선택 후, Go버튼 누르면
    def gobtnClick(self):
        global select_count

        print("go버튼 클릭\n")
        select_count = 0
        if (select_count == 0):                     # 최종 선택에서만 구매 항목 수 저장
            for x in range(goods_count):
                if(int(goods_num[x + 1]) > 0):
                    print(x)
                    select_count += 1

        if (select_count == 0):
            inform = "상품을 선택해주세요 !"
            QMessageBox.information(self, 'Information', inform)

        else:
            self.close()
            self.go = ConfirmWindowClass()

    def backbtnClick(self):
        self.close()
        screen.show()

    def __del__(self):
        print("SelectWindowClass 객체 삭제")


# confirmGoods screen
class ConfirmWindowClass(QMainWindow, confirm_form_class):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setFixedSize(QSize(800, 430))  # 창크기 고정

        self.NObtn.clicked.connect(self.nobtnClick)
        self.YESbtn.clicked.connect(self.yesbtnClick)

        self.show()

    def setupUI(self):

        self.setupUi(self)
        self.setWindowTitle("confirmGoods")

        # 상품 목록 만들기
        print(goods_count, '\n')
        print('행', select_count)
        self.goodstableWidget.setRowCount(select_count)  # 행 개수
        #        self.goodstableWidget.setColumnCount(4)         # 열 개수
        #        self.goodstableWidget.setHorizontalHeaderLabels(['상품명'])    # 행 헤더 변경

        row = 0
        for x in range(goods_count):
            if (int(goods_num[x + 1]) > 0):
                # 상품명 세팅
                self.goodstableWidget.setItem(row, 0, QTableWidgetItem('   ' + goods_list[x + 1][1]))
                # 상품 수 세팅
                goods_num_text = QTableWidgetItem(str(goods_num[x + 1]) + '개')
                goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(row, 1, goods_num_text)
                row += 1

        self.goodstableWidget.setColumnWidth(0, int(self.goodstableWidget.width() * 5 / 7))
        self.goodstableWidget.setColumnWidth(1, int(self.goodstableWidget.width() * 1 / 7))
        self.goodstableWidget.resizeRowsToContents()

    def nobtnClick(self):
        self.close()
        selectScreen.show()

    def yesbtnClick(self):
        print("yes버튼 클릭\n")
        self.close()

# 상품 찾는 중 창
#        self.yes = FindWindowClass()

# 구매 완료 창
        self.yes = CompleteWindowClass()


    def __del__(self):
        print("ConfirmWindowClass 객체 삭제")

# findGoods screen
class FindWindowClass(QMainWindow, find_form_class):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setFixedSize(QSize(800, 430))  # 창크기 고정

        self.show()

    def setupUI(self):

        self.setupUi(self)
        self.setWindowTitle("findGoods")

        pixmap = QPixmap('/home/pi/work/UI/src/find2.png')
        self.backLabel.setPixmap(pixmap)
#        self.goodstableWidget.setGeometry(310, 750, 475, 260)


        # 상품 목록 만들기
        self.goodstableWidget.setRowCount(select_count)  # 행 개수
        #        self.goodstableWidget.setColumnCount(4)         # 열 개수
        #        self.goodstableWidget.setHorizontalHeaderLabels(['상품명'])    # 행 헤더 변경

        row = 0
        for x in range(goods_count):
            if (int(goods_num[x + 1]) > 0):
                # 상품명 세팅
                self.goodstableWidget.setItem(row, 0, QTableWidgetItem('   ' + goods_list[x + 1][1]))
                # 상품 수 세팅
                goods_num_text = QTableWidgetItem(str(goods_num[x + 1]) + '개')
                goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(row, 1, goods_num_text)
                row += 1

        self.goodstableWidget.setColumnWidth(0, int(self.goodstableWidget.width() * 5 / 7))
        self.goodstableWidget.setColumnWidth(1, int(self.goodstableWidget.width() * 1 / 7))
        self.goodstableWidget.resizeRowsToContents()

    def __del__(self):
        print("FindWindowClass 객체 삭제")


# completeGoods screen
class CompleteWindowClass(QMainWindow, complete_form_class):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setFixedSize(QSize(800, 430))  # 창크기 고정

        self.OKbtn.clicked.connect(self.okbtnClick)
        self.show()

    def setupUI(self):

        total_price = 0

        self.setupUi(self)
        self.setWindowTitle("completeGoods")

        # 상품 목록 만들기
        self.goodstableWidget.setRowCount(select_count)  # 행 개수
        #        self.goodstableWidget.setColumnCount(4)         # 열 개수
        #        self.goodstableWidget.setHorizontalHeaderLabels(['상품명'])    # 행 헤더 변경

        row = 0
        for x in range(goods_count):
            if (int(goods_num[x + 1]) > 0):
                # 상품명 세팅
                self.goodstableWidget.setItem(row, 0, QTableWidgetItem('   ' + goods_list[x + 1][1]))
                # 상품 수 세팅
                goods_num_text = QTableWidgetItem(str(goods_num[x + 1]) + '개')
                goods_num_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(row, 1, goods_num_text)
                # 상품 금액 세팅
                price = int(goods_list[x + 1][4]) * int(goods_num[x + 1])
                total_price += price
                goods_price_text = QTableWidgetItem(str(price) + '원')
                goods_price_text.setTextAlignment(Qt.AlignCenter)  # 가운데 정렬
                self.goodstableWidget.setItem(row, 2, goods_price_text)
                row += 1

        # 총 금액 표시
        total_price_text = '총  ' + str(total_price) + '원       '
        self.totalprice.setText(total_price_text)
        self.totalprice.setAlignment(Qt.AlignRight)                             # 오른쪽 정렬
        self.totalprice.setStyleSheet("background-color: rgb(200, 200, 200);")  # 배경색 변경


        self.goodstableWidget.setColumnWidth(0, int(self.goodstableWidget.width() * 5 / 9))
        self.goodstableWidget.setColumnWidth(1, int(self.goodstableWidget.width() * 1 / 9))
        self.goodstableWidget.setColumnWidth(2, int(self.goodstableWidget.width() * 2 / 9))
        self.goodstableWidget.resizeRowsToContents()

    def okbtnClick(self):
        global screen

        print("ok버튼 클릭\n")
        manageStock()
        self.close()

        del screen
        screen = waitWindowClass()

    def __del__(self):
        print("CompleteWindowClass 객체 삭제")



# DB 연결 확인
def ConnDB():
    # mysql db 파일 접속, 없으면 생성
    conn = pymysql.connect(host=mylocalhost , user=myuser, password=mypasswd,
                           db=mydb, charset='utf8'
                           )
    cur = conn.cursor()

    # db테이블에서 정보 조회
    sql = "SELECT * FROM GoodsInfo_table"
    cur.execute(sql)
    rows = cur.fetchall()

    # 테이블이 없으면 새로 생성
    if not rows:
        print("DB 연결 실패")
        sql = "CREATE TABLE GoodsInfo_table(barcodeID int(10) not null auto_increment, goodsName VARCHAR(20) not null, section int(10) not null, stock int(10) not null, price int(10) not null, primary key(barcodeID))"
        cur.execute(sql)
        conn.commit()

    else:
        print("DB 연결 성공")
        print(rows)

    conn.close()


# DB data 추출
def SelectData():
    global goods_count
    # 데이터베이스 내부 테이블의 내용을 모두 추출
    conn = pymysql.connect(host=mylocalhost, user=myuser, password=mypasswd,
                           db=mydb, charset='utf8'
                           )

    cur = conn.cursor()

    # 테이블 column이름 저장
    sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'jangba_db' AND TABLE_NAME = 'GoodsInfo_table';"
    cur.execute(sql)
    rows = cur.fetchall()
    count = len(rows)
    column = ()
    print(rows)
    for x in range(count):
        column = column + rows[x]
    print(column)
    goods_list.insert(0, column)

    sql = "SELECT * FROM GoodsInfo_table"
    cur.execute(sql)
    rows = cur.fetchall()

    conn.close()

    # 각 튜플에 data값 저장
    goods_count = len(rows)
    for x in range(goods_count):
        goods_list.insert(x + 1, rows[x])


# DB data 추출
def manageStock():

    # 데이터베이스 내부 테이블의 내용을 모두 추출
    conn = pymysql.connect(host=mylocalhost, user=myuser, password=mypasswd,
                           db=mydb, charset='utf8',  # 한글처리 (charset = 'utf8')
                           )

    cur = conn.cursor()

    for x in range(goods_count):
        if (int(goods_num[x + 1]) > 0):
            goodsName = str(goods_list[x + 1][1])
            goodsnum = str(goods_num[x + 1])
            sql = "update GoodsInfo_table set stock = stock - "+goodsnum+" where goodsName = '" +goodsName+ "';"
            cur.execute(sql)
            conn.commit()
            print(goodsName+"재고수 -"+goodsnum)

    conn.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # db 세팅
    ConnDB()

    screen = waitWindowClass()
    screen.show()

    app.exec_()
    del screen
