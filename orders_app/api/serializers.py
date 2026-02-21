from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for reading order data."""

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'created_at', 'updated_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating an order from an offer detail."""

    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all())

    def create(self, validated_data):
        offer_detail = validated_data['offer_detail_id']
        customer_user = self.context['request'].user
        business_user = offer_detail.offer.user
        return Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
