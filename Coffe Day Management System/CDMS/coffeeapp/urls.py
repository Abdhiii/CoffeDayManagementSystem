from django.urls import path
from . import views
from .views import  generate_bill_pdf, generate_pdf_with_reportlab


urlpatterns = [
    path('',views.base, name='base'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('ourspecials/', views.ourspecials, name='ourspecials'),
    path('products/', views.products, name='products'),
    path('logout/', views.logout, name='logout'),
    path('saveenquiry/', views.saveEnquiry, name='saveenquiry'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('payment/', views.payment_view, name='payment'),
    path('order_confirmed/', views.order_confirmed_view, name='order_confirmed'),
    path('generate_bill_pdf/', generate_bill_pdf, name='generate_bill_pdf'),
    path('render_markdown/', views.render_markdown_view, name='render_markdown'),
    path('generate_pdf_with_reportlab/', generate_pdf_with_reportlab, name='generate_bill_mo_pdf'),
]
