from fastapi.security import OAuth2PasswordBearer
from typing import Final

# TODO: move token url to configs.
OAUTH2_SCHEME: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(tokenUrl="/auth/login")