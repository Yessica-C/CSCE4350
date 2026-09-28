from django.test import TestCase

from .models import Item, Location, Purchase_Order, Purchase_Order_Data


class PurchaseOrderDeleteTests(TestCase):
	def setUp(self):
		item = Item.objects.create(
			id=1,
			name='Test item',
			description='Test description',
			price='10.00',
			last_cost='8.00',
		)
		location = Location.objects.create(
			id=1,
			name='Test location',
			address='123 Test Street',
		)
		purchase_order = Purchase_Order.objects.create(po_num=1)
		Purchase_Order_Data.objects.create(
			item_id=item,
			location_id=location,
			po_num=purchase_order,
			quantity_ordered=2,
			item_cost='8.00',
		)

	def test_delete_requires_confirmation(self):
		response = self.client.get('/inventory/purchase_orders/delete/1/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Yes, delete')
		self.assertTrue(Purchase_Order.objects.filter(po_num=1).exists())

	def test_confirmed_delete_removes_purchase_order_entries(self):
		response = self.client.post('/inventory/purchase_orders/delete/1/')

		self.assertRedirects(response, '/inventory/purchase_orders/')
		self.assertFalse(Purchase_Order.objects.filter(po_num=1).exists())
		self.assertFalse(Purchase_Order_Data.objects.filter(po_num=1).exists())

# Create your tests here.
