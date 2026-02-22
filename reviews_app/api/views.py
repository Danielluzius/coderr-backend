from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review

from .permissions import IsCustomerUser, IsOwnerOfReview
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """Lists all reviews or creates a new one."""

    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        reviewer_id = self.request.query_params.get('reviewer_id')
        ordering = self.request.query_params.get('ordering', '-updated_at')
        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)
        return queryset.order_by(ordering)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a single review."""

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAuthenticated(), IsOwnerOfReview()]
        return [IsAuthenticated()]

    def get_object(self):
        obj = generics.get_object_or_404(Review, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
