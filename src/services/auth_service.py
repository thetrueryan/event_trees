from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from repositories.users_repo import UsersRepository
from schemas.user_schemas import RegisteredUserSchema, UserAuthSchema
from utils.auth_utils import hash_password
from core.logger import logger


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def register_user(self, user: UserAuthSchema) -> RegisteredUserSchema:
        """
        Ререстрируем пользователя, хешируем пароль и добавляем в бд, возвращаем
        схему для генерации токенов
        """
        try:
            user.password = hash_password(user.password)
            user_id = await self.users_repository.add_one(user.model_dump())
            logger.info(f"user: {user.email} with id: {user_id} registered succesfully")
            return RegisteredUserSchema(
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
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=detail
                )
        except Exception as e:
            logger.error(f"Unknown ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла ошибка на стороне сервера"
            )