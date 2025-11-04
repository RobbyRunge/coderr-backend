from rest_framework import serializers

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

    def to_representation(self, instance):
        """
        Override the default representation to ensure that
        specific fields are never null, but empty strings if unset.
        """
        data = super().to_representation(instance)
        for field in [
            'first_name', 'last_name', 'location',
            'tel', 'description', 'working_hours'
        ]:
            if data.get(field) is None:
                data[field] = ''
        return data
