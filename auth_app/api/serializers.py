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
