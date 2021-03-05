from lib.BootpayApi import BootpayApi
from .models import BillingInfo, PaymentHistory
from product.models import ProductSerial
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import datetime


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

def save_billingInfo(billing_id, card_name, card_number):
    card_number = card_number[-4:]
    result, _ = BillingInfo.objects.get_or_create(billing_key=billing_id, 
                                                card_name=card_name, 
                                                card_number=card_number)
    return result

def find_free_serial(product):
    return ProductSerial.objects.filter(product=product, owner=None)

def save_receipt(receipt_id, receipt_url, purchased_at, serial, billinginfo):
    purchased_at = purchased_at if purchased_at is not None else None
    serial = ProductSerial.objects.get(serial_number=serial.serial_number)
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

# crontab_date is tuple
def reserve(crontab_date, task, args, name):
    schedule, _ = CrontabSchedule.objects.get_or_create(
                                    minute=crontab_date[0],
                                    hour=crontab_date[1], 
                                    day_of_week=crontab_date[2], 
                                    day_of_month=crontab_date[3], 
                                    month_of_year=crontab_date[4]
                                )
    try:
        PeriodicTask.objects.create(crontab=schedule, name=name, task=task, args=args)
        return schedule

    except Exception as e:
        print(e)
        return None

def reserve_billing(billing_id, policy, target_serial, userinfo, crontab_date):
    args = {'billing_id': billing_id, 'policy': policy, 
            'target_serial': target_serial, 'userinfo': userinfo}

    return reserve(crontab_date, 'order.tasks.do_payment', args, 'Billing_'+ billing_id)

def cancel_reserve(receipt_id):
    try:
        history = PaymentHistory.objects.get(receipt_id=receipt_id)
        billing_key = history.billing_info.billing_key
        PeriodicTask.objects.get(name='Billing_'+ billing_key).delete()
        history.refunded = True
        history.save()
        BillingInfo.objects.get(billing_key=billing_key).delete()

        return True

    except Exception as e:
        print(e)
        return False