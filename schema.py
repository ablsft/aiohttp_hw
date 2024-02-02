from typing import Type, Optional
import re
import abc

import pydantic
from pydantic import EmailStr, Field


PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 24

PASSWORD_LOWERCASE = re.compile(r'[a-z]')
PASSWORD_DIGITS = re.compile(r'[0-9]')


class CreateAdvertisement(pydantic.BaseModel):

    title: str
    description: str


class UpdateAdvertisement(pydantic.BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None


class AbstractUser(pydantic.BaseModel, abc.ABC):
    username: str
    password: str
    email: Optional[str] = None

    @pydantic.field_validator('email')
    def check_email(cls, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError('Invalid email address')
        return value

class CreateUser(AbstractUser):

    @pydantic.field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < PASSWORD_MIN_LENGTH:
            raise ValueError(
                f'Password must contain at least {PASSWORD_MIN_LENGTH} characters')
        if len(value) > PASSWORD_MAX_LENGTH:
            raise ValueError(
                f'Password length should not exceed {PASSWORD_MAX_LENGTH} characters')
        if not PASSWORD_LOWERCASE.search(value):
            raise ValueError('Password must contain lowercase letters')
        if not PASSWORD_DIGITS.search(value):
            raise ValueError('Password must contain digits')
        return value
    

class UpdateUser(CreateUser):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class Login(AbstractUser):
    pass


SCHEMA_MODEL = Type[CreateAdvertisement | UpdateAdvertisement | CreateUser |
                    UpdateUser | Login]
