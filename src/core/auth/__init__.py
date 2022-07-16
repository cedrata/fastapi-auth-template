from fastapi.security import OAuth2PasswordBearer
from typing import Final

# This is instance will be injected in routes when those have to be secured.
# This is just checcking the user exists and the inserted credentials are corect, role is not 
# responsability of OAUTH2_SCHEME, at least for the implementation w/out full oauth flow.
#
# The tokenUrl is not inserted in any configuration file because it should not change in time,
# by doing so it encourages keep the same endpoint as the login one.
OAUTH2_SCHEME: Final[OAuth2PasswordBearer] = OAuth2PasswordBearer(tokenUrl="/auth/login")