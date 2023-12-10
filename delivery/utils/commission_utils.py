from decimal import Decimal
from coreapp.utils.twilio_utils import get_system_settings

settings_object = get_system_settings()


def get_commission_amount(amount):
    return amount * Decimal(settings_object.delivery_commission / 100)
