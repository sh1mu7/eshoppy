from ...models import Brand, Category, VariantGroup, VariantOption, Product, ProductVariant, ProductReview
from rest_framework import serializers


class CustomerBrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='logo.get_url', read_only=True)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'logo', 'logo_url', 'order', 'slug', 'is_featured', 'is_active')


class CustomerCategorySerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='image.get_url', read_only=True, required=False)
    parent_name = serializers.CharField(source='parent.name', read_only=True, required=False)
    product_count = serializers.CharField(source='get_product_count', read_only=True, required=False)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('product_count',)
