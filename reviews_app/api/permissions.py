from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Custom permission to only allow customer users to access certain views.
    Assumes the User model has a 'user_type' attribute.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "user_type", None) == "customer"
        )


class IsBusinessUser(BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    Assumes the User model has an 'is_business' attribute.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_business)
    

class IsReviewOwner(BasePermission):
    """
    Allows access only to the owner of the review.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
