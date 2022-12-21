from django.urls import path
from . import views

urlpatterns = [
    path('copy/<int:id>', views.copy),
    path('paste/<int:id>', views.paste),
    path('delete/<int:id>/', views.delete),
    path('', views.index),
]
