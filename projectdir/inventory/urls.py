from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),
]