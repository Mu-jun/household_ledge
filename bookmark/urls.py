from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:id>', views.add),
    path('paste/<int:id>', views.paste),
    path('delete/<int:id>/', views.delete),
    path('', views.index),
]
