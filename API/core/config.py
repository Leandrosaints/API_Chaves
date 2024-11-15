from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base




#"mysql+asyncmy://user:password@localhost:3306/database", pool_pre_ping=True)

class Settings(BaseSettings):
    API_V1_STR:str = "/api/v1"
    DB_URL:str = 'mysql+asyncmy://root:''@localhost:3306/painel'
    DBBaseModel = declarative_base()

    JWT_SECRETS:str = "g_BA-RPpdW2uoAwZPTRIKorXErtMxH2thdJzB5X3TFY"
    ALGORITHM:str = 'HS256'
    ACESSE_TOKEN_EXPIRE_MINUTES:int = 60*24*7

class Config:
    case_sensitive: True

settings: Settings = Settings()
