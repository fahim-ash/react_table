# models.py
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test_project.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class StockMarket(Base):
    __tablename__ = "stock_market"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    trade_code = Column(String, index=True)
    high = Column(Numeric)
    low = Column(Numeric)
    open = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Numeric)

def create_database():
    print('database has been created')
    Base.metadata.create_all(bind=engine)
