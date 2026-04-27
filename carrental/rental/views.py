from django.shortcuts import render, get_object_or_404
from .models import Car, Company
from .models import Booking
import qrcode
import base64
from io import BytesIO
from datetime import datetime
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.core.files import File
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect
from .forms import CarForm
from .models import CarImage
from accounts.decorators import company_required
from django.urls import reverse

# HOME
def home(request):
    featured_cars = Car.objects.all().order_by('popularity')[:6]  
 
    companies = Company.objects.filter(cars__isnull=False).distinct().order_by('name')
    
    return render(request, "index.html", {
        "featured_cars": featured_cars,
        "companies": companies
    })


EXCLUDE_KEYS = [
    "priceMin", "priceMax",
    "yearMin", "yearMax",
    "seatsMin", "seatsMax",
    "powerMin", "powerMax",
    "sort", "brand", "fuel", "gear", "company"
]

def cars(request):
    qs = Car.objects.all()

    # =====================================================
    # Filtri i disponueshmerise
    # =====================================================
    start = request.GET.get("start")
    end   = request.GET.get("end")

    if start and end:
        qs = qs.exclude(
            bookings__status__in=["pending", "confirmed"],
            bookings__start_date__lt=end,
            bookings__end_date__gt=start
        )

    # =====================================================
    # Cmimi
    # =====================================================
    price_min = request.GET.get("priceMin")
    price_max = request.GET.get("priceMax")

    if price_min:
        qs = qs.filter(price_per_day__gte=price_min)

    if price_max:
        qs = qs.filter(price_per_day__lte=price_max)

    # =====================================================
    # Viti i makines
    # =====================================================
    year_min = request.GET.get("yearMin")
    year_max = request.GET.get("yearMax")

    if year_min:
        qs = qs.filter(year__gte=year_min)

    if year_max:
        qs = qs.filter(year__lte=year_max)

    # =====================================================
    #Numri i sediljeve
    # =====================================================
    seats_min = request.GET.get("seatsMin")
    seats_max = request.GET.get("seatsMax")

    if seats_min:
        qs = qs.filter(seats__gte=seats_min)

    if seats_max:
        qs = qs.filter(seats__lte=seats_max)

    # =====================================================
    #Fuqia motorrike
    # =====================================================
    power_min = request.GET.get("powerMin")
    power_max = request.GET.get("powerMax")

    if power_min:
        qs = qs.filter(power__gte=power_min)

    if power_max:
        qs = qs.filter(power__lte=power_max)

    # =====================================================
    # Filtrimi i futur nga perdoruesi
    # =====================================================
    brand = request.GET.get("brand")
    fuel  = request.GET.get("fuel")
    gear  = request.GET.get("gear")
    car_type = request.GET.get("type")
    company_id = request.GET.get("company")

    if brand:
        qs = qs.filter(brand__iexact=brand)

    if fuel:
        qs = qs.filter(fuel=fuel)

    if gear:
        qs = qs.filter(gear=gear)

    if car_type:
        qs = qs.filter(car_type=car_type)
    
    # Kopmania
    if company_id:
        qs = qs.filter(company_id=company_id)

    # =====================================================
    # Sorting sipas kategorive
    # =====================================================
    sort = request.GET.get("sort")

    SORT_MAP = {
        "price-asc":  "price_per_day",
        "price-desc": "-price_per_day",
        "year-asc":   "year",
        "year-desc":  "-year",
        "popular":    "-popularity",
    }

    if sort in SORT_MAP:
        qs = qs.order_by(SORT_MAP[sort])

    qs = qs.distinct()
    #Shfaqen makinat nga cdo kompani
    companies = Company.objects.filter(cars__isnull=False).distinct().order_by('name')
    
    # Merr emrin e kompanise se zgjedhur
    selected_company = None
    if company_id:
        try:
            selected_company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            pass

#Nese ka makina ng ajo kompani i shfaq ato ,nese jo shfaq makinat te gjitha
    template = (
        "partials/car_list.html"
        if request.headers.get("HX-Request")
        else "cars.html"
    )

    return render(request, template, {
        "cars": qs,
        "companies": companies,
        "selected_company": selected_company
    })


# CAR DETAILS
def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, "car-details.html", {"car": car})

# ABOUT
def about(request):
    return render(request, "aboutus.html")

# CONTACT
def contact(request):
    return render(request, "contactus.html")

def booking_success(request, reference):
    booking = get_object_or_404(Booking, reference=reference)

    return render(request, "success.html", {
        "booking": booking
    })

def booking_lookup(request):
    booking = None
    error = None

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        reference = request.POST.get("reference", "").strip()

        booking = Booking.objects.filter(
            reference__iexact=reference,
            full_name__iexact=full_name
        ).first()

        if not booking:
            error = "No booking found with provided details."

    return render(
        request,
        "booking_lookup.html",
        {
            "booking": booking,
            "error": error
        }
    )


def contact(request):
    success = False

    if request.method == "POST":
        ContactMessage.objects.create(
            full_name=request.POST.get("full_name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )
        success = True

    return render(
        request,
        "contactus.html",
        {"success": success}
    )


@login_required
def my_cars(request):
    company = request.user.company  
    cars = Car.objects.filter(company=company)

    return render(
        request,
        "dashboard/dashboard_cars.html",
        {
            "company": company,
            "cars": cars,
        }
    )


@login_required
def add_car(request):
    company = request.user.company 

    if request.method == "POST":
        form = CarForm(request.POST)

        if form.is_valid():
            car = form.save(commit=False)
            car.company = company
            car.save()

            images = request.FILES.getlist("images")
            for image in images:
                CarImage.objects.create(
                    car=car,
                    image=image
                )

            return redirect("my_cars")
    else:
        form = CarForm()

    return render(request, "dashboard/add_car.html", {
        "form": form
    })
    
@login_required
@company_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__company=request.user.company
    )

    if booking.status == "pending":
        booking.status = "confirmed"   
        booking.save() 

    return redirect("company_bookings")


@login_required
@company_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        car__company=request.user.company
    )
    booking.status = "cancelled"
    booking.save()
    return redirect("company_bookings")
    
# rental/views.py
@login_required
@company_required
def delete_car_image(request, image_id):
    image = get_object_or_404(
        CarImage,
        id=image_id,
        car__company=request.user.company
    )

    car_id = image.car.id
    image.delete()

    return redirect("edit_car", car_id=car_id)

@login_required
@company_required
def set_main_car_image(request, image_id):
    image = get_object_or_404(
        CarImage,
        id=image_id,
        car__company=request.user.company
    )

    # Behen reset te gjitha fotot
    CarImage.objects.filter(car=image.car).update(is_main=False)

    #Imazhin e zgjedhur e ben main image
    image.is_main = True
    image.save()

    return redirect("edit_car", car_id=image.car.id)


@login_required
@company_required
def bulk_update_bookings(request):
    if request.method != "POST":
        return redirect("company_bookings")

    action = request.POST.get("action")
    booking_ids = request.POST.getlist("booking_ids")

    if not booking_ids:
        return redirect("company_bookings")

    bookings = Booking.objects.filter(
        id__in=booking_ids,
        car__company=request.user.company,
        status="pending"
    )

    for booking in bookings:
        if action == "confirm":
            booking.status = "confirmed"
        elif action == "cancel":
            booking.status = "cancelled"
        else:
            continue

        booking.save()

    return redirect("company_bookings")