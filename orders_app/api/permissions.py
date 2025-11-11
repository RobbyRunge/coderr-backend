from rest_framework.permissions import BasePermission


class IsBusinessUserOfOrder(BasePermission):
    """
    Permission: Only the business user of the order can update its status.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.business_user


class IsCustomerUser(BasePermission):
    """
    Permission: Only users with profile type 'customer' can create orders.
    """
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return profile and getattr(profile, 'type', None) == 'customer'