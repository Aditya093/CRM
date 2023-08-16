from django.shortcuts import redirect
from django.urls import reverse
class AccessControlMiddleware:
    def __init__(self, get_response):
        
        self.get_response = get_response
        self.not_allowed_paths = {
            'admin': [], 
            'customer': ['admin','customer','home','products','create_order','update_order','delete_order',''],  
            
            'staff': ['register','admin','customer','home','products','create_order','update_order','delete_order' ],
             'Anonymous': ['admin','customer','home','products','create_order','update_order','delete_order','logout']
                       
        }
        self.image_paths = ['images/']
    def __call__(self, request):      
        if request.user.is_superuser:
            # Allow admin user to access every page
            return self.get_response(request)
        print(request.path)
        user_groups=list(request.user.groups.values_list('name',flat=True))
        if(user_groups==[]):
            user_groups.append('Anonymous') 
        
        for group in user_groups:
            if group in self.not_allowed_paths:
                not_allowed_paths = self.not_allowed_paths[group]
                path = request.path.strip('/')
                print(path) 
                if not_allowed_paths and path in not_allowed_paths:
                    # Redirect the user to the user page or display an unauthorized message
                    return redirect(reverse('user'))

        return self.get_response(request)
