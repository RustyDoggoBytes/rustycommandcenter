from datetime import datetime
from zoneinfo import ZoneInfo

from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    name = models.CharField(max_length=100)

    @property
    def chores(self):
        return Item.chores_objects.filter(user=self)

    def __str__(self):
        return self.name


class List(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChoresManager(models.Manager):
    def get_queryset(self):
        # This will be used by default and always filter by list_id=0
        return super().get_queryset().filter(list__name="chores")


class Item(BaseModel):
    objects = models.Manager()
    chores_objects = ChoresManager()

    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    list = models.ForeignKey(List, related_name="items", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="items",
        related_query_name="item",
    )
    recurring = models.BooleanField(default=False)

    def complete_task(self):
        self.completed = not self.completed
        self.save()

        if self.completed and self.recurring:
            Item.objects.create(
                name=self.name, list=self.list, user=self.user, recurring=True
            )

    def relative_date_string(self):
        # Get today's date
        today = datetime.today().date()

        # Calculate the difference between the given date and today
        delta = self.created.date() - today

        if delta.days == 0:
            return "Today"
        elif delta.days == 1:
            return "Tomorrow"
        elif delta.days == -1:
            return "Yesterday"
        elif delta.days > 1:
            return f"Due in {delta.days} days"
        elif delta.days < -1:
            return f"Due {abs(delta.days)} days ago"

    def __str__(self):
        return f"{self.id} {self.name} - u{self.user} - r{self.recurring}"


DOW_CHOICES = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]


class Meal(BaseModel):
    day_of_week = models.IntegerField(choices=DOW_CHOICES)
    breakfast = models.CharField(max_length=100, default="", blank=True)
    lunch = models.CharField(max_length=100, default="", blank=True)
    dinner = models.CharField(max_length=100, default="", blank=True)

    @staticmethod
    def today():
        timezone = ZoneInfo("America/Denver")
        today = datetime.now(timezone).date().weekday()
        today_meal, _ = Meal.objects.get_or_create(
            day_of_week=today,
        )
        return today_meal

    def get_dow_display(self):
        return DOW_CHOICES[self.day_of_week][1]

    def __str__(self):
        return f"{self.day_of_week} {self.breakfast} / {self.lunch} / {self.dinner}"
