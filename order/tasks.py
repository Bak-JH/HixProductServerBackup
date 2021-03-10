from celery import Celery, shared_task
from django_celery_beat.models import PeriodicTask
from .utils import *
from .models import BillingInfo
import uuid
import time

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
                        
            crontab_date = ('*','*','*',str(datetime.datetime.today().day),'*')
            reserve_result = reserve_billing(billing_id, policy, target_serial,
                                                userinfo, crontab_date)
            return result['receipt_url']
        else:
            BillingInfo.objects.get(billing_key=billing_id).delete()
            schedule = get_or_create_crontab((time.strftime('%H'),time.strftime('%M'),'*','*'))
            task = PeriodicTask.objects.create(name='Billing_pended_'+ billing_id)
            task.crontab = schedule
            task.expires = time.timezone.now() + timedelta(days=3)
    return None