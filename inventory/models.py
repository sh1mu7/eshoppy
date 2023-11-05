from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from coreapp.base import BaseModel
from inventory import constants
from inventory.utils import product_utils


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE, related_name='brand_logo')
    order = models.IntegerField()
    slug = models.SlugField(editable=False, unique=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.generate_slug('name')
        super(Brand, self).save(**kwargs)


class Category(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, )
    name = models.CharField(max_length=100)
    image = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE, related_name='category_image')
    slug = models.SlugField(editable=False, unique=True, null=True, blank=True)
    product_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_product_count(self):
        return self.product_set.count()

    def save(self, *args, **kwargs):
        self.generate_slug('name')
        super(Category, self).save(**kwargs)


class VariantGroup(BaseModel):
    group_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)


class VariantOption(BaseModel):
    group = models.ForeignKey('inventory.VariantGroup', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)


class Product(BaseModel):
    name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=8, editable=False, unique=True, null=False, blank=False)
    slug = models.SlugField(editable=False, unique=True, null=True, blank=True)
    thumbnail = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE, related_name='product_thumbnail')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, )
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    has_promotion = models.BooleanField(default=False)
    promotional_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, )
    promotions_start_date = models.DateField(null=True)
    promotions_expiry_date = models.DateField(null=True)
    quantity = models.PositiveIntegerField(default=0)
    vat = models.DecimalField(max_digits=5, decimal_places=2)
    unit_name = models.CharField(max_length=50)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2)
    has_variant = models.BooleanField(default=False)
    product_specification = models.JSONField()
    reward_points = models.IntegerField(default=0)
    stock_status = models.SmallIntegerField(choices=constants.StockStatusChoices.choices,
                                            default=constants.StockStatusChoices.IN_STOCK)
    total_review = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    images = models.ManyToManyField('coreapp.Document', related_name='product_images')

    @cached_property
    def get_brand_name(self):
        return self.brand.name

    @cached_property
    def get_category_name(self):
        return self.category.name

    @cached_property
    def get_parent_category_name(self):
        return self.category.parent.name

    @cached_property
    def get_thumbnail_url(self):
        return self.thumbnail.get_url

    def save(self, *args, **kwargs):
        self.generate_slug('name')
        self.product_code = product_utils.generate_product_code()
        super(Product, self).save(**kwargs)


class ProductVariant(BaseModel):
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='product_variants')
    variant_option = models.ForeignKey('inventory.VariantOption', on_delete=models.CASCADE,
                                       related_name='product_variant_option')
    code = models.CharField(max_length=15)
    quantity = models.IntegerField()
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)


class ProductReview(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    images = models.ManyToManyField('coreapp.Document')
    order_item = models.ForeignKey('sales.OrderItem', on_delete=models.SET_NULL, null=True, blank=True)

# TODO: Please check this inventory module
