from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Allows access only to users with a business profile."""

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.type == 'business'


class IsOwnerOfOffer(BasePermission):
    """Allows write access only to the owner of the offer."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
