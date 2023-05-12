from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('attacksCategory',views.attacksCategory, name='attacksCats'),
    path('attacks/<int:attacksId>',views.attacks, name='attacks'),
    path('attacksCategoryDetail/<int:attacksCategoryId>',views.attacksCategoryDetails, name='attacksCatsDet'),
    path('attacksDetail/<int:attacksId>',views.attacksDetails, name='attacksDet'),
    path('kkm',views.kkm, name='kkm'),
    path('kkm/botnet',views.botnet, name='botnet')
]