from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
    postgres_user: str
    postgres_password: str
    postgres_db: str
    db_host: str
    db_port: int
    redis_host: str
    redis_port: int
    redis_db: int
    celery_redis_db: int
    elastic_host: str
    elastic_port: int


settings = Settings()
