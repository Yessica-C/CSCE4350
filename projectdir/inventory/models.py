import datetime

from django.db import models
from django.utils import timezone

class Location(models.Model):
    loc_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField()

    def __str__(self):
        return self.name

class Item(models.Model):
    item_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    last_cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_sale_date = models.DateTimeField("Last Sold", null=True, blank=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.location} - Quantity on hand: {self.quantity}"