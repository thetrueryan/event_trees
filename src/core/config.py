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


class JWTSettings(BaseSettings):
    AUTH_JWT: AuthJWT = AuthJWT()


jwt_settings = JWTSettings()


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PASS: str
    DB_USER: str
    DB_PORT: int

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_SYNC(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


db_settings = DBSettings()

DB_ASYNC_URL = db_settings.DATABASE_URL_ASYNC
DB_SYNC_URL = db_settings.DATABASE_URL_SYNC
