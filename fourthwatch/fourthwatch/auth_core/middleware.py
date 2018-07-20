from rest_framework.authentication import TokenAuthentication
from fourthwatch.auth_core.models import Token
class CustomTokenAuthentication(TokenAuthentication):
    model = Token
    keyword = "Bearer"
