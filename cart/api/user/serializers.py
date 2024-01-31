from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from inventory.models import ProductVariant
from sales.models import Coupon
from ...models import Wishlist, Cart
from ...utils import validate


class SetField(serializers.Field):
    def to_representation(self, obj):
        return obj


class UserWishlistListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='get_product_name', read_only=True)
    product_thumbnail = serializers.CharField(source='get_product_thumbnail', read_only=True)
    product_price = serializers.CharField(source='get_product_price', read_only=True)
    product_variants = SetField(source='get_product_variant', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'product_name', 'product_price', 'product_thumbnail', 'product_variants')


class UserWishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('user', 'product')
        read_only_fields = ('user',)

    def validate(self, attrs):
        product = attrs.get('product')
        wishlist = Wishlist.objects.filter(product=product, user=self.context['request'].user)
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
    variant_name = serializers.CharField(source='get_product_variant_name', read_only=True)
    variant_option_name = serializers.CharField(source='get_product_variant_option_name', read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id', 'product', 'product_name', 'product_thumbnail', 'product_price', 'variant', 'variant_name',
            'product_variant', 'variant_option_name', 'quantity'
        )

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
        fields = ('id', 'user', 'product', 'product_variant')
        read_only_fields = ('user',)

    def validate(self, attrs):
        user = self.context.get('request').user if self.context.get('request') and self.context.get(
            'request').user.is_authenticated else None
        validated_attrs = validate.validate_cart_creation(attrs, user)
        return validated_attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.create(**validated_data, user=user, quantity=1)
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


class CartItemQuantitySerializer(serializers.Serializer):
    cart_item = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartPriceCalculationSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(allow_null=True, required=False)
    items = serializers.ListField(
        child=CartItemQuantitySerializer()
    )

    def validate(self, attrs):
        coupon_code = attrs.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
            except Coupon.DoesNotExist:
                raise serializers.ValidationError({'coupon_code': [_('Coupon not found.')]})
        return attrs


class OrderPriceCalculationSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True, allow_null=False, )
