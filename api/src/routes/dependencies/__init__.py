from bson import _UNPACK_LENGTH_SUBTYPE_FROM
from fastapi import HTTPException, Header, status
from src.core.exceptions import DecodeTokenError, ValidateTokenError
from src.models.commons import HttpExceptionMessage
from src.models.user import Role
from src.core import auth
from src.db.collections import user as db_user

# TODO: move token decoding to smaller function.
# TODO: logger must be in here too.


async def require_admin(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # The token is a bearer token, so it will be "Bearer somelongstring".
    # Tha string must be splitted on whitespace and only the element at index one
    # will be the jwt token.
    token = authorization.split(" ")[1]
    decoded_token:dict

    # Decode token.
    try:
        decoded_token = auth.decode_token(token)
        is_token_valid = auth.validate_token_base()
        if is_token_valid: raise Exception
    except (DecodeTokenError, ValidateTokenError):
        raise HttpExceptionMessage(status.HTTP_401_UNAUTHORIZED)
    except Exception:
        raise HttpExceptionMessage(status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Get the user from the db and see if given fields match.
    user_res = db_user.User.find_one(db_user.User.username == decoded_token["username"], db_user.User.email == decoded_token["email"], db_user.User.roles == decoded_token["roles"])
    if Role.ADMIN.value not in decoded_token["roles"] or user_res is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Required {Role.ADMIN} role")
