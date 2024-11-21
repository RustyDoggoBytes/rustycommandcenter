from django import forms

from webapp.models import Item, List


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']

class AddListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name']
