from django.urls import path

from . import views

urlpatterns = [
	path('inventory/', views.inventory_homepage, name="inventory_homepage"),
    path('inventory/items/', views.all_items, name="item_overview"),
	path('inventory/items/<int:item_id>/', views.item_zoom, name="item_zoom"),
]
