from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config.config import SECRET_KEY


# Hash Password
def hash_password(password):

    if isinstance(password, bytes):
        password = password.decode("utf-8")

    return generate_password_hash(password)


# Check Password
def check_password(password, hashed_password):

    if isinstance(password, bytes):
        password = password.decode("utf-8")

    if isinstance(hashed_password, bytes):
        hashed_password = hashed_password.decode("utf-8")

    return check_password_hash(hashed_password, password)


# Generate JWT Token
def generate_token(username):

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    # Convert bytes to string
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token