from django.shortcuts import render,redirect
from shop_admin.models import Accounts, Product, Categories,Review,User
from customers.models import Order, OrderItem
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .decorators import shopadminrequired




# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.is_shopadmin:
                login(request, user)
                return redirect('shop_admin:home') 
        else:   
                msg='Wrong Username or password'
    return render(request,'shopadmin/signin.html')

@shopadminrequired
def home(request):
    Orders=Order.objects.filter().order_by('-created_at')[:10]
    return render(request,'shopadmin/index.html',{'orders':Orders}) 

@shopadminrequired
def products(request):
    product_list = Product.objects.all().order_by('-id')
    paginator = Paginator(product_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'shopadmin/products.html',{'productpage':page_obj})

@shopadminrequired
def orders(request):
    Orders=Order.objects.filter().order_by('-created_at')
    # print(Orders)
    paginator = Paginator(Orders, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'shopadmin/orders.html',{'orders':page_obj})

@shopadminrequired
def orderdetails(request,oid):
    order=Order.objects.get(OrderId=oid)
    Orderitem=OrderItem.objects.filter(order=order)
    total=0
    for orders in Orderitem:
        total += orders.quantity*orders.price
    status_choices = Order.STATUS_CHOICES
    if request.method=='POST':
        status=request.POST['status']
        order.status=status
        order.save()
    

    
    return render(request,'shopadmin/orderdetails.html',{'orderitems':Orderitem,'order':order,'total':total,'choices':status_choices})

@shopadminrequired
def productdetails(request,pid):
    product_details=Product.objects.get(Product_ID=pid)
    review=Review.objects.filter(product=product_details)
    total=0
    for rating in review:
        total=total+rating.rating
    try:
        avgrating=total/review.count()
    except:
        avgrating=0    
    return render(request,'shopadmin/productdetails.html',{'product':product_details,'avgrating':int(avgrating)})

@shopadminrequired
def categories(request):
    msg = request.GET.get('msg', '')
    catagories = Categories.objects.all().order_by('-id')
    paginator = Paginator(catagories, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'shopadmin/catagories.html',{'catagories':page_obj})

@shopadminrequired
def addcategory(request):
    msg=''
    if request.method=='POST':
        name=request.POST['catagoryname']
        description=request.POST['description']
        slug=request.POST['slug']
        categoryid=request.POST['categoryid']
        image=request.FILES['catagorypic']
        category = Categories.objects.filter(slug=slug).exists()
        category_id=Categories.objects.filter(category_ID=categoryid).exists()
    
        if category or category_id:
            msg='Category Already Exist'
            return redirect('shop_admin:categories')
        else:
            category_create=Categories.objects.create(category_name=name,category_ID=categoryid,slug=slug,category_image=image,category_description=description)    
            msg='New Category Added'
            return redirect('shop_admin:categories')
        
    return render(request,'shopadmin/addcategory.html')

@shopadminrequired
def addproduct(request):
    catagories=Categories.objects.all()
    if request.method=='POST':
        porduct_name=request.POST['productname']
        product_price=request.POST['price']
        product_id = 'MNBR'+str(Product.objects.count())
        slug=request.POST['slug']
        description= request.POST['description']
        category=request.POST['catagory']
        unit='Nos'
        brand= request.POST['brand']
        minquandity=request.POST['minquantity']
        product_pic=request.FILES['productpic']
        product_slug = Product.objects.filter(slug=slug).exists()
        product_id_Check = Product.objects.filter(Product_ID=product_id).exists()
        
        if product_slug or product_id_Check:
            msg='product already exists'
        else:
            Addproduct= Product.objects.create(Product_name=porduct_name,Product_ID=product_id,slug=slug,Min_value=minquandity,Price=product_price,brand=brand,
                                         Description=description,Product_category_id =category,onstock=True,product_image=product_pic)

    return render(request,'shopadmin/addproduct.html',{'cat':catagories})

@shopadminrequired
def editproduct(request,pid):
        catagory=Categories.objects.filter()
        product=Product.objects.get(Product_ID=pid)
        if request.method=='POST':
            product.Product_name=request.POST['productname']
            product.Product_ID=request.POST['productID']
            product.Product_category_id=request.POST['productcat']
            product.Price=request.POST['price']
            product.Description=request.POST['description']
            product.Min_value=request.POST['minquantity']
            if 'productpic' in request.FILES:
                product.product_image = request.FILES['productpic']
            product.save()
            return redirect('shop_admin:products')

        return render(request,'shopadmin/editproduct.html',{'product':product,'catagory':catagory})

@shopadminrequired
def deleteproduct(request,pid):
    try:
        product=Product.objects.get(id=pid)
        product.delete()
        return redirect('shop_admin:products')  
    except:
        return redirect('shop_admin:products')  

@shopadminrequired
def stockupdate(request,pid):
    try:
        product=Product.objects.get(id=pid)
        if product.onstock:
            product.onstock=False
            product.save()
        else:
            product.onstock=True
            product.save()     

        return redirect('shop_admin:products')  
    except:
        return redirect('shop_admin:products')  
    
@shopadminrequired
def updatecategory(request,cid):
    try:
        catagory=Categories.objects.get(id=cid)
        if request.method == 'POST':
            catagory.category_name=request.POST['category_name']
            catagory.category_description=request.POST['category_description']
            catagory.slug=request.POST['slug']
            catagory.category_ID=request.POST['category_ID']
            if 'category_image' in request.FILES:
                catagory.category_image = request.FILES['category_image']

            catagory.save()
            return redirect('shop_admin:categories')
    except:
        pass
    return render(request,'shopadmin/editcatagory.html',{'catdata':catagory})    

@shopadminrequired
def catagorydelete(request,cid):
    try:
        catagory=Categories.objects.get(id=cid)
        catagory.delete()
        return redirect('shop_admin:categories')
    except:
        return redirect('shop_admin:categories')
    
def adminlogout(request):
   logout(request)  
   return redirect('shop_admin:signin')    


 
