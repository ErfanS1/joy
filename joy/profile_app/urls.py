from django.urls import path

from . import views
from profile_app.apis.authentication.login import Login
from .apis.authentication.signup import SignUp

# from .apis.authentication import Login

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", Login.as_view(), name='login'),
    path("signup/", SignUp.as_view(), name='signup')
]
