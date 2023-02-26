from typing import Optional
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request


def get_user_from_header(request: Request) -> Optional[int]:
    """
    Given a request, return the user id if the user is authenticated,
    otherwise return None.
    """
    user_id = None
    try:
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(token)
            user_id = validated_token['user_id']
    except:
        pass
    return user_id


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
