from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.headers.get('Authorization')
        if header and header.startswith('Bearer '):
            token = header.split(' ')[1]
            try:
                user = JWTAuthentication().authenticate(request)
                request.user = user[0]
            except:
                pass

        response = self.get_response(request)

        return response
