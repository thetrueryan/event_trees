from datetime import timedelta, datetime, timezone

import jwt
import bcrypt

from src.core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
    expire_minutes: int = settings.AUTH_JWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc())
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat=now,
        exp=expire,
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(password=pwd_bytes, salt=salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
