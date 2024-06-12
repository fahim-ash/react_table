from fastapi import FastAPI, Depends
from models import StockMarket, StockMarketBase
from sqlalchemy.orm import Session
from db import get_db
import csv
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    print('hello world')
    return {"message": "Hello, World"}

@app.get("/stock_market", response_model=List[StockMarketBase])
async def stock_market(db: Session = Depends(get_db)):
    query = db.query(StockMarket).filter(StockMarket.id < 10)
    data = query.all()
    if not data:
        return {"message": "Data not found"}
    return data


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
    #check if already data exists
    query = db.query(StockMarket).fetchone()
    if query:
        return {"message": "data already inserted"}
    
    with open('misc/stock_market_data.csv', 'r') as csvfile:
        next(csvfile, None)
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            processed_data = process_csv_data(row)
            new_entry = StockMarket(**processed_data)
            db.add(new_entry)
    db.commit()
    return {"message": "Inserted Data Succesfully"}

