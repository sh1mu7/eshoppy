from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from coreapp.base import BaseModel


class Wishlist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)

    @cached_property
    def get_product_name(self):
        return self.product.get_product_name

    @cached_property
    def get_product_price(self):
        return self.product.price

    @cached_property
    def get_product_variant(self):
        if self.product.product_variants.exists():
            variants = self.product.product_variants.all()
            variant_names = {variant.id for variant in variants}
            return variant_names
        else:
            return ["No Variant"]

    @cached_property
    def get_product_thumbnail(self):
        return self.product.get_thumbnail_url


class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    product_variant = models.ForeignKey('inventory.ProductVariant', on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey('inventory.VariantOption', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    @cached_property
    def get_product_name(self):
        return self.product.get_product_name

    @cached_property
    def get_product_price(self):
        return self.product.price

    @cached_property
    def get_product_thumbnail(self):
        return self.product.get_thumbnail_url

    @cached_property
    def get_product_variant_name(self):
        return self.product_variant.code

    @cached_property
    def get_product_variant_option_name(self):
        return self.variant.name
