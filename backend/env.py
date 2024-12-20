import os


SECRET_KEY = os.getenv("SECRET_KEY", "1234567890")  # Replace with a secure key
ALGORITHM = "HS256"  # Algorithm used for signing the token
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time
