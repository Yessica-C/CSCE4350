from .models import Inventory_Entry

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
