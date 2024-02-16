from django.urls import path

from . import views
from profile_app.apis.authentication.login import Login
from .apis.authentication.signup_send_otp import SignUpSendOTP
from .apis.authentication.signup_verify_otp import SignUpVerifyOTP

# from .apis.authentication import Login

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", Login.as_view(), name='login'),
    path("signup/", SignUpSendOTP.as_view(), name='signup-send-otp'),
    path("signup/otp/", SignUpVerifyOTP.as_view(), name='signup-verify-otp'),
]
