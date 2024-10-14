#データベースのURLを取得

import os, urllib
from dotenv import load_dotenv

load_dotenv()

SERVER_URL=os.environ["SERVER_URL"]
DATABASE=os.environ["DATABASE"]
USER_NAME=os.environ["USER_NAME"]
PASSWORD=os.environ["PASSWORD"]
SERVER_PORT=os.environ["SERVER_PORT"]

DATABASE_URL = f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{SERVER_URL}:{SERVER_PORT}/{DATABASE}?charset=utf8"
