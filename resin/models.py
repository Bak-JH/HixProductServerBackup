from django.db import models
from product.models import Product


class Material(models.Model):
    name = models.CharField(max_length=50)
    printer = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    last_update = models.DateTimeField(auto_now=True)

# # Create your models here.
# class LayerHeight(models.Model):
#     layer_height = models.FloatField(blank=True, default=0)

class PrintSetting(models.Model):
    # layer_height = models.ForeignKey(LayerHeight, on_delete=models.SET_NULL, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=False, blank=False)
    layer_height = models.FloatField(blank=True, default=0)
    bed_curing_layer = models.IntegerField(blank=True, default=0)
    bed_curing_time = models.IntegerField(blank=True, default=0)
    curing_time = models.IntegerField(blank=True, default=0)
    layer_delay = models.IntegerField(blank=True, default=0)
    z_hop_height = models.IntegerField(blank=True, default=0)
    max_speed = models.IntegerField(blank=True, default=0)
    init_speed = models.IntegerField(blank=True, default=0)
    up_accel_speed = models.IntegerField(blank=True, default=0)
    up_decel_speed = models.IntegerField(blank=True, default=0)
    down_accel_speed = models.IntegerField(blank=True, default=0)
    down_decel_speed = models.IntegerField(blank=True, default=0)
    contraction_ratio = models.FloatField(blank=True, default=0)
    led_offset = models.FloatField(blank=True, default=100)
    class Meta:
        unique_together = (('layer_height', 'material'),)

