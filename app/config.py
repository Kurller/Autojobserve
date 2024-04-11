
#from pydantic import BaseSettings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password:str
    database_hostname:str
    database_username:str
    database_name:str
    
    
    class Config():
        env_file=".env"
settings=Settings()