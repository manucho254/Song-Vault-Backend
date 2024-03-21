from apps.utils.constants import GENRES

from datetime import timedelta, datetime
from typing import List, Dict, Union

from django.conf import settings

import jwt


def get_genres() -> List[tuple]:
    """get genres

    Returns:
        list: a dictionary of genres
    """
    return GENRES


def encode_token(payload: Dict, hours: int = 4) -> str:
    """Encode jwt token
    Args:
        payload (dict): payload to create token with
        hours (int, optional): expiry duration. Defaults to 4.

    Returns:
        str: jwt encoded token
    """
    payload.update({"exp": timedelta(hours=hours) + datetime.now()})

    return jwt.encode(payload, key=settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> Union[Dict, None]:
    """Decode jwt token

    Args:
        token (str): jwt token

    Returns:
        str: none if token decoding fails else return token
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
