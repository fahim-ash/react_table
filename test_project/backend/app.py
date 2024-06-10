from fastapi import FastAPI, Depends
from models import StockMarket
from sqlalchemy.orm import Session
from db import get_db
import csv
from datetime import datetime


app = FastAPI()

@app.get("/")
async def read_root():
    print('hello world')
    return {"message": "Hello, World"}

@app.get("/index")
async def index():
    return {"message": "Hello, World"}

def process_csv_data(row):
    data = {}
    data["date"] = datetime.strptime(row[0], "%Y-%m-%d").date()
    data["trade_code"] = row[1]
    data["high"] = row[2].replace(",", "")
    data["low"] = row[3].replace(",", "")
    data["open"] = row[4].replace(",", "")
    data["close"] = row[5].replace(",", "")
    data["volume"] = row[6].replace(",", "")
    print(data)

    return data

@app.get("/insert_data")
async def insert_data(db: Session=Depends(get_db)):
    with open('misc/stock_market_data.csv', 'r') as csvfile:
        next(csvfile, None)
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            processed_data = process_csv_data(row)
            new_entry = StockMarket(**processed_data)
            db.add(new_entry)
    db.commit()
    return {"message": "Inserted Data Succesfully"}

