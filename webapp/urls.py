from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from webapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('health/', views.health, name='health'),
    path('ready/', views.health, name='ready'),
    path('lists/', views.ListView.as_view(), name='lists'),
    path('lists/<int:id>/', views.EditListView.as_view(), name='edit-lists'),
    path('lists/<int:list_id>/items/', views.ItemsView.as_view(), name='items'),
    path('lists/<int:list_id>/items/<int:id>/', views.EditItemView.as_view(), name='edit-items'),

]