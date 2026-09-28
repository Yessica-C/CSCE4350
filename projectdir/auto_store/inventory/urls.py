from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
	path('inventory/', views.inventory_homepage, name="inventory_homepage"),
    path('inventory/receiving/', views.receiving, name="receiving"),
    path('inventory/items/', views.all_items, name="item_overview"),
    path('inventory/items/add/', views.add_item, name="add_item"),
    path('inventory/items/edit/<int:item_id>/', views.edit_item, name="edit_item"),
	path('inventory/items/zoom/<int:item_id>/', views.item_zoom, name="item_zoom"),
    path('inventory/purchase_orders/', views.all_pos, name="purchase_order_overview"),
    path('inventory/purchase_orders/add/', views.add_po, name="add_po"),
    path('inventory/purchase_orders/edit/<int:po_num>/', views.edit_po, name="edit_po"),
	path('inventory/purchase_orders/zoom/<int:po_num>/', views.po_zoom, name="po_zoom"),
    path('inventory/purchase_orders/delete/<int:po_num>/', views.delete_po, name="delete_po"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]
