from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib.auth import authenticate, authenticate, logout, login
from django.db.models import Max
from .models import Item, Location
from .utils import quantity_on_hand, quantity_on_hand_by_location
from .utils import get_full_po, get_po_number_list

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        last_cost = request.POST.get('last_cost')

        # Create a new Item instance and save it to the database
        item = Item(name=name, description=description, price=price, last_cost=last_cost)
        item.save()

        # Redirect to the all_items view after successful creation
        return redirect('item_overview')
    
    highest_item_number = Item.objects.aggregate(max_number=Max('id'))['max_number']
    id = highest_item_number + 1 if highest_item_number is not None else 1
    return render(request, 'inventory/add_item.html', {'id': id,})

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'inventory/login.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'inventory/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'inventory/logout.html')

def po_zoom(request, po_num):
    po_table = get_full_po(po_num)
    return render(request, 'inventory/po_zoom.html', {'po_num': po_num, 'po_table': po_table})