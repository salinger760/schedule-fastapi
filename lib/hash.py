import bcrypt

salt = bcrypt.gensalt(rounds=12, prefix=b"2a")


class Hash:
    def generate_hashed_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, hashed_password, plain_password) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
