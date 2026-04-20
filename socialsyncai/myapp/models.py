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
