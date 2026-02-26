from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for a single OfferDetail object."""

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailUrlSerializer(serializers.ModelSerializer):
    """Serializer that returns only id and url for an OfferDetail."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f'/api/offerdetails/{obj.id}/'


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for the offer list endpoint."""

    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'username': obj.user.username,
        }


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Serializer for the offer detail endpoint."""

    details = OfferDetailUrlSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    def get_min_price(self, obj):
        prices = obj.details.values_list('price', flat=True)
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        times = obj.details.values_list('delivery_time_in_days', flat=True)
        return min(times) if times else None


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new offer with exactly 3 details."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError('Exactly 3 details are required (basic, standard, premium).')
        types = [d['offer_type'] for d in value]
        if sorted(types) != ['basic', 'premium', 'standard']:
            raise serializers.ValidationError('Details must include basic, standard and premium.')
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Serializer for partially updating an offer and its details."""

    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError('Each detail must include "offer_type".')
        return value

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            OfferDetail.objects.filter(offer=instance, offer_type=offer_type).update(**detail_data)
        return instance