from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import register, UsernameValidationView, EmailValidationView, LoginView, userlogout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', userlogout, name='logout'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-email'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email')
]