from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from app.db.deps import get_db;
from app.db.session import SessionLocal
from app.utils.send_sms import send_sms
from sqlalchemy.orm import Session
from app.schemas.user import Phone, PhoneOtp
from app.models.user import User, Otp


import random
from datetime import timedelta, datetime, timezone


otp_storage = {}

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def getAllUsers(db: Session = Depends(get_db)):
    s = select(User)
    users = db.execute(s).scalars().all();
    return users;

@router.post("/login")
def authorize_user(input:PhoneOtp, db:Session = Depends(get_db)):

    query = select(Otp).where(Otp.mobile == input.mobile)
    row = db.execute(query).scalar_one_or_none()
    if not row:
        return "Mobile does not exists"
    if row.otp == input.otp:
        print(datetime.now(timezone(timedelta(hours=5, minutes=30))), row.expiry_at)
        if(datetime.now(timezone(timedelta(hours=5, minutes=30))) < row.expiry_at):
            return "Successfully logged in"
        return "OTP expired!!!"
    return "OTP wrong!!!!!"


@router.post("/sent-otp")
def send_otp(input: Phone, db: Session = Depends(get_db)):
    otp = str(random.randint(0, 9999)).zfill(4)
    exist = db.execute(select(Otp).where(Otp.mobile == input.mobile)).scalar_one_or_none()
    print(input.mobile)
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
    
    # db:Session = get_db
    user = db.execute(select(User.name).where(User.mobile == input.mobile)).scalars().first()

    if not user:
        return f"user not found! OTP {otp} Sent"
    else:
        return f"OTP {otp} sent to "+user;
    return 'otp sent'
    #check phn present and assignt to 'exist' variable
    #send OTP
    #store recent otp and mobile mapping
    #FUTURE: USE REDDIS
    #return res