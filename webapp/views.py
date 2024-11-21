from http import HTTPStatus

from django import forms
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from webapp.models import Item
from webapp.utils.htmx import HTMX


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']


def index(request):
    return render(
        request,
        "index.jinja",
        context={
            "items": Item.objects.all(),
            "form": AddItemForm(),
            "error": request.GET.get("error", ""),
        })


def add_item(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()

    return redirect(
        reverse("items")
    )

class EditItemView(View):
    def delete(self, request, id: int):
        Item.objects.filter(id=id).delete()

        return HTMX.redirect(
            reverse("items"),
        )


    def post(self, request, id: int):
        item = Item.objects.get(id=id)
        item.completed = not item.completed
        item.save()

        return HTMX.redirect(
            reverse("items"),
        )
