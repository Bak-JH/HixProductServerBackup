from order.views import *
from django.test import TestCase, Client
from lib.BootpayApi import BootpayApi
import uuid
from uuid import UUID
from django.contrib.auth.models import User
from django.utils import timezone


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
        ProductSerial.objects.create(product=cls.product, owner=None)

    def test_bootpay_load(self):
        bootpay = load_bootpay()

        print("==================== test_bootpay_load ====================\n")
        print(bootpay.response, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(bootpay)

    def test_bootpay_billing(self):
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

    def test_find_free_serial(self):
        result = find_free_serial(self.product)

        print("==================== test_find_free_serial ====================\n")
        print(result, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_billinginfo_save(self):
        result = save_billingInfo(self.billing_id, 'KB국민카드', '5365100000002395')

        print("==================== test_billinginfo_save ====================\n")
        print(result.billing_key, result.card_number, result.card_name, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertIsNotNone(result)

    def test_receipt_save(self):
        serial = find_free_serial(self.product)[0]
        result = save_receipt(''.join(self.receipt_id), ''.join(self.receipt_url), timezone.now(), serial.serial_number)

        print("==================== test_receipt_save ====================\n")
        print(serial.serial_number)
        print(result.receipt_id, result.receipt_url, result.date, '\n')
        print('--------------------------------------------------------------\n\n')

        self.receipt_id.append(result.receipt_id)
        self.assertIsNotNone(result)

    def test_refund(self):
        bootpay = load_bootpay()
        if bootpay.response['status'] is 200:
            result = bootpay.cancel(self.recipt_id, '', 'tester', 'just')
        else:
            result = None

        print("==================== test_refund ====================\n")
        print(self.recipt_id)
        print(result, '\n')
        print('--------------------------------------------------------------\n\n')

        self.assertEqual(result['status'], 200)
