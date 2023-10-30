from django.conf import settings
from django.db import models
from coreapp.base import BaseModel



class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('inventory.VariantOption', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)


class WishList(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
