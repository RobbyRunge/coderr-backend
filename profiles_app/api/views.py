from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile
from .serializers import ProfileSerializer, UserProfileSerializer


class ProfileDetailView(RetrieveUpdateAPIView):
    """
    View to retrieve and update a user profile.
    Only the owner of the profile can update it.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Ensure that only the owner can update their profile.
        """
        obj = super().get_object()
        if self.request.method in ['PATCH', 'PUT']:
            if obj.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(
                    "You are only allowed to edit your own profile."
                )
        return obj


class BusinessProfileListView(ListAPIView):
    """
    View to retrieve business profiles.
    Returns all users with user_type='business' (with or without profile).
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(user_type='business').order_by('id')


class CustomerProfileListView(ListAPIView):
    """
    View to retrieve customer profiles.
    Returns all users with user_type='customer' (with or without profile).
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        User = get_user_model()
        return User.objects.filter(user_type='customer').order_by('id')
