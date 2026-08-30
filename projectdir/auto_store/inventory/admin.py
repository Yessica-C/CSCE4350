from django.contrib import admin
from .models import Item, Location, Inventory_Entry, Purchase_Order

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Inventory_Entry)
admin.site.register(Purchase_Order)