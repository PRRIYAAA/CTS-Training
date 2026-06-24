from passlib.context import CryptContext

# Use a password hashing scheme without bcrypt's 72-byte limit.
# pbkdf2_sha256 avoids the bcrypt length restriction and is secure
# for password storage in most FastAPI applications.

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )