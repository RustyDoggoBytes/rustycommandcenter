from django import forms

from webapp.models import Item, List

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']

class AddListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
