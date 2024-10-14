from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.mymodels import Product

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 商品コードから名前と価格を取得するエンドポイント
@app.get("/product/{code}")
def get_product_info(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.CODE == code).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"name": product.NAME, "price": product.PRICE}