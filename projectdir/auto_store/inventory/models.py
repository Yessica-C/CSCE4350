from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_cost = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return str(self.id) + " | " + self.name

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    def __str__(self):
        return str(self.id) + " | " + self.name

class Inventory_Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_on_hand = models.IntegerField()
    def __str__(self):
        return "item #" +str(self.item_id) + " | location #" + str(self.location_id) + " | quantity:" + str(self.quantity_on_hand)1