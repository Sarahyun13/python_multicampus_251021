import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic 
import sqlite3
import os.path 

# 데이터베이스 작업을 담당하는 클래스
class DatabaseManager:
    def __init__(self, db_path="ProductList.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        self._ensure_table()

    def _ensure_table(self):
        # 테이블이 없으면 생성
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Products (id integer primary key autoincrement, Name text, Price integer);"
        )
        self.conn.commit()

    def add(self, name, price):
        self.cur.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
        self.conn.commit()

    def update(self, prod_id, name, price):
        self.cur.execute("UPDATE Products SET Name=?, Price=? WHERE id=?;", (name, price, prod_id))
        self.conn.commit()

    def remove(self, prod_id):
        self.cur.execute("DELETE FROM Products WHERE id=?;", (prod_id,))
        self.conn.commit()

    def list_all(self):
        self.cur.execute("SELECT * FROM Products;")
        return self.cur.fetchall()

    def close(self):
        try:
            self.conn.close()
        except:
            pass

# 디자인 파일을 로딩
form_class = uic.loadUiType("ProductList3.ui")[0]

class Window(QMainWindow, form_class):
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.setupUi(self)
        self.db = db_manager

        #초기값 셋팅 
        self.id = 0 
        self.name = ""
        self.price = 0 

        #QTableWidget의 컬럼폭 셋팅하기 
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        #QTableWidget의 헤더 셋팅하기
        self.tableWidget.setHorizontalHeaderLabels(["제품ID","제품명", "가격"])
        #탭키로 네비게이션 금지 
        self.tableWidget.setTabKeyNavigation(False)

        # 엔터키로 다음 컨트롤로 이동
        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())

        # 더블클릭 시그널 처리
        self.tableWidget.doubleClicked.connect(self.doubleClick)

        # (선택) UI에 버튼이 있으면 연결 — 존재하는 경우에만 연결하도록 안전하게 처리
        if hasattr(self, "btnAdd"):
            self.btnAdd.clicked.connect(self.addProduct)
        if hasattr(self, "btnUpdate"):
            self.btnUpdate.clicked.connect(self.updateProduct)
        if hasattr(self, "btnRemove"):
            self.btnRemove.clicked.connect(self.removeProduct)

        # 초기 데이터 로드
        self.getProduct()

    def addProduct(self):
        self.name = self.prodName.text()
        self.price = self.prodPrice.text() or "0"
        # 가격을 정수로 시도 변환 (유효성 검사 간단 처리)
        try:
            price_int = int(self.price)
        except ValueError:
            price_int = 0
        self.db.add(self.name, price_int)
        self.getProduct()

    def updateProduct(self):
        self.id  = self.prodID.text()
        self.name = self.prodName.text()
        self.price = self.prodPrice.text() or "0"
        try:
            id_int = int(self.id)
        except ValueError:
            return
        try:
            price_int = int(self.price)
        except ValueError:
            price_int = 0
        self.db.update(id_int, self.name, price_int)
        self.getProduct()

    def removeProduct(self):
        self.id  = self.prodID.text() 
        try:
            id_int = int(self.id)
        except ValueError:
            return
        self.db.remove(id_int)
        self.getProduct()

    def getProduct(self):
        # 기존 내용 삭제
        self.tableWidget.clearContents()
        items = self.db.list_all()
        self.tableWidget.setRowCount(len(items))
        row = 0 
        for item in items:
            # item: (id, Name, Price)
            itemID = QTableWidgetItem(str(item[0]))
            itemID.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(row, 0, itemID)

            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(item[1])))

            itemPrice = QTableWidgetItem(str(item[2]))
            itemPrice.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(row, 2, itemPrice)

            row += 1

    def doubleClick(self):
        # 테이블에서 선택한 행의 값을 폼으로 옮김
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        id_item = self.tableWidget.item(row, 0)
        name_item = self.tableWidget.item(row, 1)
        price_item = self.tableWidget.item(row, 2)
        if id_item:
            self.prodID.setText(id_item.text())
        if name_item:
            self.prodName.setText(name_item.text())
        if price_item:
            self.prodPrice.setText(price_item.text())


# 인스턴스를 생성한다.
app = QApplication(sys.argv)
dbm = DatabaseManager("ProductList.db")
myWindow = Window(dbm)
myWindow.show()

# 앱 종료 시 DB 닫기
app.aboutToQuit.connect(dbm.close)

app.exec_()



