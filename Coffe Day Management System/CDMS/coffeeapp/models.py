from django.utils import timezone
from django.db import models

# Create your models here.

class Signup(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password=models.CharField(max_length=250)
    confirm_password = models.CharField(max_length=250)
    signup_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Login(models.Model):
    login_id = models.IntegerField(default=1)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100)
    login_time = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.email
    
class contactEnquiry(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    message=models.TextField()
    enquiry_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    


class CartItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    added_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Recalculate total price before saving
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
