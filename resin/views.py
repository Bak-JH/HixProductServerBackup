import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers

from django.forms.models import model_to_dict

from resin.models import Material, PrintSetting
from product.models import Product



def update_check(request, printer_name):
    # materials = Material.objects.values("M_id","last_update")
    printer = get_object_or_404(Product, name=printer_name)

    data = serializers.serialize("json",Material.objects.filter(printer=printer), fields=('name','last_update'))
    print(data)
    return HttpResponse(data, content_type="application/json")

def download_all(request, printer_name):
    printer = get_object_or_404(Product, name=printer_name)
    main_dict = {}
    for mat in Material.objects.filter(printer=printer):
        mat_dict = {}
        for sett in PrintSetting.objects.filter(material=mat):
            data = serializers.serialize("json",[ sett, ])
            json_decoded = json.loads(data)
            json_decoded[0].pop('pk', None)
            json_decoded[0].pop('model', None)
            fields = json_decoded[0].pop('fields', None)
            mat_dict[sett.layer_height] = fields
        main_dict[mat.name] = mat_dict
    # data = serializers.ser ialize("json",Material.objects.all())
    jsonObj = json.dumps(main_dict)
    return HttpResponse(jsonObj, content_type="application/json")


# Create your views here.
