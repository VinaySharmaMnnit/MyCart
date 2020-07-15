from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from math import ceil
import json
import datetime
from .utils import cookieCart,cartData,guestOrder


# Create your views here.
def index(request):
    allprod = []
    catprod = Product.objects.values('category', 'id')
    cats = {items['category'] for items in catprod}
    for cat in cats:
        product = Product.objects.filter(category=cat)
        n = len(product)
        nSlides = ceil(n / 4)
        allprod.append([product, range(1, nSlides), nSlides])


    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    context = {'items': items, 'allprod':allprod,'order': order, 'cartItems': cartItems}
    return render(request, 'shop/index.html', context)

def about(request):
    return render(request,'shop/about.html')

def checkout(request):
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={"items":items,"order":order,"cartItems":cartItems,}
    return render(request,'shop/checkout.html',context)

def cart(request):
    #first check if user is logged in or not
    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']


    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'shop/cart.html',context)
def contact(request):
    if request.method == 'POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        description=request.POST.get('description','')
        print(name,email,phone,description)
        contact=Contact(name=name,email=email,phone=phone,description=description)
        contact.save()
        thank=True
        return render(request, 'shop/contact.html', {'thank': thank})

    return render(request,'shop/contact.html')


def tracker(request):
    return render(request,'shop/tracker.html')

def match(query,item):
    if query.lower() in item.desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True;
    else:
        return False

def search(request):
    query=request.GET.get('search','')
    allprod = []
    catprod = Product.objects.values('category', 'id')
    cats = {items['category'] for items in catprod}
    for cat in cats:
        producttemp = Product.objects.filter(category=cat)
        prod=[item for item in producttemp if match(query,item)]
        n = len(prod)
        nSlides = ceil(n / 4)
        if n!=0:
           allprod.append([prod, range(1, nSlides), nSlides])

    params = {'allprod': allprod,'msg':""}
    if len(allprod)==0 or len(query)<3:
        params={'msg':"Please make relevant search"}

    return render(request, 'shop/search.html', params)




def prodview(request,myid):
    product=Product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': product[0]})

def UpdateItem(request):
    data=json.loads(request.body)
    prodId=data['prodId']
    action = data['action']
    print('Action:',action)
    print('ProdId:',prodId)
    username=request.user.username
    email=request.user.email

    customer=Customer.objects.get(user=request.user)


    product=Product.objects.get(id=prodId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitems , created = OrderItems.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderitems.quantity=(orderitems.quantity+1)
    elif action == 'remove':
        orderitems.quantity=(orderitems.quantity-1)
    orderitems.save()
    if(orderitems.quantity<=0):
        orderitems.delete()
    return JsonResponse('item is added',safe=False)


#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
       
    else:
        customer,order=guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id=transaction_id
    if total==float(order.get_cart_total):
        order.complete=True
    order.save()
    if order.shipping==True:
        Shippingaddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zip_code=data['shipping']['zipcode'],
                
       )
    print("Data:",request.body)
    return JsonResponse('Payment complete',safe=False)



