from rest_framework import serializers
from django.contrib.auth import get_user_model

from profiles_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    Ensures that certain fields are never null in the response,
    but are set to an empty string ('') if no value is present.
    """

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        ]

    # Ensure that certain fields are never null in the response
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in [
            'first_name', 'last_name', 'location',
            'tel', 'description', 'working_hours'
        ]:
            if data.get(field) is None:
                data[field] = ''
        return data

    # Ensure that certain fields are never null in the request
    def validate(self, attrs):
        for field in [
            "first_name", "last_name",
            "location", "tel",
            "description", "working_hours"
        ]:
            if field in attrs and attrs[field] is None:
                attrs[field] = ""
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for User with Profile data.
    Returns all users (with or without profile).
    """

    class Meta:
        model = get_user_model()
        fields = ['id']

    def to_representation(self, obj):
        """
        Return profile data if it exists, otherwise return default values.
        """
        try:
            profile = obj.profile
            return {
                'user': profile.user.id,
                'username': profile.username,
                'first_name': profile.first_name or '',
                'last_name': profile.last_name or '',
                'file': profile.file.url if profile.file else None,
                'location': profile.location or '',
                'tel': profile.tel or '',
                'description': profile.description or '',
                'working_hours': profile.working_hours or '',
                'type': profile.type
            }
        except Profile.DoesNotExist:
            return {
                'user': obj.id,
                'username': obj.username,
                'first_name': '',
                'last_name': '',
                'file': None,
                'location': '',
                'tel': '',
                'description': '',
                'working_hours': '',
                'type': obj.user_type
            }
