from django.urls import path

from webapp import views
from webapp.views import (
    DashboardView,
    CalendarView,
    dashboard_complete_task,
    meal_plan_view,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/tasks/<int:id>/complete",
        dashboard_complete_task,
        name="dashboard-task-complete",
    ),
    path("dashboard-meals/", views.dashboard_meal_view, name="dashboard-meal"),
    path(
        "dashboard-chores/<int:user_id>/",
        views.dashboard_chores,
        name="dashboard-chores",
    ),
    path("chores/", views.chores, name="chores"),
    path("chores/<int:id>", views.chores_edit, name="chores-edit"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("meal-plan/", meal_plan_view, name="meal-plan"),
    path("health/", views.health, name="health"),
    path("ready/", views.health, name="ready"),
    path("lists/", views.ListView.as_view(), name="lists"),
    path("lists/<int:id>/", views.EditListView.as_view(), name="edit-lists"),
    path("lists/<int:list_id>/items/", views.ItemsView.as_view(), name="items"),
    path(
        "lists/<int:list_id>/items/<int:id>/",
        views.EditItemView.as_view(),
        name="edit-items",
    ),
    path("test/", views.test, name="test"),
]
