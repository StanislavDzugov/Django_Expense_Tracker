from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import JsonResponse, HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from authentication.forms import CreateUserForm
import json
from authentication.tokens import account_activation_token


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
            user_email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            email_body = render_to_string('auth/email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@expenseapp.com',
                [user_email],
            )
            email.send(fail_silently=True)
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            messages.error(request, form.errors)
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'auth/register.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


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

