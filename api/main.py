from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv
from api.database import get_db,Users

load_dotenv()
origin = os.getenv('ORIGIN')
origins: List[str] = origin.split(',') if origin else ["https://ytnotes.co"]
host = os.getenv('HOST')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

class UserEmail(BaseModel):
    email:EmailStr

class WaitlistResponse(BaseModel):
    message:str
    status:str


@app.post('/register',response_model=WaitlistResponse)
async def register(email:UserEmail,db:Session = Depends(get_db)):
    try:
        register_email = email.email.lower().strip()
        existing_user = db.query(Users).filter(Users.email == register_email).first()
        if existing_user:
            return JSONResponse(
                status_code=200,
                content = {
                    'message':'You are already registered🥳',
                    'status':'already registered'
                    }
            )
        register_user = Users(email = register_email)
        db.add(register_user)
        try:
            db.commit()
            return JSONResponse(
                status_code=201,
                content={
                    'message':'Excited to have you on board🎉',
                    'status':'success'
                    }
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
            status_code=500,
            detail={
                'message':'Databse error occurred',
                'status':'error'
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={
                'message':'Something went wrong',
                'status':'Unexpected error occourred'
            }
        )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000) )
    uvicorn.run(
        app,
        # reload=True,
        workers=4,
        host=host,
        port=port,
         log_level='info'
        )
