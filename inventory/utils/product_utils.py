import string
import random


def generate_product_code():
    random_number = random.randint(100000, 999999)
    return f"P-{random_number}"
