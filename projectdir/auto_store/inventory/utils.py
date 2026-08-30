from turtle import pos

from .models import Inventory_Entry, Purchase_Order

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

def get_full_po(po_num):
    #get all purchase order entries with matching po_num
    po = Purchase_Order.objects.filter(po_num=po_num)
    return po

def get_po_number_list():
    #get all unique purchase order numbers
    po_nums = Purchase_Order.objects.values_list('po_num', flat=True).distinct()
    table = []
    for num in po_nums:
        date = Purchase_Order.objects.filter(po_num=num).first().order_date
        table.append({'po_num': num, 'date': date})
    return table