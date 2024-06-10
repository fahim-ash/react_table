from config import *
from app import app
import uvicorn
if __name__ == "__main__":
    print('listening..........')
    uvicorn.run(app, host=host, port=port)