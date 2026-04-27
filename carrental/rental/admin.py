from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import Car, CarImage, Booking
from .models import ContactMessage
from django.utils import timezone
from .models import Company


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "company", "price_per_day")
    list_filter = ("company", "car_type")
    search_fields = ("name", "brand")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__owner=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not change:
            obj.company = request.user.company
        super().save_model(request, obj, form, change)

# -------------------------
# Anullimi ose kofirmimi i booking
# -------------------------

@admin.action(description=" Confirm selected bookings")
def confirm_bookings(modeladmin, request, queryset):
    updated = queryset.update(status="confirmed")

    for booking in queryset:
        send_mail(
            subject="Car Rental – Rezervimi u konfirmua",
            message=f"""
Pershendetje {booking.full_name},

Rezervimi juaj eshte konfirmuar !

Kodi i references: {booking.reference}
Makina e marre me qira: {booking.car.name}
Nga: {booking.start_date}
Deri: {booking.end_date}

Faleminderit qe na zgjodhet!
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=True,
        )

    modeladmin.message_user(
        request,
        f"{updated} booking(s) confirmed successfully."
    )


@admin.action(description="Cancel selected bookings")
def cancel_bookings(modeladmin, request, queryset):
    updated = queryset.update(status="cancelled")

    for booking in queryset:
        send_mail(
            subject="Car Rental – Rezervimi u Anulua",
            message=f"""
Pershendetje {booking.full_name},

Rezervimi juaj eshte anuluar
Kodi i references: {booking.reference}
Makina: {booking.car.name}

Nese mendoni se ka ndodhur ndonje gabime, ju lutemi te na kontaktoni.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=True,
        )

    modeladmin.message_user(
        request,
        f"{updated} booking(s) cancelled."
    )
# -------------------------
# Admini kryesor menaxhon rezervimet
# -------------------------

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "full_name",
        "email",
        "car",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("reference", "full_name", "email")

    actions = [confirm_bookings, cancel_bookings] 
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(car__company__owner=request.user)


#Adminit kryesor i jepet mundesia te bej reply mesazhet nga contact us
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("full_name", "email", "subject", "message")

    readonly_fields = ("full_name", "email", "subject", "message", "created_at")

    fieldsets = (
        ("User Message", {
            "fields": ("full_name", "email", "subject", "message", "created_at")
        }),
        ("Admin Reply", {
            "fields": ("reply", "is_read")
        }),
    )

    def save_model(self, request, obj, form, change):
        
        if obj.reply and not obj.replied_at:
            send_mail(
                subject=f"Re: {obj.subject}",
                message=f"""
Pershendetje {obj.full_name},

Faleminderit qe na kontaktuat!

{obj.reply}

Gjithe te mirat,
Car Rental Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
                fail_silently=False,
            )

            obj.replied_at = timezone.now()
            obj.is_read = True

        super().save_model(request, obj, form, change)
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "owner")