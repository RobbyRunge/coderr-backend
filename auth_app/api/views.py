from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny

from profiles_app.models import Profile

from .serializers import RegistrationSerializer, LoginSerializer
from auth_app.models import CustomUser


class RegistrationView(APIView):
    """
    API endpoint for user registration (customer or business).
    Expects: username, email, password, repeated_password, type
    Returns: Auth token, username, email, user ID
    Status codes:
        201 - User successfully created
        400 - Invalid request data
        500 - Internal server error
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user registration.
        Validates input, creates a new user, and returns an authentication
        token.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create user
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                user_type=serializer.validated_data['type']
            )

            # Create auth token
            token, created = Token.objects.get_or_create(user=user)

            # Create associated profile
            Profile.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                type=serializer.validated_data['type']
            )

            # Success response
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }, status=status.HTTP_201_CREATED)

        # Error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    Expects: username, password
    Returns: Auth token, fullname, email, user ID
    Status codes:
        200 - Login successful
        400 - Invalid credentials
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login request.

        Validates credentials and returns authentication token.
        """
        serializer = LoginSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            # Get authenticated user from validated data
            user = serializer.validated_data['user']
            # Get or create authentication token
            token, created = Token.objects.get_or_create(user=user)
            # Prepare response data
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
