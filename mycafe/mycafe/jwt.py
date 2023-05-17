# -*- coding: utf-8 -*-
"""JWT 관련 모듈

JWT관련 모듈이다
"""

import random
import datetime

from django.conf import settings

import jwt


def create_token(user_pk: int) -> str:
    """JWT를 생성하는 함수

    JWT를 생성하는 함수이다. JWT에 포함되는 정보는 exp claim, 
    user_pk이다.
    salt는 random int를 추가해 동시점 동일 유저가 토큰 생성 시 
    동일한 토큰이 생성되는걸 방지한다
    
    Parameters
    ----------
    user_pk : int
        User 객체의 pk 값

    Returns
    ----------
    tokens : str
        token string
    """

    iat = datetime.datetime.now(tz=datetime.timezone.utc)

    payload = {
        'user_pk' : user_pk,
        'exp' : iat + settings.JWT_TOKEN_TTL,
        'salt' : random.randint(0, 1000000000)
    }
    token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm="HS256")

    return token

def check_token(token : str) \
            -> tuple[dict[str, str] or None, str or None]:
    """JWT를 체크하는 함수

    create_jwt로 생성 된 JWT 토큰 valid체크하는 함수.
    - signature
    - exp
    순으로 검사를 하게 됨.
    
    Parameters
    ----------
    token : str
        검사 할 token string

    Returns
    ----------
    payload : tuple[dict[str, str] or None, str or None]
        token의 payload 정보(dict)와 실패 시 실패 원인문자열 반환

    See Also
    ----------
    create_token : JWT 생성 함수
    """

    assert token and type(token) == str

    payload = None
    msg = None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        msg = "Invalid signature"
    except jwt.ExpiredSignatureError:
        msg = "Token expired"
    except jwt.DecodeError:
        msg = "Invalid input"
    except jwt.InvalidTokenError:
        msg = "Unknown jwt error"

    return payload, msg
