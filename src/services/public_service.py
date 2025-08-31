from src.utils.excepts import not_found_error
from src.repositories.users_repo import UsersRepository


class PublicService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def get_user_info(self, user_id: int) -> dict:
        user_data = await self.users_repository.get_one_with_relationship(user_id)
        if not user_data:
            raise not_found_error
        return user_data.model_dump()
