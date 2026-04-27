from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

from rental.api import create_booking, check_availability

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("rental.urls")),  
    path("accounts/", include("accounts.urls")),
)

urlpatterns += [
    path("api/bookings/check/", check_availability),
    path("api/bookings/create/", create_booking),
    path("", include("accounts.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
