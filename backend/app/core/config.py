from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    TWILLIO_KEY : str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILLIO_FROM_MOBILE: str

    class Config:
        env_file = ".env"

settings = Settings()