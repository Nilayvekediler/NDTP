from django.contrib import admin

# Register your models here.

from .models import AttacksCategory
from .models import Attacks

admin.site.register(AttacksCategory)
admin.site.register(Attacks)