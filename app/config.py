from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DATABASE: str
    
    # Application settings
    APP_NAME: str = "Fruits API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A comprehensive API for managing fruits, nutritional information, and suppliers"
    
    # Environment settings
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    TESTING: bool = False
    
    # Azure App Service settings
    WEBSITE_HOSTNAME: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 