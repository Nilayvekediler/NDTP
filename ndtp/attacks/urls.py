from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('attacksCategory',views.attacksCategory, name='attacksCats'),
    path('attacks/<int:attacksId>',views.attacks, name='attacks'),
    path('attacksCategoryDetail/<int:attacksCategoryId>',views.attacksCategoryDetails, name='attacksCatsDet'),
    path('attacksDetail/<int:attacksId>',views.attacksDetails, name='attacksDet'),
    path('kkm',views.kkm, name='kkm'),
    path('kkm/botnet',views.botnet, name='botnet'),
    path('kkm/start/<str:node>/<int:ct_id>', views.start_ct, name='start_ct'),
    path('kkm/stop/<str:node>/<int:ct_id>', views.stop_ct, name='stop_ct'),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("userPage", views.userpage, name="userpage"),
    path("monitoring", views.monitoring, name="monitoring"),

]