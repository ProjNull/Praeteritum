from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Microservice"
    postgres_url: str
    redis_url: str
    kafka_bootstrap_servers: str

    class Config:
        env_file = ".env"


settings = Settings()
