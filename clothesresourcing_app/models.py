from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPE_OF_INSTITUTION = [
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
]


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_OF_INSTITUTION, default=1)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name + " Opis: " + self.description


class Donation(models.Model):
    categories = models.ManyToManyField(Category)
    quantity = models.PositiveIntegerField(default=1)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=32)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(default="Brak uwag", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(default=False)

