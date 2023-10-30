import string
import random


def generate_product_code(product_name, brand_name, category_name):
    brand_initial = brand_name[:2].lower() if brand_name else ''
    category_initials = ''.join(word[:2] for word in category_name.lower().split())
    name_without_spaces = ''.join(product_name.lower().split())
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    product_code = f"{brand_initial}-{category_initials}-{name_without_spaces}-{random_string}"
    return product_code
