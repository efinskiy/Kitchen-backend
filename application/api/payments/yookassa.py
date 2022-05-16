from datetime import datetime
from flask import current_app, request
import requests
from .config import YOOKASSA_CONFIG as config
import hmac

from yookassa import Configuration
from yookassa import Payment
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt
from yookassa.domain.models.receipt_item import ReceiptItem
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

Configuration.configure(secret_key=config.secretkey, account_id=config.account_id)

def createPayment(items, value, email, order_id):
    receipt_items = []

    for item in items:
        receipt_items.append(
            ReceiptItem({
                "description": item.title,
                "quantity": item.amount,
                "amount": {
                    "value": item.summ,
                    "currency": Currency.RUB
                },
                "vat_code": 1
            })
        )

    receipt = Receipt()
    receipt.customer = {'email': email}
    receipt.items = receipt_items

    builder = PaymentRequestBuilder()
    builder.set_amount({"value": value, "currency": Currency.RUB}) \
        .set_confirmation({
            "type": ConfirmationType.REDIRECT,
            "return_url": "https://stolovaya.online"
        })\
        .set_capture(False)\
        .set_description(f"Заказ №{order_id}")\
        .set_metadata({
            "orderNumber": order_id
        })\
        .set_receipt(receipt)
    
    request = builder.build()

    res = Payment.create(request)
