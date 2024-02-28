from django import forms

from .models import UserStore


class UserStoreForm(forms.ModelForm):
    coin = forms.CharField(
        widget=forms.NumberInput(attrs={"readonly": "readonly", "required": False}),
        initial=0,
    )

    class Meta:
        model = UserStore
        fields = "__all__"
