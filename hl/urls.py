from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add),
    path('detail/<int:id>/', views.detail),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),
    path('<str:url_key>', views.share),
    path('', views.index),
]
