from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

# Ruhet statusi primar i rezervimit
@receiver(pre_save, sender=Booking)
def store_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_booking = Booking.objects.get(pk=instance.pk)
            instance._old_status = old_booking.status
        except Booking.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


# Dergohet email vetem kur nga statusi pending kalon ne confirmed
@receiver(post_save, sender=Booking)
def send_booking_confirmed_email(sender, instance, created, **kwargs):
    old_status = getattr(instance, "_old_status", None)

    if old_status == "pending" and instance.status == "confirmed":

        send_mail(
            subject="Car Rental – Rezervimi u konfirmua",
            message=f"""
Pershendetje {instance.full_name},

Rezervimi juaj u konfirmua!

Kodi i references: {instance.reference}
Makina: {instance.car.name}
Nga data: {instance.start_date}
Deri me: {instance.end_date}

Faleminderit qe na zgjodhet!
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )