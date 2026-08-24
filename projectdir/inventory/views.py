from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from .models import Inventory, Item, Location


def homepage(request):
    return render(request, "inventory/homepage.html")


def item_detail(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    if item is None:
        return render(request, "inventory/item_not_found.html")

    on_hand_locations = Location.objects.annotate(
        quantity=Coalesce(
            Sum("inventory__quantity", filter=Q(inventory__item=item)),
            Value(0),
        )
    ).values("id", "name", "quantity")

    on_hand_locations = [
        {
            "location_id": row["id"],
            "location_name": row["name"],
            "quantity": row["quantity"],
        }
        for row in on_hand_locations
    ]
    #TODO store numbers & item counts not correct 
    return render(
        request,
        "inventory/item_detail.html",
        {"item": item, "table": on_hand_locations},
    )