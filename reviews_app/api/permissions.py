from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Custom permission to only allow customer users to access certain views.
    Assumes the User model has an 'is_customer' attribute.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer)


class IsBusinessUser(BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    Assumes the User model has an 'is_business' attribute.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_business)
