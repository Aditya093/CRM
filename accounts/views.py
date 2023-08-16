from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import Orderfilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
from collections import Counter
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
            for form in formset:
                if form.cleaned_data.get('product'):
                    product=form.cleaned_data['product']
                    form.instance.ordered_price=product.price
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
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'accounts/account_settings.html',context)

def forgot_password(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        
        if user:
            # Generate and save a reset token
            reset_token = get_random_string(50)
            user.reset_token = reset_token
            user.save()

            # Send the reset link to the user's email
            reset_link = f"{settings.BASE_URL}/reset_password/?token={reset_token}"
            send_mail(
                'Password Reset Link',
                f'Click the following link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'accounts/reset_password_message.html', {'email': user.email})
    
    return render(request, 'accounts/forgot_password.html')



def reset_password(request):
    reset_token = request.GET.get('token')
    if request.method == 'POST':
        password = request.POST.get('password')
        
        user = User.objects.filter(reset_token=reset_token).first()

        if user:
            # Reset password and clear reset token
            user.password = make_password(password)
            user.reset_token = None
            user.save()
            return redirect('/login/')

    return render(request, 'accounts/reset_password.html', {'token': reset_token})


def pie_chart(request):
    data=Order.objects.all()
    items=[]
    prices=[]
    for key in data:
        items.append(key.product)
        
    items_set=Counter(items)
    labels=items_set.keys()
    values=items_set.values()
    for i,j in zip(labels,values):
        price=j*(i.price)
        prices.append(price)  
    print(prices)    
    names=[]
    for x in labels:
        name=x.name
        names.append(name)
    values=list(values) 

    fig_bar = px.bar(x=names,y=prices, title="Bar", height=500)

    # Scatter Chart
    fig_scatter = px.scatter(x=values, y=prices, height=500)

    # Line Chart

    fig_line = px.line(x=names, y=prices, height=500)
    fig_line.update_traces(textposition="bottom right")

    # Pie Chart
    fig_pie = px.pie(values=values,labels=labels, names=names, height=500)


    bar_chart = fig_bar.to_html(full_html=False, include_plotlyjs=False)
    scatter_chart = fig_scatter.to_html(full_html=True, include_plotlyjs=False)
    line_chart = fig_line.to_html(full_html=False, include_plotlyjs=False)
    pie_chart = fig_pie.to_html(full_html=False, include_plotlyjs=False)

    context={'bar_chart':bar_chart,'pie_chart':pie_chart,'line_chart':line_chart,'scatter_chart':scatter_chart}
      
    return render(request,'accounts/insights.html',context)

def bar_chart(request):
    data=Order.objects.all()
    items=[]
    prices=[]
    for key in data:
        items.append(key.product)
    for key in data:
        prices.append(key.ordered_price)
    print(items)
    print(prices)    
    fig=go.bar(x=items,y=prices)
    chart=opy.plot(fig,output_type='div')
    context={'bar_chart':chart}
    return render(request,'accounts/insights.html',context)    