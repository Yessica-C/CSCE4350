from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_cost = models.DecimalField(max_digits=10, decimal_places=2)

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

class Inventory_Entry:
    id = models.IntegerField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_on_hand = models.IntegerField()