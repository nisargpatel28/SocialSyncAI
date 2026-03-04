from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('products/', views.product_list),
    path('products/<int:product_id>/', views.product_detail),
]
