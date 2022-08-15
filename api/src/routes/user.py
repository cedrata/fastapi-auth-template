from datetime import datetime
from typing import Any, Dict, Final, List, Tuple

from beanie.odm.enums import SortDirection
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from src.core.auth import (
    OAUTH2_SCHEME,
    hash_password,
    is_admin,
    is_authorized,
    require_admin,
)
from src.db.collections.user import User as UserCollection
from src.helpers.container import CONTAINER
from src.models.commons import BaseMessage, HttpExceptionMessage
from src.models.user import (
    Role,
    UserPartialDetails,
    UserPartialDetailsAdmin,
    UserRegistration,
    UserRegistrationAdmin,
)
from src.routes.enums.commons import Endpoint
from src.services.logger.interfaces.i_logger import ILogger

# Router instantiation.
router = APIRouter()

_REGISTER_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: BaseMessage,
    Endpoint.RESPONSES: {
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "User registration for basic user, this will set the default user role to 'user', to let the use chose the roles use the /register-admin endpoint",
}


@router.post(
    "/register",
    response_model=_REGISTER_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_REGISTER_POST_PARAMS[Endpoint.RESPONSES],
    description=_REGISTER_POST_PARAMS[Endpoint.DESCRIPTION],
)
async def register(user_registration: UserRegistration):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username} as username.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=user_registration.password,
        roles=[Role.USER.value],
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.save()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg)
    except Exception as e:
        logger.error("routes", str(e))
        msg = f"An unknown exception occured, maybe bad db connection"
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username} has been succesully added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_REGISTER_ADMIN_POST_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: BaseMessage,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": f"Forbidden access, {Role.ADMIN} role required",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_409_CONFLICT: {
            "model": HttpExceptionMessage,
            "description": "Unsuccesful registration, the user already exists",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "User registration for admin, this will let the user chose the roles, at least one role is required.This endpoint execution is limited to users having the admin role. This endpoint execution is limited to users having the admin role.",
    Endpoint.DEPENDENCIES: [Depends(require_admin)],
    # Endpoint.TAGS: [Role.ADMIN.value.capitalize()],
}


@router.post(
    "/register-roles",
    response_model=_REGISTER_ADMIN_POST_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_REGISTER_ADMIN_POST_PARAMS[Endpoint.RESPONSES],
    description=_REGISTER_ADMIN_POST_PARAMS[Endpoint.DESCRIPTION],
    dependencies=_REGISTER_ADMIN_POST_PARAMS[Endpoint.DEPENDENCIES],
)
async def register_admin(
    user_registration: UserRegistrationAdmin,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    now_date = datetime.utcnow()

    # Check if user access token is valid.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user has admin role.
    if not is_admin_result[1]:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    # Document creation.
    logger.info(
        "routes",
        f"Document creation for user having {user_registration.username} as username and roles {user_registration.roles}.",
    )
    user = UserCollection(
        email=user_registration.email,
        username=user_registration.username,
        password=hash_password(user_registration.password),
        roles=user_registration.roles,
        creation=now_date,
        last_update=now_date,
    )

    # Saving the document to db.
    try:
        await user.save()
    except DuplicateKeyError as e:
        logger.error("routes", str(e))
        duplicates = dict(e.details).get("keyPattern")
        msg = f"The following fields must be unique: {duplicates}"
        raise HTTPException(status.HTTP_409_CONFLICT, detail=msg)
    except Exception as e:
        logger.error("routes", str(e))
        msg = f"An unknown exception occured, maybe bad db connection"
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response = BaseMessage(message="OK")
    status_code = status.HTTP_201_CREATED

    logger.info(
        "routes",
        f"The user having username {user_registration.username} and roles {user_registration.roles} has been succesully added to the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_GET_ALL_USERS_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: List[UserPartialDetails | UserPartialDetailsAdmin],
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": f"Forbidden access, {Role.ADMIN} role required",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "Get all users with parial details from the db. If needed is possible to limit returned entities and skip the required amount",
}


@router.get(
    "/all",
    response_model=_GET_ALL_USERS_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_GET_ALL_USERS_PARAMS[Endpoint.RESPONSES],
    description=_GET_ALL_USERS_PARAMS[Endpoint.DESCRIPTION],
)
async def get_all_users(
    limit: int | None = None,
    skip: int | None = None,
    is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin),
):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    projection: BaseModel

    # Check if user is authorized to access the endpoint.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if the user has admin role or not.
    if not is_admin_result[1]:
        projection = UserPartialDetails
    else:
        projection = UserPartialDetailsAdmin

    logger.info(
        "routes",
        f"Returning the users in the db: limit={limit} and skip={skip}.",
    )

    try:
        response = await UserCollection.find_all(
            projection_model=projection,
            limit=limit,
            skip=skip,
            sort=[("username", SortDirection.ASCENDING)],
        ).to_list()
    except Exception as e:
        logger.error(
            "routes", f"An unknown exception occured while fetcthing the users: {e}"
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        f"Success returning all the users.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_GET_USERS_COUNT_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: int,
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_403_FORBIDDEN: {
            "model": HttpExceptionMessage,
            "description": f"Forbidden access, {Role.ADMIN} role required",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while registering the user",
        },
    },
    Endpoint.DESCRIPTION: "Get the total number of users in the database",
}


@router.get(
    "/count",
    response_model=_GET_USERS_COUNT_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_GET_USERS_COUNT_PARAMS[Endpoint.RESPONSES],
    description=_GET_USERS_COUNT_PARAMS[Endpoint.DESCRIPTION],
)
async def get_users_count(
    is_authorized_result: Tuple[bool, dict] = Depends(is_authorized)
):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: int

    # Check if teh user is authorized or not.
    if not is_authorized_result[0]:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="The provided token may be expired or invalid.",
        )

    logger.info(
        "routes",
        f"Returning the total number of users document in the db.",
    )

    try:
        response = await UserCollection.find_all().count()
    except Exception as e:
        logger.error(
            "routes",
            f"An unknown exception occured while fetcthing the total number of users documents: {e}",
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        f"Success returning the total number of users documents in the db.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_GET_USER_BY_ID_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: List[UserPartialDetails | UserPartialDetailsAdmin],
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",  # Exception raised by the require_admin function (see Endpoint.DEPENDENCIES).
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    Endpoint.DESCRIPTION: "Get user parial details from the db given the username. To get full details run admin endpoint.",
}


@router.get(
    "/username/{username}",
    response_model=_GET_USER_BY_ID_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_GET_USER_BY_ID_PARAMS[Endpoint.RESPONSES],
    description=_GET_USER_BY_ID_PARAMS[Endpoint.DESCRIPTION],
)
async def get_user_by_username(
    username: str, is_admin_result: Tuple[bool, bool, dict] = Depends(is_admin)
):
    logger = CONTAINER.get(ILogger)
    status_code: int
    response: BaseModel
    projection: BaseModel

    # Check if user access token was valid and user authorized.
    if not is_admin_result[0]:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    # Check if user has admin role or not.
    if not is_admin_result[1]:
        projection = UserPartialDetails
    else:
        projection = UserPartialDetailsAdmin

    logger.info(
        "routes",
        f"Returning the in the db: username={username}.",
    )

    try:
        response = await UserCollection.find_one(
            UserCollection.username == username,
            projection_model=projection,
        )
    except Exception as e:
        logger.error(
            "routes", f"An unknown exception occured while fetcthing the user: {e}"
        )
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

    status_code = status.HTTP_200_OK

    logger.info(
        "routes",
        f"Success returning the serched user.",
    )
    return JSONResponse(status_code=status_code, content=jsonable_encoder(response))


_GET_CURRENT_USER_PARAMS: Final[Dict[Endpoint, Any]] = {
    Endpoint.RESPONSE_MODEL: List[UserPartialDetails | UserPartialDetailsAdmin],
    Endpoint.RESPONSES: {
        status.HTTP_401_UNAUTHORIZED: {
            "model": HttpExceptionMessage,
            "description": "Unauthorized",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": HttpExceptionMessage,
            "description": "An unknown error occured while retriving the user",
        },
    },
    Endpoint.DESCRIPTION: "Get current user complete details.",
}


@router.get(
    "/me",
    response_model=_GET_CURRENT_USER_PARAMS[Endpoint.RESPONSE_MODEL],
    responses=_GET_CURRENT_USER_PARAMS[Endpoint.RESPONSES],
    description=_GET_CURRENT_USER_PARAMS[Endpoint.DESCRIPTION],
)
async def get_current_user(
    is_authorized_result: Tuple[bool, dict] = Depends(is_authorized),
    token: str = Depends(OAUTH2_SCHEME),
):

    # Check if the user is authorized or not.
    if not is_authorized_result[0]:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="The provided token may be expired or invalid.",
        )

    # Decoded token is in is_authorized_result[1]

    response = UserCollection.find_one()

    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)
