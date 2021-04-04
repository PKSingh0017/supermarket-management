from django.contrib import admin
from django.urls import path, include
from .views import (home, about, billing, add_to_cart, 
                remove_single_item_from_cart, remove_from_cart, 
                OrderSummaryView)

urlpatterns = [
    path('', home, name='home'),
    path('about/', home, name='about'),
    path('billing/', billing, name='billing'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-single-item-from-cart/<int:pk>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
]