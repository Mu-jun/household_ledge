from django.urls import path
from . import views

app_name = "hl"

urlpatterns = [
    path('add/', views.add),
    path('<int:id>/', views.household_ledge),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('<str:url_key>', views.share),
    path('', views.index),
]
