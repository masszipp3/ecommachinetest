from django.urls import path
from . import views

app_name='shop_admin'

urlpatterns=[
    path('',views.home,name='home'),
    path('signin',views.signin,name='signin'),
    path('products',views.products,name='products'),
    path('categories',views.categories,name='categories'),
    path('orders',views.orders,name='orders'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('<str:pid>/editproduct',views.editproduct,name='editproduct'),
    path('<str:pid>/deleteproduct',views.deleteproduct,name='deleteproduct'),
    path('<str:pid>/stockupdate',views.stockupdate,name='stockupdate'),
    path('<str:cid>/categoryid',views.updatecategory,name='editcategory'),
    path('<str:cid>/catagorydelete',views.catagorydelete,name='deletecategory'),
    path('<str:oid>/orderdetails',views.orderdetails,name='orderdetails'),
    path('<str:pid>/productdetails',views.productdetails,name='productdetails'),
    path('logout',views.adminlogout,name='logout'),















]