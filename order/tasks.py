from celery import Celery, shared_task
from django_celery_beat.models import PeriodicTask
from .utils import *
from .models import BillingInfo
import uuid
import time

app = Celery('tasks', broker='pyamqp://guest:guest@localhost//')

@shared_task(max_retries=3)
def do_payment(billing_id, product_name, price, serial_number, userinfo, isSave):
    bootpay = load_bootpay()
    if bootpay.response['status'] is 200:
        result = billing_bootpay(
                    bootpay, 
                    billing_id, 
                    product_name, 
                    price,
                    str(uuid.uuid4()),
                    userinfo
                )

        if result is not None:
            billinginfo = save_billingInfo(isSave, billing_id, result['card_name'], result['card_no'], userinfo['username'])
            save_receipt(result['receipt_id'], result['receipt_url'], result['purchased_at'], serial_number, billinginfo)
            send_receipt(result['receipt_url'],
                        userinfo['email'], serial_number)
                        
            crontab_date = ('*','*','*',str(datetime.datetime.today().day),'*')
            reserve_billing(billing_id, product_name, price, serial_number,userinfo, crontab_date)

            try:
                pended_task = PeriodicTask.objects.get(name='Pended_Billing_'+billing_id)
                pended_task.delete()
            except:
                pass
            return result['receipt_url']
        else:
            reserve_pended_billing(billing_id, product_name, price, serial_number, userinfo)

            try:
                pended_task = PeriodicTask.objects.get(name='Pended_Billing_'+billing_id)
                if pended_task.expires <= datetime.datetime.now(pended_task.expires.tzinfo):
                    billing_task = PeriodicTask.objects.get(name='Billing_'+billing_id)
                    print(billing_task)
                    billing_task.delete()
                    pended_task.delete()
            except Exception as e:
                print(e)
                pass

        try:
            pended_task = PeriodicTask.objects.get(name='Pended_Billing_'+billing_id)
            if pended_task.expires <= datetime.datetime.now(pended_task.expires.tzinfo):
                billing_task = PeriodicTask.objects.get(name='Billing_'+billing_id)
                print(billing_task)
                billing_task.delete()
                pended_task.delete()
        except Exception as e:
            print(e)
            pass

    else:
        reserve_pended_billing(billing_id, product_name, price, serial_number, userinfo)
    return None