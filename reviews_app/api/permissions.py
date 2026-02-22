from rest_framework.permissions import BasePermission


class IsOwnerOfReview(BasePermission):
    """Allows write access only to the creator of the review."""

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user


class IsCustomerUser(BasePermission):
    """Allows access only to users with a customer profile."""

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'customer'
