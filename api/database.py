from sqlalchemy import create_engine, Column,String,DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session,sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
DATABASEURL =os.getenv('POSTGRESQLURI')   
engine = create_engine(DATABASEURL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Users(Base):
    __tablename__ = 'users'
    email = Column(String,primary_key=True,index=True)
    joined_at = Column(DateTime,default=datetime.now)