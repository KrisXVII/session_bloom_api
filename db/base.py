import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

class Base(DeclarativeBase):
	pass

os.getenv("DATABASE")

db = SQLAlchemy(model_class=Base)

