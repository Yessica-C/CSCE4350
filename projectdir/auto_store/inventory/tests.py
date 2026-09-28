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

	def test_receiving_updates_received_quantity_and_inventory(self):
		entry = Purchase_Order_Data.objects.get(po_num=1)

		response = self.client.post('/inventory/receiving/', {
			'entry_id': entry.id,
			'quantity_received': 1,
		})

		self.assertRedirects(response, '/inventory/receiving/')
		entry.refresh_from_db()
		self.assertEqual(entry.quantity_received, 1)
		self.assertEqual(
			entry.item_id.inventory_entry_set.get(location_id=entry.location_id).quantity_on_hand,
			1,
		)

	def test_receiving_does_not_double_count_existing_received_quantity(self):
		entry = Purchase_Order_Data.objects.get(po_num=1)
		entry.quantity_received = 1
		entry.save(update_fields=['quantity_received'])

		self.client.post('/inventory/receiving/', {
			'entry_id': entry.id,
			'quantity_received': 2,
		})

		entry.refresh_from_db()
		self.assertEqual(entry.quantity_received, 2)
		self.assertEqual(
			entry.item_id.inventory_entry_set.get(location_id=entry.location_id).quantity_on_hand,
			1,
		)

	def test_receiving_all_ordered_items_completes_purchase_order(self):
		entry = Purchase_Order_Data.objects.get(po_num=1)

		self.client.post('/inventory/receiving/', {
			'entry_id': entry.id,
			'quantity_received': entry.quantity_ordered,
		})

		self.assertEqual(Purchase_Order.objects.get(po_num=1).status, 'Complete')

	def test_receiving_can_filter_open_entries_by_po_number(self):
		second_po = Purchase_Order.objects.create(po_num=2)
		second_entry = Purchase_Order_Data.objects.create(
			item_id=Item.objects.get(id=1),
			location_id=Location.objects.get(id=1),
			po_num=second_po,
			quantity_ordered=3,
			item_cost='8.00',
		)

		response = self.client.get('/inventory/receiving/?po_num=2')

		filtered_entries = list(response.context['entries'])
		self.assertEqual(len(filtered_entries), 1)
		self.assertEqual(filtered_entries[0].po_num.po_num, second_po.po_num)
		self.assertContains(response, 'value="2"')

	def test_purchase_orders_can_filter_by_selected_statuses(self):
		Purchase_Order.objects.create(po_num=2, status='Open')
		Purchase_Order.objects.create(po_num=3, status='Complete')

		response = self.client.get('/inventory/purchase_orders/?status=Open')

		filtered_orders = response.context['table']
		self.assertEqual(len(filtered_orders), 1)
		self.assertEqual(filtered_orders[0]['status'], 'Open')
		self.assertEqual(response.context['selected_statuses'], ['Open'])
		self.assertContains(response, 'value="Open"')
		self.assertContains(response, 'checked')

# Create your tests here.
