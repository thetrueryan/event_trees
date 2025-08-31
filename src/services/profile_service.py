from src.repositories.users_repo import UsersRepository
from src.schemas.user_schemas import LoggedUserSchema


class ProfileService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository
