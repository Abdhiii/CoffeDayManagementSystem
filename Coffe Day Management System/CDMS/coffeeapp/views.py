import base64
from datetime import timezone
from django.utils import timezone
import os
from django.shortcuts import render, redirect, get_object_or_404
import markdown2
from coffee import settings
from .forms import CartItemForm, SignUpForm, LoginForm
from .models import CartItem, Signup, Login, contactEnquiry
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

# Create your views here.

def base(request):
    return render(request, 'coffeeapp/base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                signup_instance = form.save(commit=False)
                signup_instance.signup_date = timezone.now()
                signup_instance.save()
                return redirect('login')
            else:
                form.add_error('confirm_password', 'Passwords do not match')
    else:
        form = SignUpForm()
    return render(request, 'coffeeapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Signup.objects.get(email=email, password=password)
                login_instance, created = Login.objects.update_or_create(
                    email=email,
                    defaults={'password': password, 'login_time': timezone.now()}
                )
                
                request.session['login_id'] = user.id
                return redirect('home')
            except Signup.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'coffeeapp/login.html', {'form': form})

def home(request):
    return render(request, 'coffeeapp/home.html')

def about(request):
    return render(request, 'coffeeapp/about.html')

def contact(request):
    return render(request, 'coffeeapp/contact.html')

def ourspecials(request):
    return render(request, 'coffeeapp/ourspecials.html')

def products(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        CartItem.objects.create(name=name, price=price)
        return redirect('cart')
    return render(request, 'coffeeapp/products.html')

def logout(request):
    return redirect('login')

def saveEnquiry(request):
    if request.method == "POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        message=request.POST.get("message")
        en=contactEnquiry(name=name,email=email,phone=phone,message=message)
        en.save()
        return render(request, 'coffeeapp/contact.html',{'message': 'Message Submitted'})
    return render(request, 'coffeeapp/contact.html')

#def cart(request):
 #   return render(request, 'coffeeapp/cart.html')



def cart_view(request):
    if request.method == 'POST':
        for item in CartItem.objects.all():
            # Get the updated quantity from the form
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        # Redirect to avoid resubmission of the form
        return redirect('cart')

    cart_items = CartItem.objects.all()
    for item in cart_items:
        item.total_price = item.price * item.quantity
    # Calculate the total price for each item
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'coffeeapp/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def add_to_cart(request):
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.created_at = timezone.now()
            cart_item.save()
            return redirect('cart')
    else:
        form = CartItemForm()
    cart_items = CartItem.objects.all()
    return render(request, 'coffeeapp/cart.html', {'form': form, 'cart_items': cart_items})

def delete_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('cart')
    return render(request, 'coffeeapp/delete_item.html', {'cart_items': CartItem.objects.all()})

def edit_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = CartItemForm(instance=item)
    return render(request, 'coffeeapp/edit_item.html', {'form': form, 'item': item})


def payment_view(request):
    cart_items = CartItem.objects.all()
    for item in cart_items:
        item.total_price = item.price * item.quantity
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'coffeeapp/payment.html', {'cart_items': cart_items, 'total_price': total_price})


def order_confirmed_view(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.all()
        total_price = sum(item.price * item.quantity for item in cart_items)
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        pdf = generate_pdf_with_reportlab(context)
        encoded_pdf = base64.b64encode(pdf).decode('utf-8')
        request.session['pdf'] = encoded_pdf
        CartItem.objects.all().delete()
        return render(request, 'coffeeapp/order_confirmed.html')
    return redirect('cart')

def generate_bill_pdf(request):
    encoded_pdf = request.session.get('pdf', None)
    if encoded_pdf:
        pdf = base64.b64decode(encoded_pdf)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="bill.pdf"'
        return response
    return redirect('order_confirmed')

def generate_pdf_with_reportlab(context):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.drawString(100, height - 100, "Coffee Shop Receipt")
    y = height - 150
    for item in context['cart_items']:
        p.drawString(100, y, f"Item: {item.name}, Price: {item.price}, Quantity: {item.quantity}")
        y -= 20

    p.drawString(100, y - 20, f"Total Price: {context['total_price']}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

def render_markdown_view(request):
    markdown_file_path = os.path.join(settings.BASE_DIR, 'your_app', 'data.md')
    with open(markdown_file_path, 'r') as file:
        markdown_content = file.read()
    html_content = markdown2.markdown(markdown_content)
    return render(request, 'coffeepp/markdown_page.html', {'html_content': html_content})

