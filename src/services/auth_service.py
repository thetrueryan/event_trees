from repositories.users_repo import UsersRepository


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    