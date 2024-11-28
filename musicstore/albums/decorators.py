from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            messages.success(request, "У вас нет доступа к этой странице.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view