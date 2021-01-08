from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from .models import UserModel
import json
import os


# Create your views here.

def index(request):
    user = UserModel.objects.get(user=request.user)
    if request.method == 'POST':
        currency = request.POST.get('currency')
        user.currency = currency
        user.save()
        messages.success(request, 'Changes saved')
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    return render(request, 'user/index.html', {'currencies': currency_data, 'currency': user.currency})
