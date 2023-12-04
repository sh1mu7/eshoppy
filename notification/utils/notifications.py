import logging

from firebase_admin import messaging

from orders.constants import OUT_FOR_DELIVERY
from stores.models import StoreInvoice
from .constants import DELIVERY_BOY, NEW_ORDER_FROM_CUSTOMER, REQUEST_ACCEPTED_BY_RIDER
from .firebase import get_db_ref
from .models import User

logger = logging.getLogger(__name__)


def new_order_notification(order):
    data = {
        "msg": f"Your order {order.invoice_no} has been posted successfully",
        "date": str(order.created_at),
        "is_read": False
    }
    ref = get_db_ref().child(str(order.user.id)).child("notifications")
    ref.push(data)
    invoices = StoreInvoice.objects.filter(order=order)
    for invoice in invoices:
        data = {
            "msg": f"Congratulations!You have a new order {invoice.order.invoice_no}",
            "date": str(order.created_at),
            "is_read": False
        }
        store_ref = get_db_ref().child(str(invoice.store.owner.id)).child("notifications")
        store_ref.push(data)
        token = invoice.store.owner.device_id
        if token is not None:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Congratulations!",
                    body=f"You have a new order {invoice.order.invoice_no}",
                ),
                data={
                    "invoice_no": str(invoice.id),
                    "customer_name": str(invoice.order.user.get_name),
                    "notification_type": str(NEW_ORDER_FROM_CUSTOMER)
                },
                token=token,
            )
            try:
                messages = [message, ]
                response = messaging.send_all(messages)
            except Exception as e:
                logger.error(f"Error {e} happened while creating order")

    # invoices = StoreInvoice.objects.filter(order=order)
    # for invoice in invoices:
    #     data = {
    #         "msg": f"Your order {invoice.order.invoice_no} is {invoice.order.get_status_display()}",
    #         "date": str(order.created_at),
    #         "is_read": False
    #     }
    #     store_ref = get_db_ref().child(str(invoice.store.owner.id)).child("notifications")
    #     store_ref.push(data)


def shipment_request_notification(shipment_req):
    data = {
        "shop_name": shipment_req.store.name,
        "order_id": shipment_req.store_invoice.order.id,
        "invoice_no": shipment_req.store_invoice.order.invoice_no,
        "invoice_id": shipment_req.store_invoice.id,
        "store_owner_id": shipment_req.store.owner.id,
        "from": str(shipment_req.store.address),
        "to": str(shipment_req.address),
        'request_id': shipment_req.id
    }
    ref = get_db_ref().child("shipment_request/")
    # if bool(ref.order_by_child('order_id').equal_to(shipment_req.store_invoice.order.id).get()):
    if bool(ref.order_by_child('invoice_id').equal_to(shipment_req.store_invoice.id).get()):
        # UPDATE record with existing store_invoice_id
        child_key = list(ref.order_by_child('invoice_id').equal_to(shipment_req.store_invoice.id).get())[0]
        print(f"child_key --- {child_key}")
        ref.child(child_key).update({"request_id": shipment_req.id})
        print(f"shipment request firebase id before -- {shipment_req.firebase_id}")
        shipment_req.firebase_id = child_key
        shipment_req.save()
        print(f"shipment request firebase id after -- {shipment_req.firebase_id}")
    else:
        print("create")
        reqId = ref.push().key
        print(f"refId -- {reqId}")
        shipment_req.firebase_id = reqId
        ref.child(reqId).set(data)
        shipment_req.save()


# this is required to bring the app foreground
def shipment_request_push_notification(shipping_req):
    title = "New Delivery Request"
    msg = f"{shipping_req.store.name} is looking for a rider."

    # store = Store.objects.get(id=shipping_req.store.name)
    # gcd_formula = "6371 * acos(least(greatest(\
    #                                           cos(radians(%s)) * cos(radians(lat)) \
    #                                           * cos(radians(lng) - radians(%s)) + \
    #                                           sin(radians(%s)) * sin(radians(lat)) \
    #                                           , -1), 1))"
    # distance_raw_sql = RawSQL(
    #     gcd_formula,
    #     (store.lat, store.lng, store.lat)
    # )
    # qs = User.objects.filter(
    #     is_active=True, type=DELIVERY_BOY
    # ).select_related('location').annotate(distance=distance_raw_sql)
    # users = qs.filter(distance__lt=store.store_range, device_id__isnull=False).values('device_id')

    users = User.objects.filter(is_active=True, type=DELIVERY_BOY).values('device_id')

    tokens = []

    for q in users:
        tokens.append(str(q['device_id']))

    get_db_ref()
    messages = []
    for token in tokens:
        messages.append(
            messaging.Message(
                data={
                    "to": str(token),
                    "body": msg,
                    "title": title,
                },
                notification=messaging.Notification(title, msg),
                token=token,
            )
        )
    response = messaging.send_all(messages)
    print(response)
    logger.error(f"{response.success_count} shipment request push notification messages were sent successfully")


def delete_shipment_request_notification(firebaase_id):
    print('inside delete shipment notifications')
    try:
        ref = get_db_ref().child("shipment_request").child(firebaase_id).delete()
        # print(f"req_id -- {req_id}")
        # ref = get_db_ref().child("shipment_request").order_by_child('invoice_id').equal_to(req_id).get()
        # for k in ref:
        #     print(f'k -- {k}')
        #     get_db_ref().child("shipment_request").child(k).delete()
    except Exception as e:
        logger.error(f" in delete shipment request Exception  -- {e} ")


def push_notification(title, msg, tokens):
    """
    :param title: Title of notification
    :param msg: Message or body of notification
    :param tokens: Tokens of the users who will receive this notification
    :return:
    """
    chunks = [tokens[i:i + 500] for i in range(0, len(tokens), 500)]
    for chunk in chunks:
        messages = []
        for token in chunk:
            messages.append(
                messaging.Message(
                    notification=messaging.Notification(title, msg),
                    token=token,
                )
            )
        response = messaging.send_all(messages)


def shipment_accept_notification(notification_data, shipment):
    store_owner = User.objects.get(id=shipment.store.owner.id)
    ref = get_db_ref().child(str(store_owner.id)).child("shipment")
    ref.push().set(notification_data)

    token = store_owner.device_id
    if token is not None:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Congratulations!",
                body=f"You order {shipment.store_invoice.order.invoice_no}",
            ),
            data={
                "store_invoice_id": shipment.store_invoice.id,
                "store_address": shipment.store.address,
                "user_address": str(shipment.store_invoice.order.address.address),
                "delivery_boy_image": str(shipment.user.image.url),
                "delivery_boy_name": shipment.user.get_name,
                "delivery_boy_number": shipment.user.username,
                "status": OUT_FOR_DELIVERY,
                "notification_type": str(REQUEST_ACCEPTED_BY_RIDER)
            },
            token=token,
        )
        try:
            messages = [message, ]
            response = messaging.send_all(messages)
        except Exception as e:
            logger.error(f"Error {e} happened while sending shipment request acceptance notification to store owner")
