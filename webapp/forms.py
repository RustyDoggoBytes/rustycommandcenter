from django import forms
from django.forms import modelformset_factory

from webapp.models import Item, List, Meal, DOW_CHOICES


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name"]


class AddListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["name"]


class MealForm(forms.ModelForm):
    day_of_week = forms.ChoiceField(choices=DOW_CHOICES, widget=forms.HiddenInput)

    class Meta:
        model = Meal
        fields = ["day_of_week", "breakfast", "lunch", "dinner"]


MealFormSet = modelformset_factory(Meal, form=MealForm, extra=0)
