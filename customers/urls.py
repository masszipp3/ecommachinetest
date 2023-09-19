from django.urls import path
from . import views

app_name='customers'

urlpatterns=[
    path('',views.home,name='home'),
    path('productdetails/<str:slug>',views.details,name='productsdetials'),
    path('store',views.store,name='store'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('mycart',views.cart,name='mycart'),
    path('order',views.orderplace,name='orderplaced'),
    path('emailcheck',views.emailcheck,name='emailcheck'),
    path('signup',views.customersignup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('synccart',views.sync_cartdata,name='synccartdata'),
    path('addaddress',views.saveaddress,name='addaddress'),
    path('logout',views.customerlogout,name='logout'),
    path('removeitem/<str:pid>',views.removeitemcaer,name='removeitem')






]