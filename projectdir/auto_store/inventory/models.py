from django.db import models

# Create your models here.
class Item(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
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
    id = models.IntegerField(primary_key=True,auto_created=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity_on_hand = models.IntegerField()
    def __str__(self):
        return "item #" +str(self.item_id) + " | location #" + str(self.location_id) + " | quantity:" + str(self.quantity_on_hand)

class Purchase_Order_Data(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    po_num = models.ForeignKey('Purchase_Order', on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return "PO #" + str(self.po_num) + " | item #" + str(self.item_id.id) + " | location #" + str(self.location_id.id) + " | ordered:" + str(self.quantity_ordered) + " | received:" + str(self.quantity_received)

class Purchase_Order(models.Model):
    class Status(models.TextChoices):
        UNPOSTED = 'UPST', ('Unposted')
        OPEN = 'OPEN', ('Open')
        COMPLETE = 'CMPL', ('Complete')
    po_num = models.IntegerField(primary_key=True)
    order_date = models.DateField(null=True, blank=True)
    status = models.TextField(choices=Status.choices, default='Unposted', max_length=10)
    def __str__(self):
        return "PO #" + str(self.po_num)

class Timecard_Entry(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    employee_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField(null=True, blank=True)

class Sale(models.Model):
    customer = models.BigIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

class Sale_Entry(models.Model):
    order_id = models.ForeignKey(Sale, on_delete=models.CASCADE, db_column='order_id')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, db_column='item')
    quantity = models.BigIntegerField()
    price = models.FloatField()
    time_of_sale = models.DateTimeField()
