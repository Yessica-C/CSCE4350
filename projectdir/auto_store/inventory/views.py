from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Item, Location, Inventory_Entry

# hello world page
def inventory_homepage(request):
    items = Item.objects.all()
    return render(request, 'inventory/inventory_homepage.html', {'items': items})

def all_items(request):
    items = Item.objects.all()
    return render(request, 'inventory/all_items.html', {'items': items})

def item_zoom(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return render(request, 'inventory/item_not_found.html', status=404)
        
    inventory_entries = Inventory_Entry.objects.filter(item_id=item_id)
    table = []
    for entry in inventory_entries:
        location = Location.objects.get(id=entry.location_id.id)
        table.append({
            'location_id': location.id,
            'location_address': location.address,
            'quantity_on_hand': entry.quantity_on_hand
        })
    return render(request, 'inventory/item_detail.html', {'item': item, 'table': table})