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
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'),name="reset_password"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_form.html'),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_done.html'),name="password_reset_complete")
]                                                                                             