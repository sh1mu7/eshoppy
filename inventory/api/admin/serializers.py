from django.db.models import F

from coreapp.api.serializers import DocumentSerializer
from django.utils.translation import gettext_lazy as _
from coreapp.models import Document
from ...models import Brand, Category, VariantGroup, VariantOption, Product, ProductVariant, ProductReview
from rest_framework import serializers
from ...utils.product_variants import create_product_variants, update_product_variants


class AdminDocumentSerializer(serializers.ModelSerializer):
    document_url = serializers.CharField(source='get_url', read_only=True)

    class Meta:
        model = Document
        fields = ('id', 'document_url')


class AdminBrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='logo.get_url', read_only=True)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo', 'logo_url', 'order', 'slug', 'is_featured', 'is_active')


class AdminCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.get_url', read_only=True, required=False)
    parent_name = serializers.CharField(source='parent.name', read_only=True, required=False)
    product_count = serializers.CharField(source='get_product_count', read_only=True, required=False)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('product_count',)


class AdminVariantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantGroup
        fields = ('group_name', 'is_active')


class AdminVariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantOption
        fields = '__all__'


class AdminProductVariant(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductVariant
        fields = '__all__'
        read_only_fields = ('product',)


class AdminProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_name', read_only=True)
    parent_category_name = serializers.CharField(source='get_parent_category_name', read_only=True)
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    brand_name = serializers.CharField(source='get_brand_name', read_only=True)
    stock_status_display = serializers.CharField(source='get_stock_status_display', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'sku', 'brand_name', 'category_name', 'parent_category_name', 'thumbnail_url', 'is_featured',
            'stock_status_display', 'is_active'
        )


class AdminProductCreateSerializer(serializers.ModelSerializer):
    product_variants = AdminProductVariant(many=True, required=False, write_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'thumbnail', 'category',
            'brand', 'sku', 'description', 'cost', 'price', 'has_promotion',
            'promotional_price', 'promotions_start_date', 'promotions_expiry_date', 'quantity', 'vat', 'unit_name',
            'unit_value', 'has_variant', 'product_specification', 'reward_points', 'stock_status', 'is_active',
            'is_featured', 'images', 'product_variants'
        )
        read_only_fields = ('product_variants',)

    def validate(self, attrs):
        has_variant = attrs['has_variant']
        if has_variant:
            try:
                data = attrs['product_variants']
            except KeyError:
                raise serializers.ValidationError({'product_variants': [_('variant data not found')]})
        return attrs

    def create(self, validated_data):
        has_variant = validated_data.get('has_variant', False)
        variants_data = validated_data.pop('product_variants', [])
        images = validated_data.pop('images')

        if not has_variant:
            product = Product.objects.create(**validated_data)
            product.images.set(images)
            return product
        else:
            product = Product.objects.create(**validated_data)
            product.images.set(images)
            create_product_variants(product, variants_data)
            return product


class AdminProductDetailSerializer(serializers.ModelSerializer):
    images = AdminDocumentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='get_category_name', read_only=True)
    parent_category_name = serializers.CharField(source='get_parent_category_name', read_only=True)
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    brand_name = serializers.CharField(source='get_brand_name', read_only=True)
    product_variants = AdminProductVariant(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'product_code', 'slug', 'thumbnail', 'thumbnail_url', 'category', 'category_name',
            'parent_category_name', 'brand', 'brand_name', 'sku', 'description', 'cost', 'price', 'has_promotion',
            'promotional_price', 'promotions_start_date', 'promotions_expiry_date', 'quantity', 'vat', 'unit_name',
            'unit_value', 'has_variant', 'reward_points', 'stock_status', 'is_active', 'is_featured', 'images',
            "product_specification", 'product_variants'
        )


class AdminProductUpdateSerializer(serializers.ModelSerializer):
    product_variants = AdminProductVariant(many=True, required=False, write_only=True)

    class Meta:
        model = Product
        fields = (
            'name', 'thumbnail', 'category',
            'brand', 'sku', 'description', 'cost', 'price', 'has_promotion',
            'promotional_price', 'promotions_start_date', 'promotions_expiry_date', 'quantity', 'vat', 'unit_name',
            'unit_value', 'has_variant', 'product_specification', 'reward_points', 'stock_status', 'is_active',
            'is_featured', 'images', 'product_variants'
        )

    def validate(self, attrs):
        has_variant = attrs.get('has_variant')
        if has_variant:
            if 'product_variants' not in attrs:
                raise serializers.ValidationError({'product_variants': [_('variant data not found')]})
        return attrs

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        variants_data = validated_data.pop('product_variants', [])
        Product.objects.filter(id=instance.id).update(**validated_data)
        instance.images.set(images)
        update_product_variants(instance, variants_data)
        return instance


class AdminPromotionProductSerializer(serializers.ModelSerializer):
    promotion_status = serializers.CharField(source='get_promotion_status', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'product_code', 'name', 'promotional_price', 'promotions_start_date', 'promotions_expiry_date',
            'promotion_status'
        )


class AdminPromotionProductDetailSerializer(serializers.ModelSerializer):
    promotion_status = serializers.CharField(source='get_promotion_status', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'product_code', 'name', 'price', 'promotional_price', 'promotions_start_date',
            'promotions_expiry_date',
            'promotion_status'
        )


class AdminProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    product_name = serializers.CharField(source='product.get_product_name', read_only=True)
    product_image = serializers.CharField(source='product.get_thumbnail_url', read_only=True)
    images_url = AdminDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            'id', 'user_name', 'product', 'product_name', 'product_image', 'rating', 'comment', 'images', 'images_url'
        )
