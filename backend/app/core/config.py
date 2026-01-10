from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TWILLIO_KEY : str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILLIO_FROM_MOBILE: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_TIMEDELTA_MINUTES: str

    class Config:
        env_file = ".env"

settings = Settings()