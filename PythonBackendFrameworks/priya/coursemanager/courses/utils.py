# utils.py
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from jose import JWTError, jwt
from rest_framework.exceptions import APIException

from .models import User


class Unauthorized(APIException):
    status_code = 401
    default_detail = "Invalid or expired authentication token."
    default_code = "not_authenticated"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a plain text password matches the hashed version."""
    if check_password(plain_password, hashed_password):
        return True

    # Preserve compatibility with users registered before Django's password
    # hasher was adopted. Modern bcrypt versions work directly but are not
    # compatible with Passlib 1.7's backend detection.
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        import bcrypt

        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except (TypeError, ValueError):
            return False
    return False

def hash_password(plain_password: str) -> str:
    """Hashes a plain text password for secure storage."""
    return make_password(plain_password)


def create_access_token(data: dict) -> str:
    """Generates a signed JWT token using python-jose with an expiry window."""
    to_encode = data.copy()
    
    # Calculate expiry timestamp
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    
    # Update payload payload with standard 'exp' claim
    to_encode.update({"exp": expire})
    
    # Sign and encode the token
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def get_current_user(request) -> User:
    """Decode a Bearer JWT and return the user identified by its subject."""
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise Unauthorized("Authentication credentials were not provided.")

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        email = payload.get("sub")
        if not email:
            raise Unauthorized("Invalid authentication token.")
        return User.objects.get(email=email)
    except User.DoesNotExist as exc:
        raise Unauthorized("Invalid authentication token.") from exc
    except JWTError as exc:
        # python-jose raises JWTError for invalid signatures and expired tokens.
        raise Unauthorized("Invalid or expired authentication token.") from exc
