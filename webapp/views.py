from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import AddItemForm, AddListForm, MealFormSet
from webapp.models import Item, List, Meal, User
from webapp.utils.htmx import HTMX


@login_required(login_url="/login/")
def index(request):
    return redirect(reverse("dashboard"))


class CalendarView(TemplateView):
    template_name = "calendar.jinja"


def meal_plan_view(request):
    # Fetch existing meals for the week (dow=0 to dow=6)
    meals = Meal.objects.filter(day_of_week__in=range(7))

    # If meals are not already in the database for each day, create a default Meal instance for each dow
    for dow in range(7):
        if not meals.filter(day_of_week=dow).exists():
            Meal.objects.create(
                day_of_week=dow
            )  # Create empty meal if it doesn't exist for the day

    formset = MealFormSet(
        queryset=Meal.objects.filter(day_of_week__in=range(7)).order_by("day_of_week")
    )

    if request.method == "POST":
        formset = MealFormSet(request.POST)

        if formset.is_valid():
            formset.save()

    return render(request, "meal_plan.jinja", {"formset": formset})


def dashboard_meal_view(request):
    return render(
        request,
        "dashboard_meals.jinja",
        context={
            "meals": Meal.today(),
        },
    )


class DashboardView(View):
    def get(self, request):
        user_chores = []
        for user in User.objects.all():
            user_chores.append(
                {
                    "name": user.name,
                    "chores": Item.chores_objects.filter(user=user, completed=False),
                    "completed_chores": Item.chores_objects.filter(
                        user=user, completed=True
                    ),
                }
            )

        return render(
            request,
            "dashboard.jinja",
            context={
                "user_chores": user_chores,
            },
        )


def dashboard_complete_task(request, id: int):
    item = Item.chores_objects.get(id=id)
    item.complete_task()

    return HTMX.redirect(reverse("dashboard"))


class ItemsView(View):
    def get(self, request, list_id: int):
        return render(
            request,
            "items.jinja",
            context={
                "items": Item.objects.filter(list_id=list_id),
                "list": List.objects.get(id=list_id),
                "form": AddItemForm(),
            },
        )

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
        item.complete_task()

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
            },
        )

    def post(self, request):
        form = AddListForm(request.POST)
        if form.is_valid():
            form.save()

        return HTMX.redirect(reverse("lists"))


class EditListView(View):
    def delete(self, request, id: int):
        List.objects.filter(id=id).delete()

        return HTMX.redirect(
            reverse("lists"),
        )


def health(request):
    return HttpResponse("OK")


def test(request):
    return render(request, "test.jinja")
