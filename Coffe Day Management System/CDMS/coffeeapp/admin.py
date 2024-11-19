from django.contrib import admin
from .models import CartItem, Signup, Login, contactEnquiry

# Register your models here.
@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','password','confirm_password')

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('email','password')

@admin.register(contactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','message')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('name','price')