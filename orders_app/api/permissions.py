from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'


class IsBusinessUserOfOrder(BasePermission):
    """Allows write access only to the business user of the order."""

    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user


class IsAdminUser(BasePermission):
    """Allows access only to admin/staff users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
