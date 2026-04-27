from django.urls import path
from .views import login_view, register_view,logout_view
from .views import dashboard_home
from .import views
from .views import portal_login
urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path(
        "dashboard/",
        views.dashboard_home,
        name="dashboard_home"
    ),
    path("dashboard/bookings/", views.company_bookings, name="company_bookings"),
    path("dashboard/profile/", views.company_profile, name="company_profile"),
    path(
    "dashboard/cars/<int:car_id>/edit/",
    views.edit_car,
    name="edit_car"
),
    path("portal/login/", portal_login, name="portal_login"),
    path("portal/logout/", views.portal_logout, name="portal_logout"),
]

