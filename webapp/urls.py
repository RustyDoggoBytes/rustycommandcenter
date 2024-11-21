from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('health', views.health, name='health'),
    path('ready', views.health, name='ready'),
    path('lists', views.ListView.as_view(), name='lists'),
    path('lists/<int:id>', views.EditListView.as_view(), name='edit-lists'),
    path('lists/<int:list_id>/items', views.ItemsView.as_view(), name='items'),
    path('lists/<int:list_id>/items/<int:id>', views.EditItemView.as_view(), name='edit-items'),

]