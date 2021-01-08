from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from authentication.forms import CreateUserForm
import json

# Create your views here.



class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({
                'username_error': 'Username should only contain alphanumeric characters'
            }, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': 'Username already exists, put another one'
            }, status=400)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'email_error': 'Email is invalid'
            }, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': 'Email already exists, put another one'
            }, status=400)
        return JsonResponse({'email_valid': True})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}')
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'auth/register.html', context)


class LoginView(View):
    def get(self, request):
        context = {}
        return render(request, 'auth/login.html', context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expenses')
        else:
            messages.error(request, 'Username or Password is incorrect!')

        context = {}
        return render(request, 'auth/login.html', context)


def userlogout(request):
    logout(request)
    return redirect('login')

