from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from profiles_app.models import UserProfile

from .permissions import IsAdminUser, IsBusinessUserOfOrder, IsCustomerUser
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    """Lists orders for the current user or creates a new order."""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer_user=user) | Order.objects.filter(business_user=user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates status or deletes a single order."""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUserOfOrder()]
        return [IsAuthenticated()]

    def get_object(self):
        obj = generics.get_object_or_404(Order, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class OrderCountView(APIView):
    """Returns the count of in-progress orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        generics.get_object_or_404(UserProfile, user__id=business_user_id, type=UserProfile.BUSINESS)
        count = Order.objects.filter(business_user__id=business_user_id, status=Order.IN_PROGRESS).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    """Returns the count of completed orders for a business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        generics.get_object_or_404(UserProfile, user__id=business_user_id, type=UserProfile.BUSINESS)
        count = Order.objects.filter(business_user__id=business_user_id, status=Order.COMPLETED).count()
        return Response({'completed_order_count': count})
