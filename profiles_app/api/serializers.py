from rest_framework import serializers

from profiles_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for full profile detail (GET and PATCH on /api/profile/{pk}/)."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', default='')
    last_name = serializers.CharField(source='user.last_name', default='')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description',
            'working_hours', 'type', 'email', 'created_at',
        ]
        read_only_fields = ['user', 'created_at']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        return super().update(instance, validated_data)


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Serializer for business profile list."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', default='')
    last_name = serializers.CharField(source='user.last_name', default='')

    class Meta:
        model = UserProfile
        fields = [
            'user', 'username', 'first_name', 'last_name',
            'file', 'location', 'tel', 'description', 'working_hours', 'type',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer for customer profile list."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', default='')
    last_name = serializers.CharField(source='user.last_name', default='')

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'type']
