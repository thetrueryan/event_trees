from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "jwt_keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "jwt_keys" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    AUTH_JWT: AuthJWT = AuthJWT()

    DB_HOST: str | None = None
    DB_NAME: str | None = None
    DB_PASS: str | None = None
    DB_USER: str | None = None
    DB_PORT: int | None = None

    MODE: str | None = None

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()

DB_ASYNC_URL = settings.DATABASE_URL_ASYNC
DB_SYNC_URL = settings.DATABASE_URL_SYNC
