from bcrypt import hashpw, gensalt, checkpw
from aiohttp.web import View
from sqlalchemy import select

from db import Session
from errors import Unauthorized, Forbidden
from models import Token, MODEL
from crud import select_first


def hash_password(password: str) -> str:
    password = password.encode()
    password = hashpw(password, salt=gensalt())
    return password.decode() 

def check_password(password: str, hashed_password: str) -> bool:
    password = password.encode()
    hashed_password = hashed_password.encode()
    return checkpw(password, hashed_password)

def check_token(handler):
    async def wrapper(view: View):
        token = view.request.headers.get('Authorization')
        if token is None:
            raise Unauthorized('token not found')

        session = view.request['session']
        query = select(Token).where(Token.token == token)
        token = await select_first(query, session)
        if token is None:
            raise Unauthorized('invalid token')
        view.request.token = token
        return await handler(view)
    
    return wrapper

def check_owner(item: MODEL, user_id: int):
    if item.user_id != user_id:
        raise Forbidden('access denied')
    