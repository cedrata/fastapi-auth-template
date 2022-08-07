from datetime import datetime
import re
from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr, Field, validator


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class BaseUser(BaseModel):
    """Class for representing and validate the atomic part of an user."""

    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="User username")

    @validator("email")
    def email_validation(cls, email):
        try:
            return EmailStr.validate(email)
        except Exception:
            raise ValueError(
                "The email validation was not succesful, the email may be invalid."
            )

    @validator("username")
    def username_validation(cls, username):
        pattern = re.compile("^[a-z0-9._]+$")
        match = pattern.fullmatch(username)
        if match is None:
            raise ValueError(
                "The username validation was not succesful, the username can only contain alfanumerical chars underscores and dots."
            )
        return username


class BaseUserRoles(BaseModel):
    """Class for representing and validate the user roles."""

    roles: List[Role] = Field(..., description="Collection of the user roles.")

    @validator("roles")
    def roles_validation(cls, roles):
        if len(roles) == 0:
            raise ValueError(
                "The roles validation was not succesful, at least a role must be present."
            )
        return roles


class UserRegistration(BaseUser):
    """Class for representing the autonomus user registration into the system."""

    password: str = Field(..., description="User password")


class UserAdminRegistration(BaseUser, BaseUserRoles):
    """Class for representin the user registration for admin user, requires at least one role."""

    password: str = Field(..., description="User password")


class UserLogin(BaseUser, BaseUserRoles):
    """Class for projection with only username and roles (other attributes if required, no password), from the db users collection."""

    pass


class UserPartialDetails(BaseUser, BaseUserRoles):
    """Class for projection containing partial user details like: email, username, roles, craetion and last update dates."""

    creation: datetime
    last_update: datetime
