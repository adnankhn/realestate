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
        Expects: username, password, email (optional)
        """
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', None)

        if not username or not password:
            raise ValidationError("Both username and password are required.")

        try:
            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return Response({"error": "Username already exists."}, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "User created successfully.", "user_id": user.id}, status=HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user login.
        Expects: username, password
        Returns: Authentication Token
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid credentials.")

        # Generate or retrieve token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Login successful.",
            "token": token.key,
            "user_id": user.id
        }, status=200)
