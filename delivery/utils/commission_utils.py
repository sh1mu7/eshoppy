from decimal import Decimal
from utility.utils.settings_utils import settings_object


def get_commission_amount(amount):
    return amount * Decimal(settings_object.delivery_commission / 100)
