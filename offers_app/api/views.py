from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from offers_app.models import Offer, OfferDetail
from .filters import OfferFilter
from .permissions import IsBusinessUser, IsOwnerOfOffer
from .serializers import (OfferCreateSerializer, OfferDetailSerializer,
                          OfferListSerializer, OfferRetrieveSerializer,
                          OfferUpdateSerializer)


class OfferPagination(PageNumberPagination):
    """Pagination for the offer list endpoint."""

    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListCreateView(generics.ListCreateAPIView):
    """Lists all offers or creates a new one."""

    queryset = Offer.objects.all()
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']
    ordering = ['-updated_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsBusinessUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates or deletes a single offer."""

    queryset = Offer.objects.all()
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method in ('PATCH', 'DELETE'):
            return [IsAuthenticated(), IsOwnerOfOffer()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def get_object(self):
        obj = generics.get_object_or_404(Offer, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class OfferDetailRetrieveView(generics.RetrieveAPIView):
    """Retrieves a single offer detail."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
