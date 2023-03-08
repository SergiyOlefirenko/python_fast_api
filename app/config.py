from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_url: str
    secret_key: str
    algorithm: str
    access_token_expire_mins: int

    class Config:
        env_file = '.env'

settings = Settings()
