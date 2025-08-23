from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.core.config import settings
from src.repositories.users_repo import UsersRepository
from src.schemas.user_schemas import LoggedUserSchema, UserAuthSchema, HashedUserSchema
from src.utils import auth_utils
from src.core.logger import logger
from src.utils.excepts import unknown_error, not_found_error


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def create_access_token(self, user: LoggedUserSchema) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
            "token_type": "access",
        }
        return auth_utils.encode_jwt(payload)

    async def create_refresh_token(self, user: LoggedUserSchema) -> str:
        payload = {
            "sub": str(user.id),
            "token_type": "refresh",
        }
        return auth_utils.encode_jwt(
            payload=payload,
            expire_timedelta=timedelta(
                days=settings.AUTH_JWT.refresh_token_expire_days
            ),
        )

    async def register_user(self, user: UserAuthSchema) -> LoggedUserSchema:
        """
        Ререстрируем пользователя, хешируем пароль и добавляем в бд, возвращаем
        схему для генерации токенов
        """
        try:
            hashed_password = auth_utils.hash_password(user.password)
            user_id = await self.users_repository.add_one(
                HashedUserSchema(
                    email=user.email,
                    username=user.username,
                    active_status=user.active_status,
                    password=hashed_password,
                )
            )
            logger.info(f"user: {user.email} with id: {user_id} registered succesfully")
            return LoggedUserSchema(
                email=user.email,
                username=user.username,
                id=user_id,
            )
        except IntegrityError as e:
            if "email" in str(f"Integrity Error: {e}").lower():
                detail = "Пользователь с таким email уже существует"
            elif "username" in str(e).lower():
                detail = "Пользователь с таким именем уже существует"
            else:
                detail = "Пользователь с такими данными уже существует"
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
        except Exception as e:
            logger.error(f"Unknown ERROR: {e}")
            raise unknown_error

    async def login_user(self, user: UserAuthSchema) -> LoggedUserSchema:
        """
        Логиним пользователя, отправляем запрос к базе, проверяем пароль
        """
        try:
            user_data = await self.users_repository.get_one(user.id)
            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            if not auth_utils.validate_password(user_data.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                )

            return LoggedUserSchema(
                email=user.email,
                username=user.username,
                id=user_data.id,
            )

        except Exception as e:
            logger.error(f"Unknown ERROR: {e}")
            raise unknown_error
