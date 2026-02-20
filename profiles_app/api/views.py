from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import UserProfile

from .permissions import IsOwner
from .serializers import BusinessProfileSerializer, CustomerProfileSerializer, UserProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieves or partially updates a user profile by user pk."""

    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'patch']

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_object(self):
        obj = generics.get_object_or_404(UserProfile, user__pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class BusinessProfileListView(generics.ListAPIView):
    """Returns a list of all business user profiles."""

    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type=UserProfile.BUSINESS)


class CustomerProfileListView(generics.ListAPIView):
    """Returns a list of all customer user profiles."""

    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type=UserProfile.CUSTOMER)
