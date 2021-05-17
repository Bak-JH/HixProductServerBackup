import datetime
from time import timezone
from lib.BootpayApi import BootpayApi
from .models import BillingInfo, PaymentHistory
from product.models import ProductSerial
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from .models import RegularPayment
import json


def load_bootpay():
    bootpay = BootpayApi('59a4d32b396fa607c2e75e00', 't3UENPWvsUort5WG0BFVk2+yBzmlt3UDvhDH2Uwp0oA=')
    bootpay.response = bootpay.get_access_token()
    return bootpay

def billing_bootpay(bootpay, billing_id, product_name, price, order_id, userinfo):
    result = bootpay.subscribe_billing(
                        billing_id, product_name, 
                        price,      order_id, 
                        [],         userinfo
                    )
    return result['data'] if result['status'] is 200 else None



def save_billingInfo(isSave, billing_id, card_name, card_number, user):
    # if len(card_number) == 16:
    #     do something
    part_1 = card_number[:6]
    part_2 = card_number[12:]
    
    card_number = part_1 + "******" + part_2

    result, _ = BillingInfo.objects.get_or_create(billing_key=billing_id, 
                                                card_name=card_name, 
                                                card_number=card_number,
                                                owner=user)

    ### this part is for save option ###
    # if isSave != "true":
    #     to_delete = BillingInfo.objects.get(billing_key=result.billing_key)
    #     to_delete.delete()

    return result

def create_new_serial(product):
    return ProductSerial.objects.create(product=product, owner=None)

def save_receipt(receipt_id, receipt_url, purchased_at, serial_number, billinginfo):
    purchased_at = purchased_at if purchased_at is not None else None
    serial = ProductSerial.objects.get(serial_number=serial_number)

    return PaymentHistory.objects.create(receipt_id=receipt_id, 
                                         receipt_url=receipt_url, 
                                         date=purchased_at, 
                                         serial=serial,
                                         billing_info = billinginfo)

def send_receipt(url, email, serial_key):
    msg_html = render_to_string('order/receipt.html', 
                                {'receipt_url': url, 'serial_key': serial_key})

    result = send_mail(
        'Receipt from HiX',
        '',
        'HiX<support@hix.co.kr>',
        [email],
        html_message=msg_html
    )

    return result

def get_or_create_crontab(crontab_date):
    schedule, _ = CrontabSchedule.objects.get_or_create(
                                    minute=crontab_date[0],
                                    hour=crontab_date[1], 
                                    day_of_week=crontab_date[2], 
                                    day_of_month=crontab_date[3], 
                                    month_of_year=crontab_date[4]
                                )

    return schedule

# crontab_date is tuple
def reserve(crontab_date, task, args, name, expired_date=None):
    schedule = get_or_create_crontab(crontab_date)

    try:
        task, _ = PeriodicTask.objects.get_or_create(
                        crontab=schedule, name=name, 
                        task=task, args=args, expires=expired_date)
        return schedule

    except Exception as e:
        print(e)
        return None

def reserve_billing(crontab_date, regular_id):
    args = json.dumps([regular_id])
    return reserve(crontab_date, 
                    'order.tasks.do_payment', 
                    args, 'Billing_'+ regular_id)

def reserve_pended_billing(regular_id):
    args = json.dumps([regular_id])

    expire_date = datetime.datetime.now()+ datetime.timedelta(days=3)
    return reserve(['*','*','*','*','*'], 'order.tasks.do_payment', 
                    args, 'Pended_Billing_'+regular_id, expire_date)

def cancel_reserve(receipt_id):
    try:
        history = PaymentHistory.objects.get(receipt_id=receipt_id)
        billing_key = history.billing_info.billing_key
        PeriodicTask.objects.get(name='Billing_'+ billing_key).delete()
        history.refunded = True
        history.save()

        return history.receipt_url

    except Exception as e:
        print(e)
        raise e

def handle_billing_error(regular_id):
    regular = RegularPayment.objects.get(id=regular_id)
    msg_html = render_to_string('order/receipt.html', 
                                {'regular_id': regular.id})

    result = send_mail(
        'Your Subscription has a problem.',
        '',
        'HiX<support@hix.co.kr>',
        [regular.owner.email],
        html_message=msg_html
    )

    try:
        pended_task = PeriodicTask.objects.get(name='Pended_Billing_'+regular_id)
        if pended_task.expires <= datetime.datetime.now(pended_task.expires.tzinfo):
            billing_task = PeriodicTask.objects.get(name='Billing_'+regular_id)
            print(billing_task)
            billing_task.delete()
            pended_task.delete()
    except Exception as e:
        print(e)
        pass