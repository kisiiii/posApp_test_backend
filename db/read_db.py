#データベースの中身を確認

from sqlalchemy.orm import Session
from .database import engine
from .mymodels import Product, Tax, Transaction, TransactionDetail

def fetch_all_data():
    with Session(engine) as session:
        # Productテーブルの全データを取得
        products = session.query(Product).all()
        print("Products:")
        for product in products:
            print(f"ID: {product.PRD_ID}, CODE: {product.CODE}, NAME: {product.NAME}, PRICE: {product.PRICE}")

        # Taxテーブルの全データを取得
        taxes = session.query(Tax).all()
        print("\nTaxes:")
        for tax in taxes:
            print(f"ID: {tax.ID}, CODE: {tax.CODE}, NAME: {tax.NAME}, PERCENT: {tax.PERCENT}")

        # Transactionテーブルの全データを取得
        transactions = session.query(Transaction).all()
        print("\nTransactions:")
        for transaction in transactions:
            print(f"ID: {transaction.TRD_ID}, DATETIME: {transaction.DATETIME}, TOTAL_AMT: {transaction.TOTAL_AMT}")

        # TransactionDetailテーブルの全データを取得
        transaction_details = session.query(TransactionDetail).all()
        print("\nTransaction Details:")
        for detail in transaction_details:
            print(f"Transaction ID: {detail.TRD_ID}, Product ID: {detail.PRD_ID}, Price: {detail.PRD_PRICE}")

if __name__ == "__main__":
    fetch_all_data()
