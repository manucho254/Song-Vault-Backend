from apps.utils.constants import GENRES

from datetime import timedelta, datetime
from typing import List, Dict, Union
import math
import os

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


def check_file_size(file) -> int:
    """Check size of a file

    Args:
        file (_type_): file to check size

    Returns:
        int: size of a file in megabytes
    """
    return math.floor(os.stat(file).st_size / (1024 * 1024))


def valid_mp3_extension(file_name: str) -> bool:
    """check if mp3 has a valid extension

    Args:
        file_name (str): name of mp3 file

    Returns:
        bool: True if file has the correct extension else false
    """
    if not file_name:
        return False

    name_split = file_name.split(".")[-1]

    return name_split != "mp3"


def valid_image_extension(file_name: str) -> bool:
    """check if image has a valid extension

    Args:
        file_name (str): name of image

    Returns:
        bool: True if file has the correct extension else false
    """
    if not file_name:
        return False

    name_split = file_name.split(".")[-1]
    valid_extensions = ["jpg", "png", "jpeg"]

    return name_split in valid_extensions
