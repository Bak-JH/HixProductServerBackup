from celery import Celery, shared_task
from django_celery_beat.models import PeriodicTask
from .utils import *
from .models import BillingInfo, PricingPolicy, RegularPayment
import uuid
import time

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@shared_task(max_retries=3)
def do_payment(regular_id):
    try:
        payment_info = RegularPayment.objects.get(id=regular_id)
        billing_key = payment_info.billing_info.billing_key
        product_name = payment_info.policy.product.name
        price = payment_info.policy.price
        owner = payment_info.owner
        serial = payment_info.serial

    except:
        reserve_pended_billing(regular_id)
        handle_billing_error(regular_id)

        return None

    bootpay = load_bootpay()
    if bootpay.response['status'] is 200:
        result = billing_bootpay(
                    bootpay, 
                    billing_key, 
                    product_name, 
                    price,
                    str(uuid.uuid4()),
                    {'username': owner.username, 'email': owner.email}
                )

        if result is not None:
            save_receipt(result['receipt_id'], result['receipt_url'], result['purchased_at'], serial.serial_number, payment_info.billing_info)
            send_receipt(result['receipt_url'],
                        owner.email, serial.serial_number)
            
            crontab_date = (str(datetime.datetime.now().minute),
                            str(datetime.datetime.now().hour),
                            '*',
                            str(datetime.datetime.today().day),
                            '*')
            reserve_billing(crontab_date, regular_id)

            try:
                pended_task = PeriodicTask.objects.get(name='Pended_Billing_'+regular_id)
                pended_task.delete()
            except:
                pass
            return result['receipt_url']
        else:
            reserve_pended_billing(regular_id)
            handle_billing_error(regular_id)
    else:
        reserve_pended_billing(regular_id)
    return None