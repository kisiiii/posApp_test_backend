#python -m db.insert_data で実行してください。直接実行するとインポートエラーがでます

import csv
from sqlalchemy.orm import Session
from .mymodels import Product, Tax
from .database import engine

# データベースへのセッションを作成
session = Session(bind=engine)

# CSVデータをDBに挿入
csv_file_path = "vegetable_products_jp.csv"
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Productオブジェクトを作成
        product = Product(
            CODE=row['CODE'],
            NAME=row['NAME'],
            PRICE=int(row['PRICE'])
        )
        # データベースに追加
        session.add(product)
# データをコミットして保存
session.commit()


# 消費税情報をDBに追加
new_tax = Tax(ID=1, CODE=10, NAME="10%", PERCENT=0.10)
session.add(new_tax)
session.commit()

# セッションを閉じる
session.close()

print("データが挿入されました。")