from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.index,name='ShopHome'),
    path('about/',views.about,name='AboutUs'),
    path('checkout/',views.checkout,name='Checkout'),
    path('cart/',views.cart,name='Cart'),
    path('tracker/',views.tracker,name='Tracker'),
    path('contact/',views.contact,name='ContactUs'),
    path('prodview/<int:myid>',views.prodview,name='prodView'),
    path('search/',views.search,name='Search'),
    path('update_item/',views.UpdateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order')
]