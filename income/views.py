import collections
import datetime

from django.shortcuts import render
from django.contrib import messages
from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Source, Income
from userpart.models import UserModel
from .forms import IncomeForm
from django.http import JsonResponse
import json


# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(source__istartswith=search_str, owner=request.user) | \
                   Income.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Income.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Income.objects.filter(amount__istartswith=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def index(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    user = UserModel.objects.get(user=request.user)
    currency = UserModel.objects.get(user=request.user).currency
    context = {
        'sources': sources,
        'incomes': incomes,
        'user': user,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='login')
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    form = IncomeForm(instance=income)
    if request.method == "POST":
        owner = {'owner': request.user}
        querydict = QueryDict('', mutable=True)
        querydict.update(request.POST)
        querydict.update(owner)
        form = IncomeForm(querydict, instance=income)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income edited successfully')
            return redirect('income')
    sources = Source.objects.all()
    context = {'form': form, 'sources': sources, 'income': income}
    return render(request, 'income/edit-income.html', context)


@login_required(login_url='login')
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    messages.info(request, 'Income was deleted')
    return redirect('income')


@login_required(login_url='login')
def add_income(request):
    form = IncomeForm()
    if request.method == 'POST':
        owner = {'owner': request.user}
        querydict = QueryDict('', mutable=True)
        querydict.update(request.POST)
        querydict.update(owner)
        form = IncomeForm(querydict)
        if form.is_valid():
            form.save()
            messages.success(request, f'Income added successfully')
            return redirect('income')
        else:
            messages.error(request, form.errors)

    sources = Source.objects.all()
    context = {'sources': sources, 'form': form}
    return render(request, 'income/add-income.html', context)


@login_required(login_url='login')
def income_stats(request):
    today_date = datetime.date.today()
    year_ago = today_date - datetime.timedelta(days=365)
    incomes = Income.objects.filter(date__gte=year_ago,
                                      date__lte=today_date,
                                      owner=request.user)
    source_amount = {}
    for income in incomes:
        if income.source in source_amount.keys():
            source_amount[income.source] += income.amount
        else:
            source_amount[income.source] = income.amount
    return JsonResponse(source_amount)


@login_required(login_url='login')
def income_stats_date(request):
    incomes = Income.objects.filter(owner=request.user)
    date_amount = {}
    for income in incomes:
        if str(income.date) in date_amount.keys():
            date_amount[str(income.date)] += income.amount
        else:
            date_amount[str(income.date)] = income.amount
    od = collections.OrderedDict(sorted(date_amount.items()))
    od = collections.OrderedDict(reversed(list(od.items())))
    return JsonResponse(od)


@login_required(login_url='login')
def income_source_summary(request):
    currency = UserModel.objects.get(user=request.user).currency
    return render(request, 'income/income_summary.html', {'currency': currency})