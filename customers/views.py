from django.shortcuts import render,redirect
from shop_admin.models import Product,Categories,Accounts,Review,Address,User
from .models import Cart, CartItem,Order,OrderItem
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.mail import send_mail
import random
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt  # Import if you need to disable CSRF protection
import json
from django.contrib.auth.decorators import login_required
from . decorators import customerrequired



# Create your views here.

def signup(request):
    product_list=Product.objects.all()[:10]
    catagories = Categories.objects.all()[:8]
    return render(request,'customer/index.html',{'products':product_list})

def signin(request):
    msg=''
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        customer_exists=User.objects.filter(username=email,is_customer=True).exists()
        if customer_exists:
                user= authenticate(request, username=email, password=password)
                
                if user is not None and user.is_customer:
                    # print(user)
                    account = Accounts.objects.get(user=user)
                    login(request, user)
                    request.session['customer']=account.id
                    return redirect('customers:home')
        else:
            msg='invalid username or password'           


    return render(request,'customer/signin.html',{'msg':msg})

def home(request):
    product_list=Product.objects.all()[:10]
    catagories = Categories.objects.all()[:8]
    return render(request,'customer/index.html',{'products':product_list})

def details(request,slug):
    product_list=Product.objects.get(slug=slug)
    eligblity=False
    try:
        if request.method=='POST':
            rating=request.POST['rating']
            review=request.POST['review']
            reviewexist=Review.objects.filter(customer_id=request.session['customer'],product=product_list).exists()
            if not reviewexist:
                raview=Review.objects.create(rating=rating,review=review,customer_id=request.session['customer'],product=product_list)
            else:
                raview=Review.objects.get(customer_id=request.session['customer'],product=product_list)
                raview.rating=rating
                raview.review=review
                raview.save()
        reviews=Review.objects.filter(product=product_list,customer_id=request.session['customer'])
        reviewstatus= OrderItem.objects.filter(order__user=request.session['customer'],product=product_list).exists()
        if reviewstatus:
            eligblity=True
        else:
            eligblity=False    
        allreviews=Review.objects.filter(product=product_list).exclude(customer_id=request.session['customer'])
            
                
        carts=CartItem.objects.filter(cart__customer=request.session['customer'],product=product_list).exists()
    except:
        reviews=False
        carts=False   
        allreviews=Review.objects.filter(product=product_list) 
    return render(request,'customer/productdetails.html',{'product':product_list,'exists':carts,'myreview':reviews,'review':eligblity,'allreviews':allreviews})

def store(request):
    product = Product.objects.all()
    paginator = Paginator(product, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        cart=CartItem.objects.filter(cart__customer=request.session['customer'])
        cartids=[item.product.id for item in cart]
    except:
        cartids=[]
     
    
    print(cartids)

    return render(request,'customer/store.html',{'product_list':page_obj,'cartitems':cartids})


def cart(request):
    try:
        carts=Cart.objects.get(customer__user=request.user)
        # carts.delete()
        cartitems=CartItem.objects.filter(cart=carts)
        sum=0
        for i in cartitems:
            sum+=i.quantity*i.product.Price
        request.session['grandtotal']=sum   
    except:
        cartitems=0
        request.session['grandtotal']=0



    return render(request,'customer/cart.html',{'cartitems':cartitems,'total':request.session['grandtotal']})

def orderplace(request):
    try:
        address=Address.objects.filter(Account_id=request.session['customer'])
    except:
        address=''    
    if request.method=='POST':
        paymentoption=request.POST['payment-option']
        address= request.POST['address']
        orderid='ORDER'+str(Order.objects.count()+1)
        
        order=Order.objects.create(paymentmethod=paymentoption,address_id=address,total_price=request.session['grandtotal'],user_id=request.session['customer'],OrderId=orderid)
        cartss=Cart.objects.get(customer__user=request.user)
        cartitem=CartItem.objects.filter(cart=cartss)
        for item in cartitem:
            Ordderitem=OrderItem.objects.create(product=item.product,
                                                order=order,
                                                quantity=item.quantity,
                                                price=item.product.Price
                                                )
        cartss.delete()
        del request.session['grandtotal']

        return redirect('customers:home')    


    return render(request,'customer/orderplaced.html',{'total':request.session['grandtotal'],'addresses':address})

@customerrequired
def removeitemcaer(request,pid):
    cartss=Cart.objects.get(customer__user=request.user)
    carts=CartItem.objects.get(product__Product_ID=pid,cart=cartss)
    carts.delete()
    return redirect('customers:mycart')

@customerrequired
def saveaddress(request):
    if request.method=='POST':
        street_address=request.POST['street_address']
        recipient_name=request.POST['name']
        apartment_suite=request.POST['house']
        city =request.POST['city']
        state = request.POST['state']
        postal_code = request.POST['postal_code']
        country=request.POST['country']
        phone_number=request.POST['phone_number']

        Address.objects.create(street_address=street_address,recipient_name=recipient_name,apartment_suite=apartment_suite,city=city,
                               state=state,postal_code=postal_code,country=country,phone_number=phone_number,
                               Account_id=request.session['customer'])
        

    return redirect('customers:orderplaced')

def emailcheck(request):
    if request.method=='POST':
        usercheck =User.objects.filter(username=request.POST['email']).exists()
        if usercheck:
            return JsonResponse({'exist':True})
        else:
            return JsonResponse({'exist':False})
    return JsonResponse({'status':404})    
    

def customersignup(request):
        msg=''
        try:
            refererr = request.GET.get('type')
        except:
            refererr = None
        if request.method == 'POST' :
            email = request.POST['email']
            password=request.POST['password']
            if refererr is None:
                try:
                    name=request.POST['name']
                except:
                    pass    


            customer_exists=User.objects.filter(username=email,is_customer=True).exists()
            if customer_exists:
                if refererr is not None:
                    user=authenticate(request, username=email, password=password)
                    if user is not None and user.is_customer:
                        account = Accounts.objects.get(user=user)
                        login(request, user)
                        request.session['customer']=account.id
                        referring_url = request.META.get('HTTP_REFERER')
                        if referring_url:
                            return redirect(referring_url)
                        else:
                            redirect('customers:home')         
                    else:
                        msg='error'  
                else:
                    return redirect('customers:signin')              
            else:
                new_user = User.objects.create_user(username=email,password=password,is_customer=True)
                if new_user is not None and new_user.is_customer:
                    account = Accounts.objects.create(user=new_user)
                    if refererr=='last':
                        login(request, new_user)
                        request.session['customer']=account.id
                        referring_url = request.META.get('HTTP_REFERER')
                        if referring_url:
                            return redirect(referring_url)
                        else:
                            redirect('customers:home')
                    else:
                        account.name=name
                        account.save()
                        msg='account created please login'        
        return render(request,'customer/signup.html',{'msg':msg})

                    
def sync_cartdata(request):
    subtotal=0
    if request.method=='POST':
        cartdata= json.loads(request.POST.get('cart'))
        account = Accounts.objects.get(user=request.user)
        print(cartdata)
        if len(cartdata)>0:
            cart,cartcreated=Cart.objects.get_or_create(customer=account)
            for item in cartdata:
                cartdatas,cartitemcreated = CartItem.objects.get_or_create(cart=cart,product_id=item['product_id'],quantity=item['qty'])
            carts=CartItem.objects.filter(cart__customer__user=request.user)
            for i in carts:
                subtotal=subtotal+i.quantity*i.product.Price   
            request.session['grandtotal']=subtotal     
        return JsonResponse({'status':True,'total':subtotal})        


def addtocart(request):
    if request.method=='POST':
        product_id=request.POST['product']
        customer=Accounts.objects.get(user=request.user)
        product=Product.objects.get(id=product_id)
        carts,cartcreate=Cart.objects.get_or_create(customer=customer)
        cart_item,created=CartItem.objects.get_or_create(cart=carts,product=product)
        grandtotal=request.session.get('grandtotal',0)

        if not created:
            cart_item.quantity=cart_item.quantity+1
            cart_item.save()
            grandtotal+=cart_item.product.Price
            request.session['grandtotal']=grandtotal
            subtotal=cart_item.quantity*cart_item.product.Price
            return JsonResponse({
                'status':'ok','toatal':grandtotal,'quandity':cart_item.quantity,'subtotal':subtotal
            }) 
    else:
        product_id=request.GET['product']
        customer=Accounts.objects.get(user=request.user)
        product=Product.objects.get(id=product_id)
        carts,cartcreate=Cart.objects.get_or_create(customer=customer)
        cart_item,created=CartItem.objects.get_or_create(cart=carts,product=product)
        grandtotal=request.session.get('grandtotal',0)
        
        if not created:
            cart_item.quantity=cart_item.quantity-1
            grandtotal+=cart_item.product.Price
            cart_item.save()
            request.session['grandtotal']=grandtotal
        if cart_item.quantity<=0:
            cart_item.delete()
            
        subtotal=cart_item.quantity*cart_item.product.Price
        return JsonResponse({
                'status':'ok','toatal':grandtotal,'subtotal':subtotal
            })     

    return JsonResponse({'status':404}) 
@customerrequired
def customerlogout(request):
   logout(request)  
   return redirect('customers:signin')



        