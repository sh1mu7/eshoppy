from coreapp.api.serializers import DocumentSerializer
from ...models import Brand, Category, VariantGroup, VariantOption, Product, ProductVariant, ProductReview
from rest_framework import serializers


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
    group = AdminVariantGroupSerializer(many=False)

    class Meta:
        model = VariantOption
        fields = '__all__'


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


class AdminProductDetailSerializer(serializers.ModelSerializer):
    images_url = DocumentSerializer(many=True)
    category_name = serializers.CharField(source='get_category_name', read_only=True)
    parent_category_name = serializers.CharField(source='get_parent_category_name', read_only=True)
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    brand_name = serializers.CharField(source='get_brand_name', read_only=True)

    # stock_status_display = serializers.CharField(source='get_stock_status_display', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'product_code', 'slug', 'thumbnail', 'thumbnail_url', 'category', 'category_name',
            'parent_category_name', 'brand', 'brand_name', 'sku', 'description', 'cost', 'price', 'has_promotion',
            'promotional_price', 'promotions_start_date', 'promotions_expiry_date', 'quantity', 'vat', 'unit',
            'unit_value', 'has_variant', 'reward_points', 'stuck_status', 'is_active', 'is_featured', 'images',
            'images_url'
        )
