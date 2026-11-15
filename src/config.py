import os
from dotenv import load_dotenv

load_dotenv()

class Settings: 
    
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT","5432")
    DB_NAME: str = os.getenv("DB_NAME","postgres")
    DB_USER: str =  os.getenv("DB_USER","postgres")
    DB_PASSWORD: str =  os.getenv("DB_PASSWORD","")
    SECRET_SALT: str = os.getenv("SECRET_SALT", "")
    
settings = Settings()
    
    
    
    
    
    
    