from django.contrib import admin
from .models import Inventory
from .models import Item

admin.site.register(Inventory)
admin.site.register(Item)