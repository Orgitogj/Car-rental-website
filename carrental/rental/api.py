from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.conf import settings
from .models import Car, Booking
from datetime import date
import json
from django.urls import reverse
from django.core.mail import EmailMessage
from threading import Thread


@csrf_exempt
def check_availability(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)

    car_id = data.get("car_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not all([car_id, start_date, end_date]):
        return JsonResponse({"error": "Missing data"}, status=400)

    car = Car.objects.get(id=car_id)

    available = Booking.is_car_available(
        car,
        start_date,
        end_date
    )

    return JsonResponse({"available": available})


@csrf_exempt
def create_booking(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)

        car_id = data.get("car_id")
        full_name = data.get("full_name")
        email = data.get("email")
        phone = data.get("phone")
        start_date = parse_date(data.get("start_date"))
        end_date = parse_date(data.get("end_date"))

        if not all([car_id, full_name, email, phone, start_date, end_date]):
            return JsonResponse({"error": "Missing fields"}, status=400)

        car = Car.objects.get(id=car_id)

        if not Booking.is_car_available(car, start_date, end_date):
            return JsonResponse(
                {"error": "Car not available for selected dates"},
                status=409
            )

        # Krijohet booking dhe rregjistrohet ne databaze
        booking = Booking.objects.create(
            car=car,
            full_name=full_name,
            email=email,
            phone=phone,
            start_date=start_date,
            end_date=end_date,
            status="pending"
        )

        # Funksion per te derguar email
        def send_email_async():
            email_message = EmailMessage(
                subject="Car Rental –Booking recieved",
                body=f"""
Pershendetje {booking.full_name},

Rezervimi juaj u percoll tek stafi yne. Pas verifikimit do te kontaktoheni ne lidhje me procesin e metejshem.

Kodi i references: {booking.reference}
Makina: {car.name}
Nga data: {booking.start_date}
Deri me: {booking.end_date}

Faleminderit qe na zgjodhet!
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[booking.email],
            )
            email_message.send(fail_silently=True)
        
        # Dergo emailin ne background thread
        Thread(target=send_email_async).start()
        
        # Redirect ne faqen success.html 
        return JsonResponse({
            "success": True,
            "redirect": reverse(
                "booking_success",
                args=[booking.reference]
            )
        })

    except Car.DoesNotExist:
        return JsonResponse({"error": "Car not found"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)