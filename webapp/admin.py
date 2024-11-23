from django.contrib import admin
from django.contrib.auth.models import User

from .models import Item, List

admin.site.register(List)
admin.site.register(Item)