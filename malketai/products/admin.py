from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'category', 'sku', 'price', 'is_active')
    search_fields = ('name', 'sku', 'brand', 'category')
