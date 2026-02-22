from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reading and writing review data."""

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get('request')
        business_user = attrs.get('business_user')
        if Review.objects.filter(reviewer=request.user, business_user=business_user).exists():
            raise serializers.ValidationError('You have already reviewed this business user.')
        return attrs
