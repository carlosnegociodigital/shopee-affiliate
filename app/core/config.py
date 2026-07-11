from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    APP_ID = os.getenv("APP_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    API_URL = os.getenv("API_URL")

settings = Settings()