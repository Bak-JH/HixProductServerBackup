from django.shortcuts import render
from django.conf import settings
from .forms import AddResinForm
from resin.models import Material
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

@login_required
@permission_required('management.edit_resin', login_url="services.hix.co.kr/accounts/login", raise_exception=True)
def add_resinInfo(request):
    # check user doens't already own the product
    if request.method == "POST":
        try:
            resin_info = Material.objects.get(M_id=request.POST['M_id'])
            form = AddResinForm(request.POST, resin=resin_info)
        except Material.DoesNotExist:
            form = AddResinForm(request.POST, resin=request)
        except:
            return HttpResponseNotFound()

        if form.is_valid():
            register_product_serial = Material.objects.create(**form.cleaned_data)
            register_product_serial.save()
            return render(request, 'management/add_resin.html', {'form': form})
    else:
        form = AddResinForm(resin=request)
    return render(request, 'management/add_resin.html', {'form': form})
