from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core import serializers

from django.forms.models import model_to_dict

from .models import Material


def test(request):
    print(request.body)
    return HttpResponse(status=200)

def update_check(request):
    # materials = Material.objects.values("M_id","last_update")
    data = serializers.serialize("json",Material.objects.all(), fields=('M_id','last_update'))
    print(data)
    print(type(data))
    # return JsonResponse(list(data),safe=False)
    return HttpResponse(data, content_type="application/json")

def download_all(request):
    data = serializers.serialize("json",Material.objects.all())
    return HttpResponse(data, content_type="application/json")

def download(request,materialName):
	material = get_object_or_404(Material,M_id=materialName)
    
	material_dic = model_to_dict(material)

	return JsonResponse(material_dic)

# Create your views here.
