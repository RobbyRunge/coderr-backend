from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """
    Allow access only to business users for certain actions.
    """
    def has_permission(self, request, view):
        # Only relevant for POST requests
        if request.method == 'POST':
            return (
                request.user and
                request.user.is_authenticated and
                getattr(request.user, 'user_type', None) == 'business'
            )
        return True