from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allows write access only to the owner of the profile."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
