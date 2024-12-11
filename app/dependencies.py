from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "m1a2r3i4j5a6n7a8"
ALGORITHM = "HS256"
