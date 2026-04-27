from django.shortcuts import redirect
from django.contrib import messages

def company_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, "company"):
            messages.error(request, "You are not associated with a company.")
            return redirect("home")

        return view_func(request, *args, **kwargs)
    return wrapper
