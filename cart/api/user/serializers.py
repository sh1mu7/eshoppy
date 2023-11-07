from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ...models import Wishlist, Cart


class UserWishlistListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='get_product_name', read_only=True)
    product_thumbnail = serializers.CharField(source='get_product_thumbnail', read_only=True)
    product_price = serializers.CharField(source='get_product_price', read_only=True)
    product_variants = serializers.CharField(source='get_product_variant', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product_name', 'product_price', 'product_thumbnail', 'product_variants')


class UserWishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user', 'product')
        read_only_fields = ('user',)

    def validate(self, attrs):
        product = attrs.get('product')
        wishlist = Wishlist.objects.filter(product=product)
        if wishlist.exists():
            raise serializers.ValidationError({"product": [_('This product is already in your wishlist'), ]})
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        wishlist = Wishlist.objects.create(**validated_data, user=user)
        return wishlist


class UserCartListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='get_product_name', read_only=True)
    product_price = serializers.CharField(source='get_product_price', read_only=True)
    product_thumbnail = serializers.CharField(source='get_product_thumbnail', read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'product_name', 'product_thumbnail', 'product_price', 'product_price', 'variant', 'quantity')


class UserCartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'product', 'variant', 'quantity')
        read_only_fields = ('user',)

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        cart = Cart.objects.filter(product=product)
        if quantity < 1:
            raise serializers.ValidationError({'detail': [_("Product quantity can't be 0"), ]})
        if product.quantity < quantity:
            raise serializers.ValidationError(
                {"detail": [_('The requested quantity exceeds available stock.'), ]})
        if cart.exists():
            raise serializers.ValidationError({"detail": [_('The product is already in your cart'), ]})
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.create(**validated_data, user=user)
        return cart


class UserCartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('quantity',)

    def validate(self, attrs):
        quantity = attrs.get('quantity')
        available_quantity = self.instance.product.quantity
        if quantity < 1:
            raise serializers.ValidationError({'detail': [_("Product quantity can't be 0"), ]})
        if available_quantity < quantity:
            raise serializers.ValidationError({'detail': [_('The requested quantity exceeds available stock.'), ]})
        return attrs
