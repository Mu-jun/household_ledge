from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path('signUp/', views.sign_up),
    path('signIn/', views.sign_in, name="sign_in"),
    path('signOut', views.sign_out, name="sign_out"),
    path('refresh/', views.refresh, name="refresh")
]