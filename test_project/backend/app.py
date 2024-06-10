from fastapi import FastAPI
from test_project.backend.models import StockMarket
from sqlalchemy.orm import Session
import csv


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
    for date, trade_code, high, low, open, close, volume in row:
        data["date"] = date
        data["trade_code"] = trade_code
        data["high"] = high
        data["low"] = low
        data["open"] = open
        data["close"] = close
        data["volume"] = volume
    return data

@app.post("/insert_data")
async def insert_data():
    with open('../misc/stock_market.csv', 'r') as csvfile:
        next(csvfile, None)
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            processed_data = process_csv_data(row)
            new_entry = StockMarket(**processed_data)
            Session.add(new_entry)
    Session.close
    return {"message": "Inserted Data Succesfully"}

