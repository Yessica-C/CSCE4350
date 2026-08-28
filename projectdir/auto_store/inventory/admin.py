from django.contrib import admin
from .models import Item, Location, Inventory_Entry

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Inventory_Entry)