from fastapi import Header, HTTPException, status
from src.core import auth
from src.core.exceptions import DecodeTokenError, ValidateTokenError
from src.db.collections import user as db_user
from src.helpers.container import CONTAINER
from src.models.user import Role
from src.services.logger.interfaces.i_logger import ILogger


async def require_admin(authorization: str | None = Header(default=None)) -> None:
    """This function aim to check if a user has the admin role. If not an HttpException will be raised.

    Args:
        authorization (str | None, optional): Authorization string. Defaults to Header(default=None).

    Raises:
        HTTPException: Exception to indicate that the autentication did not went as expected.
    """

    logger = CONTAINER.get(ILogger)

    if authorization is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # The token is a bearer token, so it will be "Bearer somelongstring".
    # Tha string must be splitted on whitespace and only the element at index one
    # will be the jwt token.
    token = authorization.split(" ")[1]
    decoded_token: dict

    # Decode token.
    try:
        decoded_token = auth.decode_token(token)
        is_token_valid = auth.validate_token_base(decoded_token)
        if not is_token_valid:
            raise Exception
    except (DecodeTokenError, ValidateTokenError) as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=e.msg)
    except Exception as e:
        logger.warning("routes", e.loggable)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unknown error occured while validating the token.",
        )

    # Get the user from the db and see if given fields match.
    if Role.ADMIN.value not in decoded_token["roles"]:
        msg = f"The user may not exist or miss the {Role.ADMIN.value} role."
        logger.warning("routes", msg)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)

    user_res = await db_user.User.find_one(
        db_user.User.username == decoded_token["username"],
        db_user.User.email == decoded_token["email"],
        db_user.User.roles == decoded_token["roles"],
    )
    if user_res is None:
        msg = f"The user may not exist or miss the {Role.ADMIN.value} role."
        logger.warning("routes", msg)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)
