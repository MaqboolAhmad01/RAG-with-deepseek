from fastapi import APIRouter, HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from src.core.auth import get_password_hash
from src.core.email import send_verification_email
from src.core.utils import generate_otp
from src.models.user import User

from src.config.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])

# Secret key for JWT encoding/decoding
SECRET_KEY = "your_secret_key"



# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class CreateUser(BaseModel):
    email: str
    username: str
    password: str
    profile_pic:str |None=None

@router.post("/sign_up")
async def sign_up(body: CreateUser,db:Session = Depends(get_db)):
    try:
        with db.begin():
            username = body.username
            password = body.password

            if existing_user := db.query(User).filter(User.username == username).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with {existing_user.email} already exists")
            
            new_user = User(
                email=body.email,
                username=username,
                profile_pic=body.profile_pic,
                hashed_password=get_password_hash(password)  
            )

            db.add(new_user)
            db.commit()

            otp = generate_otp()
            send_verification_email(email=body.email, otp_code=otp)
        
        return {"message": "User create successfully"}
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)) from err