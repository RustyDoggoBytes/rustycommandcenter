from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class List(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(BaseModel):
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    list = models.ForeignKey(List, related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

