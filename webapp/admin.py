from django.contrib import admin

from .models import Item, List, Meal, User

admin.site.register(List)
admin.site.register(Item)
admin.site.register(Meal)
admin.site.register(User)
