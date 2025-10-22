import sqlite3
import random

class ProductDB:
    def __init__(self):
        self.conn = sqlite3.connect('MyProduct.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            productID INTEGER PRIMARY KEY,
            productName TEXT,
            productPrice INTEGER
        )''')
        self.conn.commit()

    def insert_product(self, product_name, price):
        self.cursor.execute('''
        INSERT INTO Products (productName, productPrice)
        VALUES (?, ?)''', (product_name, price))
        self.conn.commit()

    def update_product(self, product_id, product_name, price):
        self.cursor.execute('''
        UPDATE Products 
        SET productName = ?, productPrice = ?
        WHERE productID = ?''', (product_name, price, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cursor.execute('DELETE FROM Products WHERE productID = ?', (product_id,))
        self.conn.commit()

    def select_all_products(self):
        self.cursor.execute('SELECT * FROM Products')
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

def generate_sample_data():
    db = ProductDB()
    
    # 전자제품 이름 리스트
    products = ['스마트폰', '노트북', '태블릿', 'TV', '냉장고', '세탁기', '에어컨', '청소기', '전자레인지', '공기청정기']
    
    # 10만개의 샘플 데이터 생성
    for i in range(100000):
        product_name = f"{random.choice(products)}_{i}"
        price = random.randint(100000, 2000000)
        db.insert_product(product_name, price)
    
    print("100,000개의 샘플 데이터가 생성되었습니다.")
    
    # 데이터 확인을 위한 샘플 조회
    print("\n처음 5개의 제품 데이터:")
    results = db.select_all_products()
    for i in range(5):
        print(results[i])
    
    db.close_connection()

if __name__ == "__main__":
    generate_sample_data()