from .views import ResgistrationView, UserNameValidationView, EmailValidationView, LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from authentication import views 


urlpatterns = [
    path('register', ResgistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"), 
    path('validate-username', csrf_exempt(UserNameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate_email")
]
