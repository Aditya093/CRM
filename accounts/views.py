from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .filters import Orderfilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
# Create your views here.

def Register(request):

    
        form=CreateUserForm()
        if request.method =="POST":
            form= CreateUserForm(request.POST)
            if form.is_valid():
               user=form.save()
               username=form.cleaned_data.get('username')
               
               
              
               messages.success(request,'Account Successfully created for '+username)
               return redirect('login')
    
            
        context={'form':form}
        return render(request,'accounts/register.html',context)

def Login(request):
    
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
        
            user=authenticate(request,username=username,password=password)
        
            if user is not None:
               login(request,user)
               return redirect('home')
            else:
                messages.info(request,'Username or password is in correct!')        
        context={}
        return render(request,'accounts/login.html',context)
    
def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()  
    total_delivered=orders.filter(status='Delivered').count()
    total_pending=orders.filter(status='Pending').count()
    context={'orders':orders,'customers':customers,'total_customers':total_customers,
         'total_orders':total_orders, 'total_delivered':total_delivered, 'total_pending':total_pending  }
    return render(request,'accounts/dashboard.html',context)

def products(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/products.html', {'page_obj': page_obj})

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    order_count=orders.count()
    myFilter=Orderfilter(request.GET,queryset=orders)
    orders=myFilter.qs
    context={'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customers.html',context)  
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()  
    total_delivered=orders.filter(status='Delivered').count()
    total_pending=orders.filter(status='Pending').count()
    context={'orders':orders,'total_orders':total_orders, 'total_delivered':total_delivered, 'total_pending':total_pending }
    return render(request,'accounts/user.html',context)
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=8)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=='POST':
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request, 'accounts/order_form.html',context)

def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/order_form.html',context)

def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect("/")
    context={'item':order}
    return render(request,'accounts/delete.html',context)

def accountSettings(request):
    customer=request.user
    print(customer)
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'accounts/account_settings.html',context)