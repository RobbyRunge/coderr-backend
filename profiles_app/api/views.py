from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile
from .serializers import ProfileSerializer


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
