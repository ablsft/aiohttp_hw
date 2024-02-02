from aiohttp import web
from sqlalchemy import select

from crud import get_item_by_id, create_item, update_item, delete_item, select_first
from models import Advertisement, User, Token
from tools import validate
from errors import NotFound, Unauthorized
from auth import hash_password, check_password, check_token, check_owner
from schema import (
    CreateAdvertisement, 
    UpdateAdvertisement, 
    CreateUser,
    UpdateUser,
    Login,
)


class AdvertisementView(web.View):

    @check_token
    async def get(self):
        session = self.request['session']
        advertisement_id = self.request.match_info.get('advertisement_id')
        if advertisement_id is None:
            return web.json_response([advertisement.dict for advertisement in 
                            self.request.token.user.advertisements])
        advertisement = await get_item_by_id(Advertisement, 
                                             int(advertisement_id), session)
        check_owner(advertisement, self.request.token.user_id)
        return web.json_response(advertisement.dict)
        
    @check_token
    async def post(self):
        session = self.request['session']
        payload = validate(CreateAdvertisement, await self.request.json())
        payload['user_id'] = self.request.token.user_id
        advertisement = await create_item(Advertisement, payload, session)
        return web.json_response({'id': advertisement.id})
        
    @check_token
    async def patch(self):
        session = self.request['session']
        advertisement_id = self.request.match_info.get('advertisement_id')
        payload = validate(UpdateAdvertisement, await self.request.json())
        advertisement = await get_item_by_id(Advertisement, 
                                             int(advertisement_id), session)
        check_owner(advertisement, self.request.token.user_id)
        advertisement = await update_item(advertisement, payload, session)
        return web.json_response({'id': advertisement.id})
        
    @check_token
    async def delete(self):
        session = self.request['session']
        advertisement_id = self.request.match_info.get('advertisement_id')
        advertisement = await get_item_by_id(Advertisement, 
                                             int(advertisement_id), session)
        check_owner(advertisement, self.request.token.user_id)
        await delete_item(advertisement, session)
        return web.json_response({'status': 'deleted'})


class UserView(web.View):

    @check_token
    async def get(self):
        session = self.request['session']
        token = self.request.token

        user = await get_item_by_id(User, token.user_id, session)
        return web.json_response(user.dict)
        
    async def post(self):
        session = self.request['session']
        payload = validate(CreateUser, await self.request.json())
        payload['password'] = hash_password(payload['password'])
        user = await create_item(User, payload, session)
        return web.json_response({'id': user.id})
        
    @check_token
    async def patch(self):
        session = self.request['session']
        payload = validate(UpdateUser, await self.request.json())
        user = await update_item(self.request.token.user, payload, session)
        return web.json_response({'status': 'patched'})
        
    @check_token
    async def delete(self):
        session = self.request['session']
        await delete_item(self.request.token.user, session)
        return web.json_response({'status': 'deleted'})
    

class LoginView(web.View):

    async def post(self):
        session = self.request['session']
        payload = validate(Login, await self.request.json())
        query = select(User).where(User.username == payload['username'])
        user = await select_first(query, session)
        if user is None:
            raise Unauthorized('invalid user')
        if check_password(payload['password'], user.password):
            token = await create_item(Token, {'user_id': user.id}, session)
            return web.json_response({'token': str(token.token)})
        raise Unauthorized('invalid password')
        