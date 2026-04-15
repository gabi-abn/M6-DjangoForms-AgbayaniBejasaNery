from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add set the field to when the object is first created
    objects = models.Manager()

    def getName(self):
        return self.name
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country} created at: {self.created_at}"
    
class WaterBottle(models.Model):
    SKU = models.CharField(max_length=300, unique=True)
    brand = models.CharField(max_length=300)
    cost = models.DecimalField(max_digits=100, decimal_places=2)
    size = models.CharField(max_length=300)
    mouth_size = models.CharField(max_length=300)
    color = models.CharField(max_length=300)
    supplied_by = models.ForeignKey(Supplier, on_delete=models.CASCADE) #foreign key to supplier, reference from the class Supplier
    current_quantity = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return f"{self.SKU}: {self.brand}, {self.mouth_size}, {self.size}, {self.color}, supplied by {self.supplied_by.name}, {self.cost}, {self.current_quantity}"

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def __str__(self):
        return self.username