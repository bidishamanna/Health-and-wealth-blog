from django.shortcuts import render
from datetime import timedelta, timezone
from django.utils import timezone

from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from account.authentication import JWTAuthentication, create_access_token, create_refresh_token, decode_refresh_token

from account.models import User, UserToken
from account.serializer import UserSerializer

class RegisterAPIView(APIView):
    def post(self, request):
        user = request.data
        print(f'User data received: {user}')
        
        if User.objects.filter(email=user['email']).exists():
            raise exceptions.APIException('Email already exists!')
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# list view 
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

# Check Authenticated User      GET: http://localhost:8000/api/user/ 
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication] # this is for token part/ authentication_classes = user{ return (user, {'is_admin': user.is_superuser}) its it in authentication.py file}...this user            
    permission_classes = [IsAuthenticated]  # this is for login part//Ensure only authenticated users can access this view # [IsAuthenticated]  same as @login decoretor

    def get(self, request): # in request>> return (user, {'is_admin': user.is_superuser})this user is store
        user = request.user
        is_admin = request.auth.get('is_admin', False)
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'is_admin': is_admin
        })

# User Login with JWT
class LoginAPIView(APIView):
    def post(self, request: Request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first() # .first() --> Returns the first object  from the QuerySet(if any),Returns None if the queryset is empty.
                                                        #filter() always returns a QuerySet — which could have 0, 1, or many results.
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        access_token = create_access_token(user.id) #user.id is the user's primary key (e.g., 1, 42, etc.),This ID is passed to your create_access_token() function.
        refresh_token = create_refresh_token(user.id)

        # here we are storing the refresh token of a specific user with an expiration date of 7 days
        UserToken.objects.create(
            user=user, #Left Side: user=This refers to the model field user defined in your UserToken model.
            #Right Side: user > user= User.objects.filter(email=email).first()).this user queryset
            token=refresh_token, 
            expired_at = timezone.now() + timedelta(days=7)
        )
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return response

# patch 
class UserUpdateView(APIView):
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "user": serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)

class UserPutView(APIView):
    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user, data=request.data)  # Full update
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteUserView(APIView):
    def delete(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid User ID"}, status=status.HTTP_404_NOT_FOUND)


# User Logout
@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(APIView):

    def post(self, request: Request):
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=400)

        UserToken.objects.filter(token=refresh_token).delete()

        response: Response = Response({
            'status': 'success',
            'message': 'Logged out successfully'
        }, status=200)

        response.delete_cookie(key='refresh_token')
        return response

class RefreshAPIView(APIView):
    def post(self, request: Request):
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=400)

        try:
            user_id = decode_refresh_token(refresh_token)
            user = User.objects.get(pk=user_id)

            token_obj = UserToken.objects.filter(
                user=user,
                token=refresh_token,
                expired_at__gt=timezone.now()
            ).first()

            if not token_obj:
                return Response({'error': 'Invalid or expired refresh token'}, status=401)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        except Exception as e:
            return Response({'error': f'Invalid token: {str(e)}'}, status=401)

        # Invalidate the old token
        token_obj.delete()

        # Generate new tokens
        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)

        # Save new refresh token
        UserToken.objects.create(
            user=user,
            token=new_refresh_token,
            expired_at=timezone.now() + timedelta(days=7)
        )

        response = Response({
            'user': UserSerializer(user).data,
            'access_token': new_access_token,
            'refresh_token': new_refresh_token
        })
        response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True)
        return response
