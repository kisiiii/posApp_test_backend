from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.mymodels import Product, Transaction, TransactionDetail, Tax
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pytz import timezone
from pydantic import BaseModel

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンに変更 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 商品コードから名前と価格を取得するエンドポイント
@app.get("/product/{code}")
def get_product_info(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.CODE == code).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"name": product.NAME, "price": product.PRICE, "cost":product.COST, "supllier":product.SUPPLIER, "manufacuturer":product.MANUFACTURER}

# 購入処理エンドポイント
# Pydanticモデルを定義して、リクエストデータをバリデーション
class CartItem(BaseModel):
    name: str
    price: int
    barcode: str

class PurchaseRequest(BaseModel):
    cart: list[CartItem]
    totalAmt: int
    totalAmtExTax: int

@app.post("/purchase")
def purchase(purchase_data: PurchaseRequest, db: Session = Depends(get_db)):
    cart = purchase_data.cart
    totalAmt = purchase_data.totalAmt
    totalAmtExTax = purchase_data.totalAmtExTax
    
    JST = timezone('Asia/Tokyo')
    now = datetime.now(JST)  # 日本時間の現在時刻

    # transactionsテーブルに取引情報を挿入
    transaction = Transaction(
        DATETIME=now,
        EMP_CD="30",  # 固定値
        STORE_CD="001",  # 固定値（店舗コード）
        POS_NO="90",  # 固定値
        TOTAL_AMT=totalAmt,
        TTL_AMT_EX_TAX=totalAmtExTax,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)  # TRD_IDを取得

    # tax テーブルから 10% の税コードを取得
    tax_code = db.query(Tax).filter(Tax .NAME == "10%").first()  # NAME に変更
    if not tax_code:
        raise HTTPException(status_code=404, detail="10% の税コードが見つかりません")

    # transaction_detailsテーブルに購入明細を挿入
    for item in cart:
        product = db.query(Product).filter(Product.CODE == item.barcode).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品が見つかりません: {item.barcode}")

        transaction_detail = TransactionDetail(
            TRD_ID=transaction.TRD_ID,
            PRD_ID=product.PRD_ID,
            PRD_CODE=product.CODE,
            PRD_NAME=product.NAME,
            PRD_PRICE=product.PRICE,
            TAX_CD=tax_code.CODE,  # 消費税コード固定
        )
        db.add(transaction_detail)

    db.commit()

    # 合計金額（税込・税抜）を返す
    return {"totalAmt": totalAmt, "totalAmtExTax": totalAmtExTax}