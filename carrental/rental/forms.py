from django import forms
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ("company",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "car_type": forms.Select(attrs={"class": "form-select"}),
            "price_per_day": forms.NumberInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "seats": forms.NumberInput(attrs={"class": "form-control"}),
            "power": forms.NumberInput(attrs={"class": "form-control"}),
            "fuel": forms.Select(attrs={"class": "form-select"}),
            "gear": forms.Select(attrs={"class": "form-select"}),
            "engine_size": forms.TextInput(attrs={"class": "form-control"}),
        }


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ("image",)
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            )
        }
