from django.test import TestCase
import uuid
from uuid import UUID
from django.contrib.auth.models import User
from django.utils import timezone
from django.core import mail
from .models import *
from .tasks import *
from .utils import *
from order.tasks import app
from product.models import Product
from django_celery_beat.models import CrontabSchedule, PeriodicTask


def toJson(self, o):
    if isinstance(o, UUID): return str(o)
    return toJson(self, o)

# Create your tests here.
class PaymentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.billing_id = '60176037238684001f8fb2f2'
        cls.price = 100000
        cls.order_id = toJson(cls, uuid.uuid4())
        cls.product = Product.objects.create(name='test')
        cls.user = User.objects.create_user('bootpaytest', 'test@tester.com', 'tester') 
        cls.receipt_id = []
        cls.receipt_url = []

    def setUp(cls):
        ProductSerial.objects.create(product=cls.product, owner=None)
        target_serial = ProductSerial.objects.create(product=cls.product, owner=None)
        policy = PricingPolicy.objects.create(product=cls.product, price=1000)


        userinfo = {'username': cls.user.username, 'email': cls.user.email}
        args = {'billing_id': cls.billing_id, 'policy': policy, 
            'target_serial': target_serial, 'userinfo': userinfo}
        schedule = CrontabSchedule.objects.create(
                                    minute='*',
                                    hour='*', 
                                    day_of_week='*', 
                                    day_of_month='*', 
                                    month_of_year='*'
                                )
        PeriodicTask.objects.create(crontab=schedule, 
                                    name='Billing_'+cls.billing_id, 
                                    task='order.tasks.do_payment',
                                    args=args)

    def test_1_bootpay_load(self):
        bootpay = load_bootpay()

        print("==================== test_bootpay_load ====================\n")
        print(bootpay.response, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(bootpay)

    def test_2_bootpay_billing(self):
        bootpay = load_bootpay()
        result = billing_bootpay(bootpay, self.billing_id, 
                                self.product.name, self.price, 
                                self.order_id,
                                {'username': self.user.username, 'email': self.user.email})
        
        print("==================== test_bootpay_billing ====================\n")
        print(result, '\n')
        self.receipt_id.append(result['receipt_id'])
        self.receipt_url.append(result['receipt_url'])
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_3_find_free_serial(self):
        result = find_free_serial(self.product)

        print("==================== test_find_free_serial ====================\n")
        print(result, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_4_billinginfo_save(self):
        result = save_billingInfo(self.billing_id, 'KB국민카드', '5365100000002395')

        print("==================== test_billinginfo_save ====================\n")
        print(result.billing_key, result.card_number, result.card_name, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_5_receipt_save(self):
        billinginfo = save_billingInfo(self.billing_id, 'KB국민카드', '5365100000002395')
        serial = find_free_serial(self.product)[0]
        result = save_receipt(''.join(self.receipt_id), ''.join(self.receipt_url), datetime.datetime.now(), serial, billinginfo)

        print("==================== test_receipt_save ====================\n")
        print(serial.serial_number)
        print(result.receipt_id, result.receipt_url, result.date, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_6_reserve(self):
        policy = PricingPolicy.objects.get(product=self.product)
        serial = find_free_serial(self.product)[0]
        userinfo = {'username': self.user.username, 'email': self.user.email}
        crontab_date = ('*','*','*',datetime.datetime.today().day,'*')

        result = reserve_billing(self.billing_id+'=', policy, serial, userinfo, crontab_date)
        print("==================== test_reserve ====================\n")
        print(result, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_7_refund(self):
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200:
            result = bootpay.cancel(self.receipt_id, '', 'tester', 'just')
        else:
            result = None

        print(self.receipt_id[0])
        r = cancel_reserve(self.receipt_id[0])

        print("==================== test_refund ====================\n")
        print(self.receipt_id)
        print(result, '\n')
        print(r, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertEqual(result['status'], 200)
        self.assertTrue(r)

    def test_8_sendmail(self):
        print("==================== test_sendmail ====================\n")
        print(send_receipt('https://bit.ly/3jM6Rf2', 'bakjh.6280@gmail.com', find_free_serial(self.product)[0]))
        print('--------------------------------------------------------------\n\n')
        
        self.assertEqual(len(mail.outbox), 1)
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Receipt from HiX')

    def 

