from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_str(password: str):
    return pwd_context.hash(password)


def verify_str(password: str, hashed: str):
    return pwd_context.verify(password, hashed)
