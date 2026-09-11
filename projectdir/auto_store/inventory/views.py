import json

from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.contrib.auth import authenticate, authenticate, logout, login
from django.db.models import Max
from django.utils import timezone
from .models import Item, Location, Purchase_Order, Purchase_Order_Data
from .utils import quantity_on_hand, quantity_on_hand_by_location, get_full_po

def add_item(request):
    #form submission
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
    #entry
    highest_item_number = Item.objects.aggregate(max_number=Max('id'))['max_number']
    id = highest_item_number + 1 if highest_item_number is not None else 1
    return render(request, 'inventory/add_item.html', {'id': id,})

def add_po(request):
    highest_po_number = Purchase_Order.objects.aggregate(max_number=Max('po_num'))['max_number']
    new_po_num = highest_po_number + 1 if highest_po_number is not None else 1
    return redirect('edit_po', po_num=new_po_num)


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
    #get each PO, return table of relevant information
    table = []
    for po in Purchase_Order.objects.all():
        table.append({
            'po_num': po.po_num,
            'date': po.order_date,
            'status': po.status
        })
    return render(request, 'inventory/all_pos.html', {'table': table})

def edit_po(request, po_num):
    if request.method == 'POST':#form submission
        value = request.POST.get('action')
        po_data = json.loads(request.POST.get('po_data', '[]'))
        po = Purchase_Order.objects.filter(po_num=po_num).first()#check if po already exists
        if po is not None:#if it does
            #delete all existing lines for this po_num
            Purchase_Order_Data.objects.filter(po_num=po_num).delete()
        if po is None:#if it does not
            #creat a new po object with status "unposted"
            po = Purchase_Order(po_num=po_num, status='Unposted')
            po.save()
        #create new lines from submitted data
        data_error = False
        err_msg = "Invalid data submitted."
        for entry in po_data:
            item = Item.objects.filter(id=entry.get('item_id')).first()
            quantity_ordered = entry.get('quantity_ordered')
            quantity_received = entry.get('quantity_received')
            item_cost = entry.get('item_cost')
            location = Location.objects.filter(id=entry.get('location_id')).first()
            if item and quantity_ordered and item_cost and location:
                Purchase_Order_Data.objects.create(
                    po_num=Purchase_Order.objects.get(po_num=po_num),
                    item_id=item,
                    quantity_ordered=quantity_ordered,
                    quantity_received=quantity_received or 0,
                    item_cost=item_cost,
                    location_id=location
                    )
            else:
                data_error = True
                if item is None:
                    err_msg += "\nItem not found: " + str(entry.get('item_id'))
                if location is None:
                    err_msg += "\nLocation not found: " + str(entry.get('location_id'))
        if data_error:
            return render(request, 'inventory/edit_po.html', {'new_po_num': po_num, 'error_message': err_msg})
        if value == 'save': # do not post, leave PO open for editing and move to "unposted" status
            return redirect('purchase_order_overview')
        if value == 'post': # post, lock editing on PO and move to "open" status
            po.status = 'Open'  
            po.order_date = timezone.now()
            po.save()  
            return redirect('purchase_order_overview')
    #normal page request
    #if po already exists, load data and display in table
    return render(request, 'inventory/edit_po.html', {'new_po_num': po_num})

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
    po_object = Purchase_Order.objects.get(po_num=po_num)
    return render(request, 'inventory/po_zoom.html', {'po_object': po_object, 'po_table': po_table})