from django.db import models


class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    street_name = models.CharField(max_length=120)
    street_number = models.CharField(max_length=60)
    settlement = models.CharField(max_length=120)
    town = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    size = models.FloatField()
    image = models.CharField(max_length=60)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class PropertyAmenity(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=120)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class PropertyDescription(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(
        "Property",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
