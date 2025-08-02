from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql://ecommerce_user:ecommerce_password@db:5432/ecommercedb"


settings = Settings()
