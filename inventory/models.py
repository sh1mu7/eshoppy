from datetime import date

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from coreapp.base import BaseModel
from inventory import constants
from inventory.utils import product_utils


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE, related_name='brand_logo')
    position = models.IntegerField()
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
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    unit_name = models.CharField(max_length=50)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2)
    has_variant = models.BooleanField(default=False)
    product_specification = models.JSONField()
    reward_points = models.IntegerField(default=0)
    stock_status = models.SmallIntegerField(choices=constants.StockStatusChoices.choices,
                                            default=constants.StockStatusChoices.IN_STOCK)
    total_review = models.IntegerField(default=0, editable=False)
    average_rating = models.FloatField(default=0.0, editable=False)
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

    @cached_property
    def get_product_name(self):
        if self.has_variant:
            return f"{self.name} - {self.product_variants.first().variant_option.name}"
        else:

            return self.name

    @cached_property
    def get_product_review(self):
        return self.productreview_set.filter(product=self.id).values_list('id', flat=True)

    @cached_property
    def get_vat_amount(self):
        return self.vat

    @cached_property
    def has_stock(self):
        if self.quantity > 0:
            return True
        return False

    @cached_property
    def get_promotion_status(self):
        today = date.today()
        if self.promotions_start_date and self.promotions_expiry_date:
            if self.promotions_start_date <= today <= self.promotions_expiry_date:
                return 'running'
            elif today > self.promotions_expiry_date:
                return 'expired'
        return 'coming soon'

    def save(self, *args, **kwargs):
        self.generate_slug('name')
        self.product_code = product_utils.generate_product_code()
        self.average_rating = round(self.average_rating, 2)
        super(Product, self).save(**kwargs)


class ProductVariant(BaseModel):
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='product_variants')
    variant_option = models.ForeignKey('inventory.VariantOption', on_delete=models.CASCADE,
                                       related_name='product_variant_option')
    code = models.CharField(max_length=15)
    quantity = models.IntegerField()
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)

    @cached_property
    def has_stock(self):
        if self.quantity > 0:
            return True
        return False


class ProductReview(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='product_review')
    rating = models.IntegerField()
    comment = models.TextField()
    images = models.ManyToManyField('coreapp.Document')
    order_item = models.ForeignKey('sales.OrderItem', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        rating_count = self.product.total_review
        average_rating = self.product.average_rating
        total_ratings = (average_rating * rating_count) + self.rating
        self.product.total_review += 1
        self.product.average_rating = total_ratings / self.product.total_review
        self.product.save()
        self.product.refresh_from_db()
        super(ProductReview, self).save(**kwargs)
