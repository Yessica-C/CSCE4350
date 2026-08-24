from django.contrib import admin
from .models import Inventory, Location
from .models import Item

admin.site.register(Inventory)
admin.site.register(Item)
admin.site.register(Location)