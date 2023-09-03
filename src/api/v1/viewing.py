from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
import httpx

from api.v1.auth.auth_bearer import BaseJWTBearer
from core.config import ugc_config, friends_config
from services.auth import AuthApi

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/movie_matches',
    description='Получение списка фильмов и друзей',
    dependencies=[Depends(BaseJWTBearer())]
)
async def get_movie_matches(request: Request):
    current_user = request.token_payload
    current_user_id = current_user['id']
    current_user_bookmark_link = f'{ugc_config.url_bookmarks}/{current_user_id}'
    current_user_bookmarks = httpx.get(url=current_user_bookmark_link).json()
    matches = {bm: [] for bm in current_user_bookmarks}

    friend_link = friends_config.url_friends_list
    friends = httpx.get(friend_link).json()

    for friend in friends['friends']:
        friend_id = friend['id']
        bookmark_link = f'{ugc_config.url_bookmarks}/{friend_id}'
        response = httpx.get(bookmark_link).json()
        for bookmark in response:
            if bookmark in current_user_bookmarks:
                matches.get(bookmark).append(friend_id)

    return matches
