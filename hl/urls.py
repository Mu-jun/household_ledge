from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add),
    path('<int:id>/', views.detail),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('', views.index),
]
