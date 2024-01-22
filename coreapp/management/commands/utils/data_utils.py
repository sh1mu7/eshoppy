import json
import os

from coreapp.models import Document
from inventory.models import Category

BRAND_DATA = 'data/data.json'


def load_json(name):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), name)
    with open(file_path, encoding="utf8") as f:
        data = json.load(f)
    return data


def load_category_json():
    categories_json = load_json(BRAND_DATA)
    categories = []
    for data in categories_json:
        category = Category(

            name=data['name'],
            image=Document.objects.get(id=data['image']),  # Replace 'logo_id' with the actual key in your JSON
            product_count=data['product_count'],
            slug=data['slug'],
            is_active=data['is_active']
        )
        categories.append(category)
    Category.objects.bulk_create(categories)
