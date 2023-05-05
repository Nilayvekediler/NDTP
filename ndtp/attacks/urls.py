from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('attacksCategory',views.attacksCategory, name='attacksCats'),
    path('attacks/<int:attacksId>',views.attacks, name='attacks'),
    path('attacksCategoryDetail/<int:attacksCategoryId>',views.attacksCategoryDetails, name='attacksCatsDet'),
    path('attacksDetail/<int:attacksId>',views.attacksDetails, name='attacksDet') #,
    #path('stop-attack/',views.stop_attack, name='stop-attack')
]