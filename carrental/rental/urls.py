
from django.urls import path
from django.shortcuts import render, get_object_or_404
from . import views

urlpatterns = [
    path('', views.home, name='home'),         
    path('cars/', views.cars, name='cars'), 
    path('cars/<int:car_id>/', views.car_details, name='car_details'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path(
        "booking/success/<str:reference>/",
        views.booking_success,
        name="booking_success"
    ),
    path("dashboard/cars/", views.my_cars, name="my_cars"),
    path("dashboard/cars/add/", views.add_car, name="add_car"),


    path(
    "booking/lookup/",
    views.booking_lookup,
    name="booking_lookup"
    
),
    path(
    "dashboard/bookings/approve/<int:booking_id>/",
    views.approve_booking,
    name="approve_booking"
),
path(
    "dashboard/bookings/cancel/<int:booking_id>/",
    views.cancel_booking,
    name="cancel_booking"
),

path(
    "dashboard/cars/image/<int:image_id>/delete/",
    views.delete_car_image,
    name="delete_car_image"
),
path(
    "dashboard/cars/image/<int:image_id>/main/",
    views.set_main_car_image,
    name="set_main_car_image"
),
path(
  "dashboard/bookings/bulk-update/",
  views.bulk_update_bookings,
  name="bulk_update_bookings"
),

]
