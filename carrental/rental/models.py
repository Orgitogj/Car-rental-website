from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Car(models.Model):

    FUEL_CHOICES = [
        ("petrol", _("Petrol")),
        ("diesel", _("Diesel")),
        ("hybrid", _("Hybrid")),
        ("electric", _("Electric")),
    ]

    GEAR_CHOICES = [
        ("manual", _("Manual")),
        ("automatic", _("Automatic")),
    ]

    CAR_TYPE_CHOICES = [
        ("economy", "Economy"),
        ("family", "Family"),
        ("suv", "SUV"),
        ("luxury", "Luxury"),
        ("sports", "Sports"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="cars"
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    seats = models.IntegerField()
    power = models.IntegerField()
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    gear = models.CharField(max_length=20, choices=GEAR_CHOICES)
    popularity = models.IntegerField(default=0)
    engine_size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
   
   
    @property
    def main_image(self):
        main = self.images.filter(is_main=True).first()
        if main:
            return main.image
        return None
    
class CarImage(models.Model):
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="cars/")
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car.name}"

class Booking(models.Model):

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("confirmed", _("Confirmed")),
        ("cancelled", _("Cancelled")),
    ]

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    start_date = models.DateField()
    end_date = models.DateField()

  

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    reference = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"CR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.reference} - {self.car.name}"
    
    
    @staticmethod
    def is_car_available(car, start_date, end_date):
        conflicting_bookings = Booking.objects.filter(
            car=car,
            status__in=["pending", "confirmed"]
        ).filter(
           Q(start_date__lte=end_date) &
        Q(end_date__gte=start_date)
        )

        return not conflicting_bookings.exists()

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    reply = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} – {self.subject}"



