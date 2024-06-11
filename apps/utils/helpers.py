from apps.utils.constants import GENRES

from datetime import timedelta, datetime
from typing import List, Dict, Union
import math
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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


def generate_link(token: str, base_dir: str) -> str:
    """Generates a link

    Args:
        token (str): _description_
        base_dir (str): _description_

    Returns:
        str: _description_
    """
    return settings.FRONTEND_URL + base_dir + "/" + token


def send_email_message(
    template: str, context: Dict, to: List[str], subject: str, base_dir: str
) -> None:
    """Custom email sending function
    Args:
        subj (str): "message subject"
        template (str): "email template"
        context (dict): key value pairs of user information
        to (List[str]): receivers email
    """
    subject, from_email = (
        subject,
        settings.EMAIL_HOST_USER,
    )
    if context.get("name") is None:
        context["name"] = to
    context["link"] = generate_link(context["token"], base_dir)
    print(context["link"])
    del context["token"]
    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
