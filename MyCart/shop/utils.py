import json
from .models import *

def cookieCart(request):
    
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('Cart:',cart)
        items=[]
        order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
        cartItems=order['get_cart_item']
        for i in cart:
            #if product does not exist It gives error so to remove that error we are using try except
            try:
                    cartItems+=cart[i]['quantity']
                    product =Product.objects.get(id=i)
                    total=(product.price*cart[i]['quantity'])
                    order['get_cart_total']+=total
                    order['get_cart_item']+=cart[i]['quantity']

                    item={
                        'product':{
                            'id':product.id,
                            'product_name':product.product_name,
                            'price':product.price,
                            'image':product.image,
                        },
                        'quantity':cart[i]['quantity'],
                        'get_total':total,
                    }
                    items.append(item)
                    if product.digital==False:
                        order['shipping']=True
            except:
                pass

        return {'items':items,'order':order,'cartItems':cartItems}

def cartData(request):
    if request.user.is_authenticated:
        # for one to one relationship we here are getting customer

        #try:
        username=request.user.username
        email=request.user.email
        try:
           customer = Customer.objects.get(user=request.user)
        except:
            customer = Customer.objects.create(user=request.user, name=request.user.username, email=request.user.email)
            customer.save()

        #here we are getting order if it exists otherwise we are creating it.
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        #here we are getting all the order items which has order=order
        items=order.orderitems_set.all()
        cartItems = order.get_cart_item
    else:
        cookieData=cookieCart(request)
        cartItems=cookieData['cartItems']
        order=cookieData['order']
        items=cookieData['items']
    return {'items':items,'order':order,'cartItems':cartItems}


def guestOrder(request,data):
    print("User is not logged in")
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    cookieData=cookieCart(request)
    items=cookieData['items']

    customer,created=Customer.objects.get_or_create(
        email=email,
    )

    customer.name=name
    customer.save()

    order=Order.objects.create(
       customer=customer,complete=False
    )

    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItems=OrderItems.objects.create(
            product=product,
            order=order,
            quantity=item["quantity"],
        )
    
    return customer,order    