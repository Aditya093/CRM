from django.shortcuts import redirect 
from django.urls import reverse

class LoginRequiredMiddleware:
    EXCLUDED_URLS = [
        reverse('login'),  # Replace with your login URL
        reverse('register'),  # Replace with your register URL
        reverse('reset_password'),
        reverse('forgot_password'),
       
   
    ]
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if not request.user.is_authenticated and request.path not in self.EXCLUDED_URLS:
            return redirect('login')
        response=self.get_response(request)
        return response     