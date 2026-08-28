from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Item, Location, Inventory_Entry

def quantity_on_hand(item_id):
    sum = 0
    #find all inventory entries for this item
    entries = Inventory_Entry.objects.filter(item_id=item_id)
    #add quantity in each entry to sum  
    for entry in entries:
        sum += entry.quantity_on_hand
    #return sum
    return sum

def quantity_on_hand_by_location(item_id, location_id):
    sum = 0
    #find all inventory entries that match item and location
    entries = Inventory_Entry.objects.filter(item_id=item_id, location_id=location_id)
    #add quantity in each entry to sum
    for entry in entries:
        sum += entry.quantity_on_hand
    #return sum
    return sum

# hello world page
def inventory_homepage(request):
    items = Item.objects.all()
    return render(request, 'inventory/inventory_homepage.html', {'items': items})

def all_items(request):
    items = Item.objects.all()
    table = []
    for item in items:
        table.append({
            'item_id': item.id,
            'item_name': item.name,
            'item_description': item.description,
            'item_price': item.price,
            'item_last_cost': item.last_cost,
            'total_quantity': quantity_on_hand(item.id)
        })
    return render(request, 'inventory/all_items.html', {'table': table})

def item_zoom(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return render(request, 'inventory/item_not_found.html', status=404)
    locations = Location.objects.all()
    loc_table = []
    for location in locations:
        loc_table.append({
            'location_id': location.id,
            'location_address': location.address,
            'quantity_on_hand': quantity_on_hand_by_location(item_id, location.id)
        })
    return render(request, 'inventory/item_zoom.html', {'item': item, 'loc_table': loc_table, 'total_quantity': quantity_on_hand(item_id)})