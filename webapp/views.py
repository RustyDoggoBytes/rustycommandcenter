from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import AddItemForm, AddListForm, LoginForm
from webapp.models import Item, List
from webapp.utils.htmx import HTMX


@login_required(login_url="/login/")
def index(request):
    return redirect(reverse('dashboard'))


class CalendarView(TemplateView):
    template_name = "calendar.jinja"

class DashboardView(View):
    def get(self, request):
        return render(
            request,
            "dashboard.jinja",
            context={
                "user_chores": [
                    {
                        "name": "Everybody",
                        "chores": [
                            "Feed Rusty Breakfast",
                            "Fill Rusty's Water",
                            "Take Trash Out",
                            "Do bed laundry",
                        ],
                        "completed_chores": [
                            "Make Popcorn",
                            "Feed Rusty",
                        ]
                    },
                    {
                        "name": "Ivan",
                        "chores": [
                            "Do Dishes",
                            "Take Trash Out",
                            "Do bed laundry",
                        ],
                        "completed_chores": [
                            "Make Popcorn",
                            "Feed Rusty",
                        ]
                    },
                    {
                        "name": "Megan",
                        "chores": [
                            "Prepare Salads",
                            "Make breakfast",
                        ],
                        "completed_chores": [
                            "Make Popcorn",
                            "Feed Rusty",
                        ]
                    },
                    {
                        "name": "Isabela",
                        "chores": [
                            "Shower",
                            "Brush teeth",
                            "Put Toys Away",
                        ],
                        "completed_chores": [
                        ]
                    },
                    {
                        "name": "Luca",
                        "chores": [
                            "Shower",
                            "Brush teeth",
                            "Put Toys Away",
                        ],
                        "completed_chores": [
                        ]
                    }
                ]


            }
            )

class CustomLoginView(LoginView):
    template_name = 'registration/login.jinja'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('index')


class ItemsView(LoginRequiredMixin, View):
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


class EditItemView(LoginRequiredMixin,View):
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


class ListView(LoginRequiredMixin,View):
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


class EditListView(LoginRequiredMixin,View):
    def delete(self, request, id: int):
        List.objects.filter(id=id).delete()

        return HTMX.redirect(
            reverse("lists"),
        )


def health(request):
    return HttpResponse("OK")
