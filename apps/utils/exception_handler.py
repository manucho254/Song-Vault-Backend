from rest_framework import exceptions, status, views


def custom_exception_handler(exc, context):
    """ Custom exception handler

    Args:
        exc (_type_): exception
        context (_type_): context

    Returns:
        _type_: response
    """
    response = views.exception_handler(exc, context)

    if isinstance(exc, (exceptions.NotAuthenticated)):
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
