from src.utils.excepts import not_found_error
from src.repositories.users_repo import UsersRepository
from src.schemas.user_schemas import ToPublicUserSchema
from src.core.logger import logger
from src.utils.excepts import unknown_error


class PublicService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def get_user_info(self, user_id: int) -> dict:
        user_data = await self.users_repository.get_one_with_relationship(user_id)
        if not user_data:
            raise not_found_error
        return user_data.model_dump()

    async def get_users_paginated(
        self, limit: int, skip: int
    ) -> list[ToPublicUserSchema]:
        try:
            users_data = (
                await self.users_repository.get_all_with_relationship_paginated(
                    limit, skip
                )
            )
            return users_data
        except Exception as e:
            logger.error(f"Unknown Error: {e}")
            raise unknown_error
