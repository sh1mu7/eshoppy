from inventory.models import VariantOption, ProductVariant


def create_product_variants(product, variants_data):
    for variant_item in variants_data:
        variant_option = variant_item.pop('variant_option').id
        variant = VariantOption.objects.get(id=variant_option)
        ProductVariant.objects.create(product=product, variant_option=variant, **variant_item)


def update_product_variants(instance, product_variants):
    for variant_data in product_variants:
        variant_id = variant_data.get('id', None)
        if variant_id:
            product_variant = ProductVariant.objects.filter(id=variant_id, product=instance).first()
            if product_variant:
                for attr, value in variant_data.items():
                    setattr(product_variant, attr, value)
                product_variant.save()
            else:
                pass
        else:
            ProductVariant.objects.create(product=instance, **variant_data)
