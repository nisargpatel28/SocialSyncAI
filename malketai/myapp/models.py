from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    code = models.IntegerField()

    # This is a string representation of the tours
    def __str__(self):
        return (f"ID:{self.id}: First Name {self.first_name} Last Name {self.last_name} Email {self.email} Code {self.code}")


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    sku = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_nw=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
