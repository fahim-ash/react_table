from config import *
from app import app
import uvicorn
from models import create_database
if __name__ == "__main__":
    print('listening..........')
    create_database()
    uvicorn.run(app, host=host, port=port)

