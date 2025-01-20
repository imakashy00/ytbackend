from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from database import get_db,Users
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:3000'],
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
    uvicorn.run(
        app,
        reload=True,
        host='0.0.0.0',
        port=8000
        )
