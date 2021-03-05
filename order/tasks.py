from celery import Celery, shared_task
from django_celery_beat.models import PeriodicTask, PeriodicTasks
from .utils import *
from .models import BillingInfo
from product.models import Product
import uuid
from django.core import serializers

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@shared_task()
def do_payment(billing_id, policy, target_serial, userinfo):
    bootpay = load_bootpay()
    if bootpay.response['status'] is 200:
        result = billing_bootpay(
                    bootpay, 
                    billing_id, 
                    policy.product.name, 
                    policy.price,
                    str(uuid.uuid4()),
                    userinfo
                )

        if result is not None:
            billinginfo = save_billingInfo(billing_id, result['card_name'], result['card_no'])
            save_receipt(result['receipt_id'], result['receipt_url'],
                        result['purchased_at'], target_serial, billinginfo)
            send_receipt(result['receipt_url'], 
                        userinfo['email'], target_serial.serial_number)
            return result['receipt_url']
    return None
