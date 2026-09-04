from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
	path('inventory/', views.inventory_homepage, name="inventory_homepage"),
    path('inventory/items/', views.all_items, name="item_overview"),
    path('inventory/items/add/', views.add_item, name="add_item"),
	path('inventory/items/<int:item_id>/', views.item_zoom, name="item_zoom"),
    path('inventory/purchase_orders/', views.all_pos, name="purchase_order_overview"),
	path('inventory/purchase_orders/<int:po_num>/', views.po_zoom, name="po_zoom"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]
