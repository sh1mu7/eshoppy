from random import randint


def generate_order_reference():
    from sales.models import Order
    reference = f"ORDER-{randint(0, 100000)}"
    while Order.objects.filter(invoice_no=reference).exists():
        reference = f"ORDER-{randint(0, 100000)}"
    return reference
