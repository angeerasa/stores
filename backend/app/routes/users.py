from fastapi import APIRouter, Depends, status
from sqlalchemy import select, update
from app.db.deps import get_db;
from app.db.session import SessionLocal
from app.utils.send_sms import send_sms
from sqlalchemy.orm import Session
from app.schemas.user import Phone, PhoneOtp, ResponseSchema
from app.models.user import User, Otp


import random
from datetime import timedelta, datetime, timezone

from app.utils.pyjwt import create_access_token



router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def getAllUsers(db: Session = Depends(get_db)):
    s = select(User)
    users = db.execute(s).scalars().all();
    return users;

@router.post("/login", response_model=ResponseSchema)
def authorize_user(input:PhoneOtp, db:Session = Depends(get_db)):
    query = select(Otp).where(Otp.mobile == input.mobile)
    row = db.execute(query).scalar_one_or_none()
    if not row:
        return "Mobile does not exists"
    if row.otp == input.otp:
        if(datetime.now(timezone(timedelta(hours=5, minutes=30))) < row.expiry_at):
            #is first time user?
            user=db.execute(select(User).where(User.mobile == input.mobile)).scalar_one_or_none();
            # create user if first time user
            if not user:
                user = User(name=input.mobile, mobile= input.mobile)
                db.add(user)
                db.commit()
            # add id in claim
            jwt_claim = {
                "mobile": user.mobile,
                "name" : user.name
            }
            access_token = create_access_token(data=jwt_claim)
            return ResponseSchema(data= {"access_token": access_token,
                        "is_new_user": input.is_new_user,
                        "mobile": input.mobile,
                        "name": user.name
                    },
                    message= "login successful",
                    status= "200"
                )
        return ResponseSchema(
                data= {},
                message= "OTP Expired",
                status= "200")
            
    return ResponseSchema(
                data= {},
                message = "Invalid OTP",
                status= "200"
            )


@router.post("/sent-otp", response_model=ResponseSchema)
def send_otp(input: Phone, db: Session = Depends(get_db)):
    try:
        otp = str(random.randint(0, 9999)).zfill(4)
        exist = db.execute(select(Otp).where(Otp.mobile == input.mobile)).scalar_one_or_none()
        if(exist):
            db.execute(update(Otp).where(Otp.mobile == input.mobile).values(otp=otp));
        else:
            storeOtp = Otp(
            mobile = input.mobile,
            otp = otp
            )
            db.add(storeOtp);
        db.commit();
        send_sms(input, otp);
        
        user = db.execute(select(User.name).where(User.mobile == input.mobile)).scalars().first()

        if not user:
            return ResponseSchema(
                data = {
                    "is_new_user" : True,
                    "otp": otp
                },
                status = status.HTTP_200_OK,
                message = "User does not exist. OTP Sent"
            )
        else:
            return  ResponseSchema(
                data = {
                    "is_new_user" : False,
                    "otp": otp
                },
                status = status.HTTP_200_OK,
                message = "OTP Sent"
            )
    except Exception as err:
        return  ResponseSchema(
            data = {
            },
            status = status.HTTP_400_BAD_REQUEST,
            message = str(err)
        )