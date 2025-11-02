from rest_framework import serializers

from auth_app.models import CustomUser

class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(choices=['customer', 'business'], required=True)

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken.")

        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return data
    
         