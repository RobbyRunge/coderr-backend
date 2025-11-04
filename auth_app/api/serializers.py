from rest_framework import serializers

from auth_app.models import CustomUser


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    Validates input fields and checks for uniqueness of username and email.
    Fields:
        - username: required, max length 150
        - email: required, must be a valid email address
        - password: required, write-only
        - repeated_password: required, write-only, must match password
        - type: required, must be 'customer' or 'business'
    """
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(
        choices=['customer', 'business'],
        required=True
    )

    def validate(self, data):
        """
        Validates registration data:
            - Checks if passwords match
            - Checks if username and email are unique
        Raises:
            serializers.ValidationError: if validation fails
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken.")

        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return data


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates input fields.
    Fields:
        - username: required
        - password: required
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        """
        Validate login credentials.
        Checks:
            - Username is not empty
            - Password is not empty
            - User exists with the given username
            - Password matches the user's hashed password
        Raises:
            - ValidationError if credentials are invalid
        Returns:
            - data dict with added 'user' key containing User instance
        """
        username = data.get('username')
        password = data.get('password')

        # Validate username field
        if not username or username.strip() == '':
            raise serializers.ValidationError(
                {'username': 'Username is required.'}
            )

        # Validate password field
        if not password or password.strip() == '':
            raise serializers.ValidationError(
                {'password': 'Password is required.'}
            )

        # Check if user exists
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'User does not exist.'}
            )

        # Verify password
        if not user.check_password(password):
            raise serializers.ValidationError(
                {'error': 'Invalid credentials.'}
            )

        # Add user to validated data
        data['user'] = user
        return data
