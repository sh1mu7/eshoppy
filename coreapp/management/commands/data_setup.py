from django.core.management.base import BaseCommand

from .utils import data_utils


class Command(BaseCommand):
    help = 'Custom Data'

    def handle(self, *args, **kwargs):
        data_utils.load_category_json()
