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
