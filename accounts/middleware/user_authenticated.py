from django.shortcuts import redirect
from django.urls import reverse
class AuthenticationRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            if request.user.is_authenticated:
                restricted_paths = [reverse('register'), reverse('login')]
                if request.path in restricted_paths:
                     return redirect('home')
        
            response = self.get_response(request)
            return response
