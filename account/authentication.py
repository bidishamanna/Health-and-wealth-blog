import jwt
from datetime import datetime, timedelta, timezone
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from account.models import User

import os
from dotenv import load_dotenv
load_dotenv()

# Custom Authentication Class is meant to checks JWT token in the request header and verifies it.
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request): # request--data come from frontend
        auth_header = get_authorization_header(request).split() 
        
        if len(auth_header) != 2:
            raise AuthenticationFailed('Authorization header is malformed')
        # converting  bearer token to new token ///////
        try:
            token = auth_header[1].decode('utf-8')  # Decode the token(.decode('utf-8') converts bytes to a string using the UTF-8 character encoding.) # byte_data = b'hello'  string_data = byte_data.decode('utf-8') print(string_data)  # Output: hello

            print(f'Token received from client: {token}')
        except UnicodeDecodeError:
            raise AuthenticationFailed('Invalid token encoding')
        #/////////////////////////////////////////////////////////
        try:
            user_id = decode_access_token(token) # user_id =  return payload['user_id']
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            raise AuthenticationFailed(f'Token validation error: {str(e)}')
        return (user, {'is_admin': user.is_superuser})                  # return (user, None)

# JWT token has three parts (Header.Payload.Signature).
def create_access_token(id):
    payload = {
        'user_id': id,  #the function create_access_token takes one argument, named id(comes from views.py (user.id)..here this user.id store in id). if i write def create_access_token(user_id),then it should be 'user_id': user_id,
        'iat': datetime.now(timezone.utc),  
        'exp': datetime.now(timezone.utc) + timedelta(seconds=30), # Token expiration time
    }
    secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret')
    algorithm = "HS256"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_access_token(token):
    try:
        secret_key = os.getenv('JWT_SECRET_KEY', 'default_secret')  # Use a secure method to store secrets
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except Exception as e:
        raise exceptions.AuthenticationFailed(f'{str(e)}')

def create_refresh_token(id):
    payload = {
        'user_id': id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),  
        'iat': datetime.now(timezone.utc)
    }
    secret_key = os.getenv('JWT_REFRESH_SECRET_KEY', 'default_secret')
    algorithm = "HS256"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_refresh_token(token):
    try:
        refresh_secret = os.getenv('JWT_REFRESH_SECRET_KEY', 'default_secret') 
        payload = jwt.decode(token, refresh_secret, algorithms='HS256')
        print(f'payload: {payload}')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')


