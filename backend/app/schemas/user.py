from typing import Annotated, Dict

from pydantic import BaseModel, constr, AfterValidator

def phone_validation(phn:str) -> str:
    if phn.isalnum() or len(phn)==10 or phn[0] in [6,7,8,9]:
        return phn
    raise ValueError('Number not valid')


class Phone(BaseModel):
    mobile: Annotated[str, AfterValidator(phone_validation)]

class PhoneOtp(BaseModel):
    mobile: Annotated[str, AfterValidator(phone_validation)]
    otp: str #validate
    is_new_user: bool

class OTPResponse(BaseModel):
    pass

class ResponseSchema(BaseModel):
    data: Dict
    status: int
    message: str