from rest_framework import serializers
from .models import Product, Review
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'user_id', 'username', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_id', 'username']


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'category', 'sku', 'price', 'description', 'is_active',
                  'created_at', 'updated_at', 'reviews', 'average_rating', 'review_count']

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else None

    def get_review_count(self, obj):
        return obj.reviews.count()


class GenerateContentSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(
        choices=["twitter", "instagram", "facebook", "linkedin"])
    tone = serializers.ChoiceField(
        choices=["professional", "casual", "playful", "urgent"],
        default="professional")
    extra_instructions = serializers.CharField(
        max_length=500, required=False, allow_blank=True, default="")
