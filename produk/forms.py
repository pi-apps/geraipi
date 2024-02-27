from .models import Cart
from django import forms

class CartForm(forms.ModelForm):
    
    class Meta:
        model = Cart
        fields = "__all__"
