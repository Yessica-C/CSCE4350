from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Item, Location
from .utils import quantity_on_hand, quantity_on_hand_by_location
from .utils import get_full_po, get_po_number_list


# hello world page

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

def all_pos(request):
    #get all unique purchase order numbers
    #get order date for each number
    #append each to table
    table = []
    for po in get_po_number_list():
        table.append({
            'po_num': po['po_num'],
            'date': po['date']
        })
    return render(request, 'inventory/all_pos.html', {'table': table})

def homepage(request):
    return render(request, 'inventory/homepage.html')

def inventory_homepage(request):
    items = Item.objects.all()
    return render(request, 'inventory/inventory_homepage.html', {'items': items})

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

def login(request):
    return render(request, 'inventory/login.html')

def po_zoom(request, po_num):
    po_table = get_full_po(po_num)
    return render(request, 'inventory/po_zoom.html', {'po_num': po_num, 'po_table': po_table})