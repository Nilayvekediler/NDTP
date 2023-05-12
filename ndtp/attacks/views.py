from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import AttacksCategory
from .models import Attacks
from django.http import Http404
from . import attacksRun
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import time

input_gizli = 0


def index(request):
    return render(request, 'home.html')


def attacksCategory(request):
    # template = loader.get_template('attacksCategory.html')
    context = {
        'attacksCategory_list': AttacksCategory.objects.all()
    }
    # return HttpResponse(template.render(context,request))
    return render(request, 'attacksCategory.html', context)


def attacks(request, attacksId):
    global input_gizli
    attacks = Attacks.objects.get(pk=attacksId)
    context = {
        'attacks_list': [attacks]
    }

    if request.method == 'POST':
        input_gizli = request.POST.get('gizli')
        input_ipOrDns = request.POST.get('input_ip')
        input_port = int(request.POST.get('input_port', 0))

        while input_gizli != "1":
            attacksRun.triggerAttack(
                attacks.attackName, input_ipOrDns, input_port)
            input_gizli = request.POST.get('gizli')
            time.sleep(0.1)
  
        
        print("yollama işlemi bitti.")
          

    return render(request, 'modal.html', context)


def attacksCategoryDetails(request, attacksCategoryId):
    try:
        attacks_category = AttacksCategory.objects.get(pk=attacksCategoryId)
        attacks_list = Attacks.objects.filter(attackCat=attacks_category)
        context = {
            'attacksCategoryDetails_list': attacks_category,
            'attacks_list': attacks_list
        }
    except AttacksCategory.DoesNotExist:
        raise Http404("Saldırı Sınıflandırılması Bulunamadı!")
    return render(request, 'attacksCategoryDetails.html', context)


def attacksDetails(request, attacksId):
    return HttpResponse("Attack Detayı: "+str(attacksId))

def kkm(request):
    return render(request, 'kkmHome.html')

def botnet(request):
    return HttpResponseRedirect('https://192.168.1.104:8006/')