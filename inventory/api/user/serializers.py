from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from sales.models import OrderItem
from ..admin.serializers import AdminDocumentSerializer, AdminProductVariant
from ...models import Brand, Category, Product, ProductReview


class CustomerBrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='logo.get_url', read_only=True)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo', 'logo_url', 'position', 'slug', 'is_featured', 'is_active')


class CustomerCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.get_url', read_only=True, required=False)
    parent_name = serializers.CharField(source='parent.name', read_only=True, required=False)
    product_count = serializers.CharField(source='get_product_count', read_only=True, required=False)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('product_count',)


class CustomerProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_image = serializers.CharField(source='user.get_image_url', read_only=True)
    product_name = serializers.CharField(source='product.get_product_name', read_only=True)
    product_image = serializers.CharField(source='product.get_thumbnail_url', read_only=True)

    # images = AdminDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            'id', 'user_name', 'user_image', 'product', 'product_name', 'product_image', 'rating', 'comment', 'images'
        )

    def validate(self, attrs):
        rating = attrs.get('rating')
        if rating and rating > 5:
            raise serializers.ValidationError({'rating': [_('Invalid rating.')]})
        product = attrs['product']
        user = self.context['request'].user
        if not self.instance:
            if not OrderItem.objects.filter(product=product, customer=user).exists():
                raise serializers.ValidationError(
                    {'product': [_('You must have purchased the product to leave a review.')]}
                )
            if self.Meta.model.objects.filter(product=product, user=user).exists():
                raise serializers.ValidationError({'product': [_('You have already reviewed this product.')], })
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        images = validated_data.pop('images')
        product_review = ProductReview.objects.create(**validated_data, user=user)
        product_review.images.set(images)
        product_review.save()
        return product_review


class CustomerProductReviewDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_image = serializers.CharField(source='user.get_image_url', read_only=True)
    product_name = serializers.CharField(source='product.get_product_name', read_only=True)
    product_image = serializers.CharField(source='product.get_thumbnail_url', read_only=True)
    # images = AdminDocumentSerializer(many=True, read_only=True)
    images = AdminDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            'id', 'user_name', 'user_image', 'product', 'product_name', 'product_image', 'rating', 'comment',
            'images'
        )


class CustomerProductListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    product_name = serializers.CharField(source='get_product_name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'product_name', 'price', 'quantity', 'average_rating', 'category', 'thumbnail_url', 'has_variant',
            'is_featured'
        )


class NewArrivalProductSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    product_name = serializers.CharField(source='get_product_name', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'product_name', 'price', 'quantity', 'average_rating', 'category', 'thumbnail_url', 'has_variant',
            'is_featured'
        )


class CustomerProductDetailSerializer(serializers.ModelSerializer):
    images = AdminDocumentSerializer(many=True, read_only=True)
    product_name = serializers.CharField(source='get_product_name', read_only=True)
    product_review = CustomerProductReviewDetailSerializer(many=True, read_only=True)
    product_variants = AdminProductVariant(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'product_name', 'images', 'total_review', 'quantity', 'average_rating', 'price', 'description',
            'product_specification', 'product_review', 'product_variants'
        )
