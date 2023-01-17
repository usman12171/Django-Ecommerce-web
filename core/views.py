from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import JsonResponse,HttpResponse
import json
from .form import userregister,update_profile,update_customer
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from.models import Customer,category,Product,cart,Comment,palceorder
# Create your views here.
from django.core.cache import cache
from django.contrib.auth import login,authenticate
def index(request):
    context={}
    cat=category.objects.all()
    product=Product.objects.all()
    if request.user.is_authenticated:
      user=request.user.id
      userpr=Customer.objects.get(user_id=user)
      carts=cart.objects.filter(customer_id=userpr)
      context['carts']=carts
    else:  
      context['cat']=cat
      context['product']=product
    return render(request,'core/base.html',context)

def emailvalids(request):
   valu=request.GET['values']
   us=User.objects.filter(email=valu)
   print(us)
   if us:
      return JsonResponse({"email":"email is invalid"})
   else:
      return JsonResponse({"emailright":True})
   
class customerregister(View):
   def get(self,request):
      context={}
      form = userregister()
      context['form']=form
      return render(request, 'core/register.html',context)
   def post(self,request):
    context={}
    obj=Customer()
    if request.method == "POST":
       form=userregister(request.POST)
       if form.is_valid():
            post_email=form.cleaned_data['email']
            if User.objects.filter(email=post_email).exists():
               messages.success(request,'erroe')
            else:
               form.save()
               username=form.cleaned_data.get('username')
               password = form.cleaned_data.get('password1')
               user = authenticate(username=username,password=password)
               login(request,user)
               obj.user_id=request.user.id
               obj.zipcode='123'
               obj.save()    
    context['form']=form
    context['messages']=messages
    return render(request,'core/register.html',context)



def updates_profile(request):
    context={}
    current=request.user.id
    user=User.objects.get(id=request.user.id)
    form=update_profile()
    form2=update_customer()
    uer=Customer.objects.get(user_id=current)
    if request.method == "POST":
        form=update_profile(request.POST,instance=user) 
        form2=update_customer(request.POST,request.FILES,instance=uer)
        if form.is_valid() and form2.is_valid():
           form.save()
           if form2.save():
              messages.success(request,'update ho gi')
           else:
                print(form2.errors)        
    context['form']=form 
    context['form2']=form2
    return render(request,'core/update_profile.html',context)


def products(request,data=None):
   context={}
   if data == None:
      produc=Product.objects.all()
   elif data == "XL" or data == 'L' or data =='M' or data =='S':
      produc=Product.objects.filter(product_size=data)
   elif data =='White' or data == 'black' or data == 'Grey' or data=='Yellow' or data=='blue':
      produc=Product.objects.filter(productcolor=data)
   elif  data <= '100'  or data <= '200'  :
      produc=Product.objects.filter(discounted_price=data)
   context['produc']=produc
   return render(request,'core/shop.html',context)

def product_detail(request,id):
   context={}
   obj=Product.objects.filter(id=id)
   use=Customer.objects.get(user_id=request.user.id)
   objs=Comment.objects.all()
   context['obj']=obj
   context['use']=use
   context['objs']=objs
   return render(request,'core/product_detail.html',context)

def review(request):
   if request.method == "POST":
      title=request.POST.get('title')
      print(title)
      content=request.POST.get('review')
      rate=request.POST.get('rate')
      Comment(title=title,content=content,rate=rate).save()
   return render(request,'core/product_detail.html')

def add_cart(request):
   id=request.GET['p_id']
   print('jsadjkkasd',id)
   user=request.user.id
   userpr=Customer.objects.get(user_id=user)
   pro=Product.objects.get(id=id)
   max=cart.objects.all()
   max=cart.objects.filter(Q(product_id=id) & Q(customer_id=userpr)) 
   if not max:
       reg=cart(customer=userpr,product=pro)
       reg.save()
       return JsonResponse({'message':'product is in the cart'})
   else:
       return JsonResponse({'messageerror':'product is already in the cart'})
       print("rola")
   return redirect('showcart')
   

def show_cart(request):
  context ={} 
  total=0.0
  shipping_amount=70.0
  user=request.user.id
  if request.user.is_authenticated:
      userpr=Customer.objects.get(user_id=user)
      carts=cart.objects.filter(customer_id=userpr) 
      if carts:
         carts=cart.objects.filter(customer_id=userpr) 
         for carte in carts:
               pro=Product.objects.filter(id=carte.product_id)
               for pr in pro:
                  temp=pr.discounted_price*carte.quantity
                  total+=temp
                  total_amount=total+shipping_amount
      else:
            return render(request,'core/cart.html',context)
  else:
      return render(request,'core/cart.html')
        
  context['carts']=carts
  context['total']=total
  context['total_amount']=total_amount
  return render(request,'core/cart.html',context)

def remove_cart(request):
   id=request.GET['prod_id']
   shipping_amount=70
   total=0.0
   user=request.user.id
   userpr=Customer.objects.get(user_id=user)
   c=cart.objects.get(Q(product_id=id) & Q(customer_id=userpr))
   c.delete()
   if c:
     carts=cart.objects.filter(customer_id=userpr) 
   for carte in carts:
         pro=Product.objects.filter(id=carte.product_id)
         for pr in pro:
            temp=pr.discounted_price*carte.quantity
            total+=temp
            total_amount=total+shipping_amount
   data={
      'total':total,
      'total_amount':total_amount,
   }
   return JsonResponse(data)

   return redirect('showcart')  

def plus_cart(request):
   
   id=request.GET['prod_id']
   user=request.user.id
   shipping_amount=70
   total=0.0
   userpr=Customer.objects.get(user_id=user)
   c=cart.objects.get(Q(product_id=id) & Q(customer_id=userpr))
   print(c)
   c.quantity+=1
   c.save()
   if c:
     carts=cart.objects.filter(customer_id=userpr) 
   for carte in carts:
         pro=Product.objects.filter(id=carte.product_id)
         for pr in pro:
            temp=pr.discounted_price*carte.quantity
            total+=temp
            total_amount=total+shipping_amount
   data={
      'quantity':c.quantity,
      'total':total,
      'total_amount':total_amount,
   }
   return JsonResponse(data)
   return redirect('showcart')  

def minus_cart(request):
   id=request.GET['prod_id']
   user=request.user.id
   total=0.0
   shipping_amount=70
   userpr=Customer.objects.get(user_id=user)
   print
   c=cart.objects.get(Q(product_id=id) & Q(customer_id=userpr))
   print(c)
   c.quantity-=1
   c.save()
   if c:
     carts=cart.objects.filter(customer_id=userpr) 
   for carte in carts:
         pro=Product.objects.filter(id=carte.product_id)
         for pr in pro:
            temp=pr.discounted_price*carte.quantity
            total+=temp
            total_amount=total+shipping_amount
   data={
      'quantity':c.quantity,
      'total':total,
      'total_amount':total_amount,
   }
   return JsonResponse(data)
   return redirect('showcart')  
 
def checkout(request):
  
   user=request.user.id
   total=0.0
   shipping_amount=70
   userpr=Customer.objects.get(user_id=user)

   carts=cart.objects.filter(customer_id=userpr) 
   if carts:
     carts=cart.objects.filter(customer_id=userpr) 
     for carte in carts:
         pro=Product.objects.filter(id=carte.product_id)
         for pr in pro:
            temp=pr.discounted_price*carte.quantity
            total+=temp
            total_amount=total+shipping_amount
         context={
            'carts':carts,
            'total':total,
            'total_amount':total_amount,
            'userpr':userpr,
         }
   else:
      return render(request,'core/checkout.html')
   return render(request,'core/checkout.html',context)

def place_order(request):
   userid=request.user.id
   userpr=Customer.objects.get(user_id=userid)
   cu=userpr.id
   print('hdasjkdsaj',cu)
   carts=cart.objects.filter(customer_id=userpr) 
   if carts:
     carts=cart.objects.filter(customer_id=userpr) 
   for carte in carts:
         pro=Product.objects.get(id=carte.product_id)
         custo=palceorder(customer_id=userpr.id,product=pro)
         custo.save()
         carts.delete()
   return redirect('orders')
   return render(request,'core/orderplace.html')

def order(request):
   if request.user.is_authenticated:
      userid=request.user.id
      userpr=Customer.objects.get(user_id=userid)
      orders=palceorder.objects.filter(customer_id=userpr)
      context ={
         'orders':orders,
      }
      return render(request,'core/order.html',context) 
   else:
       return render(request,'core/order.html')