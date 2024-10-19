from functools import wraps
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
  
def allow_access_to(user_type_list):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if user.user_type in user_type_list:
                    return func(request, *args, **kwargs)
                raise Http404
            raise Http404
        return wrapper
    return decorator

def profile_completion_required(redirect_url=None, message=None):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if not request.user.is_profile_completed:
                flash_message = message or "Please complete your profile before proceeding."
                messages.error(request, flash_message)
                return redirect(redirect_url)
            return function(request, *args, **kwargs)
        return wrap
    return decorator
