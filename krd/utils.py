from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login

def role_required(role):
    def decorator(view_func):
        def wrap(request,*args,**kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role == role or request.user.role == "admin":
                return view_func(request,*args,**kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator