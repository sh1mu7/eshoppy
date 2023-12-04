from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _

from sales.models import Coupon, Order
from ...utils import validate
from inventory.models import ProductVariant, Product
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
    product_thumbnail = serializers.CharField(source='get_product_thumbnail', read_only=True)
    variant = serializers.PrimaryKeyRelatedField(read_only=True)
    product_variant = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.IntegerField()
    product_price = serializers.SerializerMethodField(method_name='get_product_price')

    class Meta:
        model = Cart
        fields = (
            'id', 'product', 'product_name', 'product_thumbnail', 'product_price', 'variant', 'product_variant',
            'quantity')

    def get_product_price(self, instance):
        # TODO : This method needs to be optimized otherwise it will trigger N+1 query

        product = instance.product
        if product.has_variant:
            product_variant = instance.product_variant
            if product_variant:
                return product_variant.additional_price + product.price
        return product.price


class UserCartCreateSerializer(serializers.ModelSerializer):
    product_variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), required=False)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'variant', 'quantity', 'product_variant')
        read_only_fields = ('user',)

    def validate(self, attrs):
        user = self.context.get('request').user if self.context.get('request') and self.context.get(
            'request').user.is_authenticated else None
        validated_attrs = validate.validate_cart_creation(attrs, user)
        return validated_attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.create(**validated_data, user=user)
        cart.save()
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


class CartPriceCalculationSerializer(serializers.Serializer):
    cart_list = serializers.ListField(allow_empty=False, allow_null=False)
    coupon_code = serializers.CharField(required=False)

    def validate(self, attrs):
        # Validate coupon code if provided
        coupon_code = attrs.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
            except Coupon.DoesNotExist:
                raise serializers.ValidationError({'coupon_code': [_('Coupon not found.')]})
        return attrs


class OrderPriceCalculationSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True, allow_null=False, )


