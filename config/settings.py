from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    

    
    class Config:
        env_file = "config/.env"
        env_file_encoding = 'utf-8'