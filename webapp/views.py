from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from webapp.forms import AddItemForm, AddListForm
from webapp.models import Item, List
from webapp.utils.htmx import HTMX


def index(request):
    return redirect(reverse('lists'))


class ItemsView(View):
    def get(self, request, list_id: int):
        return render(
            request,
            "items.jinja",
            context={
                "items": Item.objects.filter(list_id=list_id),
                "list": List.objects.get(id=list_id),
                "form": AddItemForm(),
            })

    def post(self, request, list_id: int):
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.instance.list_id = list_id
            form.save()

        return redirect(
            reverse("items", kwargs={"list_id": list_id}),
        )


class EditItemView(View):
    def delete(self, request, list_id: int, id: int):
        Item.objects.filter(list_id=list_id, id=id).delete()

        return HTMX.redirect(
            reverse("items", kwargs={"list_id": list_id}),
        )

    def post(self, request, list_id: int, id: int):
        item = Item.objects.get(list_id=list_id, id=id)
        item.completed = not item.completed
        item.save()

        return HTMX.redirect(
            reverse("items", kwargs={"list_id": list_id}),
        )


class ListView(View):
    def get(self, request):
        lists = List.objects.annotate(item_count=Count("items")).all()
        return render(
            request,
            "lists.jinja",
            context={
                "lists": lists,
                "form": AddListForm(),
            }
        )

    def post(self, request):
        form = AddListForm(request.POST)
        if form.is_valid():
            form.save()

        return HTMX.redirect(
            reverse("lists")
        )


class EditListView(View):
    def delete(self, request, id: int):
        List.objects.filter(id=id).delete()

        return HTMX.redirect(
            reverse("lists"),
        )


def health(request):
    return HttpResponse("OK")
