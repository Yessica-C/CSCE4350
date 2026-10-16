from django.contrib import admin
from .models import (
	Item,
	Location,
	Inventory_Entry,
	Purchase_Order,
	Purchase_Order_Data,
	Timecard_Entry,
	Sale,
	Sale_Entry,
)

admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Inventory_Entry)
admin.site.register(Purchase_Order_Data)
admin.site.register(Purchase_Order)
admin.site.register(Timecard_Entry)
admin.site.register(Sale)
admin.site.register(Sale_Entry)