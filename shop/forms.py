from django import forms
from .models import Order


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "style": "width:90px"})
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "phone", "address", "city", "notes"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom et prénom"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@exemple.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+221 77 000 00 00"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Adresse de livraison"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Instructions particulières (facultatif)"}),
        }
