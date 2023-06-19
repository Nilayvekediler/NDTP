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
from proxmoxer import ProxmoxAPI
import pyautogui
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

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

proxmox = ProxmoxAPI('192.168.1.104', user='root@pam', password='nıla123', verify_ssl=False)

def kkm(request):
    cluster_nodes = proxmox.cluster.resources.get(type='node')
    
    context = {
        'nodes': []
    }
    
    for node in cluster_nodes:
        node_data = {
            'node': node['node'],
            'cts': []
        }
        cts = proxmox.nodes(node['node']).lxc.get()
        for ct in cts:
            ct_data = {
                'id': ct['vmid'],
                'name': ct['name'],
                'status': ct['status']
            }
            node_data['cts'].append(ct_data)
        
        context['nodes'].append(node_data)

    return render(request, 'kkmHome.html', context)

def start_ct(request, node, ct_id):
    try:
        proxmox.nodes(node).lxc(ct_id).status.start.post()
        time.sleep(10) #eğer başladıysa yap bu bekleme yerine

        # chrome_window = pyautogui.getWindowsWithTitle("Google Chrome")[0]

        # chrome_window.activate()
        # target_url = "https://192.168.1.104:8006/#v1:0:=lxc%2F100:4:::::::"

        # pyautogui.hotkey("ctrl", "l")  
        # pyautogui.write(target_url) 
        # pyautogui.press("enter")  
        # pyautogui.hotkey("ctrl", "r")

        # python_script = "print('Hello, World!')"
        # attacksRun.run_python_script_on_ct(node, ct_id, python_script)
        #attacksRun.run_command_on_ct(node, ct_id, "python synFlood.py") #ÇALIŞIYOR

        #return HttpResponse("CT başlatıldı.")
        return HttpResponse("CT başlatıldı.")
    
    except proxmox.ResourceException as e:
        return HttpResponse("CT başlatma hatası: " + str(e))
    
def stop_ct(request, node, ct_id):
    try:
        proxmox.nodes(node).lxc(ct_id).status.stop.post()
        return HttpResponse("CT durduruldu.")
    except proxmox.ResourceException as e:
        return HttpResponse("CT durdurma hatası: " + str(e))
    


def botnet(request):
    return HttpResponseRedirect('https://192.168.1.104:8006/')

# def login_req(request):
#     if request.method == "POST":
#         username=request.POST["username"]
#         password=request.POST["password"]

#         user=authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return HttpResponseRedirect("home")
#         else:
#             return render(request, 'login.html', {"error":"username ya da parola yanlış"})
#     return render(request, 'login.html')

# def signin(request):
#     return render(request, 'signin.html')

# def users(request):
#     return render(request, 'signin.html')

def login_request(request):
    # if request.user.is_authenticated:
    #     return redirect("index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("userpage")
        else:
            return render(request, "login.html", {
                "error": "username ya da parola yanlış"
            })

    return render(request, "login.html")

def register_request(request):
    # if request.user.is_authenticated:
    #     return redirect("index")
        
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", 
                {
                    "error":"username kullanılıyor.",
                    "username":username,
                    "email":email,
                    "firstname": firstname,
                    "lastname":lastname
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "register.html", 
                    {
                        "error":"email kullanılıyor.",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname
                    })
                else:
                    user = User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
                    user.save()
                    return redirect("login")                    
        else:
            return render(request, "register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname
            })

    return render(request, "register.html")

def logout_request(request):
    logout(request)
    return redirect("index")


def userpage(request):
    return render(request, "userpage.html")


def monitoring(request):
    # return render(request, "monitoring.html")
    return HttpResponseRedirect('http://34.221.163.147')

