# Mock user class for testing purposes

class User:
    def __init__(self, id: int, username: str, password_hash: str):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password: str) -> str:
        # Mock password hashing function
        return f"hashed_{password}"