from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import Cart


def validate_cart_creation(attrs, user):
    product = attrs.get('product')
    product_variant = attrs.get('product_variant')
    cart = Cart.objects.filter(product=product, product_variant=product_variant, user=user)
    if product.has_variant:
        if not product_variant:
            raise serializers.ValidationError({"detail": [_('Please provide a product variant.'), ]})
        if product_variant:
            if product_variant.product != product:
                raise serializers.ValidationError(
                    {"detail": [_('The selected product variant does not belong to the specified product.'), ]}
                )
        if cart.exists():
            raise serializers.ValidationError(
                {"detail": [_(f'The {product.get_product_name} is already in your cart'), ]}
            )
    else:
        if product_variant:
            raise serializers.ValidationError({"detail": [_('This product does not have variants.'), ]})
    return attrs
