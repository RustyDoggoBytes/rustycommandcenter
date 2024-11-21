from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.index, name='items'),
    path('items', views.add_item, name='add-item'),
    path('items/<int:id>', views.EditItemView.as_view(), name='edit-item'),

]