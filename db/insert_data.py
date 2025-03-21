#csvファイルに保存したデータをデータベースのProductテーブルに挿入

import csv
from sqlalchemy.orm import Session
from .mymodels import Product
from .database import engine

# CSVファイルのパス
csv_file_path = "vegetable_products_jp.csv"

# データベースへのセッションを作成
session = Session(bind=engine)

# CSVファイルを開いて読み込む
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

# セッションを閉じる
session.close()
