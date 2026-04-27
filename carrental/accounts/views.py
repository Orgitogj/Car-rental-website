from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import company_required
from rental.models import Car, Booking
from rental.models import Company
from rental.models import CarImage
from django.shortcuts import get_object_or_404, redirect
from rental.forms import CarForm
from django.utils.translation import gettext as _
import re
from django.utils.translation import gettext_lazy as _


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        context = {"email": email}

        if not email and not password:
            messages.error(request, _("Please enter your email and password."))
            return render(request, "accounts/login.html", context)

        if not email:
            messages.error(request, _("Please enter your email."))
            return render(request, "accounts/login.html", context)

        if not password:
            messages.error(request, _("Please enter your password."))
            return render(request, "accounts/login.html", context)

        if "@" not in email or "." not in email:
            messages.error(request, _("Please enter a valid email address."))
            return render(request, "accounts/login.html", context)

        if not User.objects.filter(username=email).exists():
            messages.error(request, _("No account found with this email."))
            return render(request, "accounts/login.html", context)

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.error(request, _("Incorrect password. Please try again."))
            return render(request, "accounts/login.html", context)

        if not user.is_active:
            messages.error(request, _("Your account has been deactivated."))
            return render(request, "accounts/login.html", context)

        login(request, user)

        if user.is_superuser or user.is_staff:
            return redirect("/admin/")

        return redirect("home")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email     = request.POST.get("email", "").strip()
        phone     = request.POST.get("phone", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        context = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
        }

        if not full_name and not email and not phone and not password1 and not password2:
            messages.error(request, _("Please fill in all fields."))
            return render(request, "accounts/signup.html", context)

        if not full_name:
            messages.error(request, _("Please enter your full name."))
            return render(request, "accounts/signup.html", context)

        if len(full_name) < 7:
            messages.error(request, _("Full name must be at least 7 characters."))
            return render(request, "accounts/signup.html", context)

        if not email:
            messages.error(request, _("Please enter your email."))
            return render(request, "accounts/signup.html", context)

        if "@" not in email or "." not in email:
            messages.error(request, _("Please enter a valid email address."))
            return render(request, "accounts/signup.html", context)

        if not phone:
            messages.error(request, _("Please enter your phone number."))
            return render(request, "accounts/signup.html", context)

        if not re.match(r'^[\d\s\+\-\(\)]+$', phone):
            messages.error(request, _("Please enter a valid phone number."))
            return render(request, "accounts/signup.html", context)

        if len(re.sub(r'\D', '', phone)) < 10:
            messages.error(request, _("Phone number must be at least 10 digits."))
            return render(request, "accounts/signup.html", context)

        if not password1:
            messages.error(request, _("Please enter a password."))
            return render(request, "accounts/signup.html", context)

        if len(password1) < 8:
            messages.error(request, _("Password must be at least 8 characters."))
            return render(request, "accounts/signup.html", context)

        if not password2:
            messages.error(request, _("Please confirm your password."))
            return render(request, "accounts/signup.html", context)

        if password1 != password2:
            messages.error(request, _("Passwords do not match."))
            return render(request, "accounts/signup.html", context)

        if User.objects.filter(username=email).exists():
            messages.error(request, _("An account with this email already exists."))
            return render(request, "accounts/signup.html", context)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1
        )
        user.first_name = full_name
        user.save()

        login(request, user)
        return redirect("home")

    return render(request, "accounts/signup.html")

def logout_view(request):
    logout(request)
    return redirect("home")



@login_required
@company_required

def dashboard_home(request):
    company = request.user.company

    cars_count = Car.objects.filter(company=company).count()
    bookings_count = Booking.objects.filter(car__company=company).count()
    confirmed_bookings = Booking.objects.filter(
        car__company=company,
        status="confirmed"
    ).count()

    context = {
        "company": company,
        "cars_count": cars_count,
        "bookings_count": bookings_count,
        "confirmed_bookings": confirmed_bookings,
    }

    return render(request, "dashboard/dashboard_home.html", context)



@login_required
def company_bookings(request):
    company = request.user.company

    bookings = Booking.objects.filter(
        car__company=company
    ).select_related("car")

    return render(
        request,
        "dashboard/company_bookings.html",
        {
            "bookings": bookings
        }
    )

@login_required
def company_profile(request):
    company = request.user.company

    if request.method == "POST":
        company.name = request.POST.get("name")
        company.email = request.POST.get("email")
        company.phone = request.POST.get("phone")
        company.description = request.POST.get("description")
        company.save()

        return redirect("company_profile")

    return render(
        request,
        "dashboard/company_profile.html",
        {
            "company": company
        }
    )
    
@login_required
@company_required
def edit_car(request, car_id):
    car = get_object_or_404(
        Car,
        id=car_id,
        company=request.user.company
    )

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)

        if form.is_valid():
            car = form.save()

            #Ruhen fotot e reja qe shtohen
            for img in request.FILES.getlist("images"):
                CarImage.objects.create(
                    car=car,
                    image=img
                )

            return redirect("my_cars")
    else:
        form = CarForm(instance=car)

    return render(
        request,
        "dashboard/edit_car.html",
        {
            "form": form,
            "car": car
        }
    )

def portal_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect("/admin/")

            if hasattr(user, "company"):
                return redirect("dashboard_home")

            # Useri normal nuk lejohet te futet
            messages.error(
                request,
                "This portal is for companies only."
            )
            return redirect("portal_login")

        messages.error(request, "Invalid credentials")

    return render(request, "accounts/portal_login.html")

def portal_logout(request):
    logout(request)
    return redirect("portal_login")