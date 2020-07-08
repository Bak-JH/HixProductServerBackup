import hashlib
from django.db import models
from django.contrib.auth.models import User
import uuid




# def create_hash(input):
#     hashSHA256 = hashlib.sha256()
#     hashSHA256.update(input)

#     hash = hashSHA256.hexdigest().upper()

#     return hash[:16]


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True, help_text="Name of the product")

class ProductSerial(models.Model):
    #Don't want to expose primary key to this table as serial number
    serial_number = models.UUIDField(default=uuid.uuid4, help_text='serial number generated with UUID4')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    expire_date = models.DateField(null=True, blank=True, help_text='Expiry date, if blank means does not expire.')
    #TODO: constraint to make sure {owner, product} is unique when owner is NOT NULL
