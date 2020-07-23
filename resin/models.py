from django.db import models


# Create your models here.

class Material(models.Model):
    M_id = models.CharField(max_length=50)
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

    last_update = models.DateTimeField(auto_now=True)
