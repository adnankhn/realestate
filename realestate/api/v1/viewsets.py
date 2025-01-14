from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user signup.
        Expects: email, password
        """
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ValidationError("Both email and password are required.")

        try:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already registered."}, status=HTTP_400_BAD_REQUEST)
            
            # Create user with email as username
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password
            )
            
            # Generate token for immediate login
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "User created successfully.",
                "user_id": user.id,
                "token": token.key
            }, status=HTTP_201_CREATED)
            
        except IntegrityError:
            return Response({"error": "Registration failed."}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user login.
        Expects: email, password
        Returns: Authentication Token
        """
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ValidationError("Both email and password are required.")

        try:
            # Get user by email
            user = User.objects.get(email=email)
            # Authenticate with username (email) and password
            auth_user = authenticate(username=user.username, password=password)
            
            if auth_user is None:
                raise AuthenticationFailed("Invalid credentials.")

            # Generate or retrieve token
            token, _ = Token.objects.get_or_create(user=auth_user)

            return Response({
                "message": "Login successful.",
                "token": token.key,
                "user_id": auth_user.id
            }, status=200)
            
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid credentials.")