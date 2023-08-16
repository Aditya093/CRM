from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('customers/<str:pk_test>',views.customer,name='customer'),
    path('create_order/<str:pk>',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('register/',views.Register,name='register'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('user/',views.userPage,name='user'), 
    path('account/',views.accountSettings,name='account'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('insights',views.pie_chart,name='insights'),
    path('insights',views.bar_chart,name='insights'),
]                                                                                             
