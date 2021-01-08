import collections
from collections import OrderedDict

from django.contrib import messages
from django.http import QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Category, Expense
from userpart.models import UserModel
from .forms import ExpenseForm
from django.http import JsonResponse
import datetime
import json


# Create your views here.

def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(category__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Expense.objects.filter(date__istartswith=search_str, owner=request.user) | \
                   Expense.objects.filter(amount__istartswith=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    user = UserModel.objects.get(user=request.user)
    currency = UserModel.objects.get(user=request.user).currency
    context = {
        'categories': categories,
        'expenses': expenses,
        'user': user,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='login')
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseForm(instance=expense)
    if request.method == "POST":
        owner = {'owner': request.user}
        querydict = QueryDict('', mutable=True)
        querydict.update(request.POST)
        querydict.update(owner)
        form = ExpenseForm(querydict, instance=expense)
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense edited successfully')
            return redirect('expenses')
    categories = Category.objects.all()
    context = {'form': form, 'categories': categories, 'expense': expense}
    return render(request, 'expenses/edit-expense.html', context)


@login_required(login_url='login')
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.info(request, 'Expense was deleted')
    return redirect('expenses')


@login_required(login_url='login')
def add_expense(request):
    form = ExpenseForm()
    if request.method == 'POST':
        owner = {'owner': request.user}
        querydict = QueryDict('', mutable=True)
        querydict.update(request.POST)
        querydict.update(owner)
        form = ExpenseForm(querydict)
        if form.is_valid():
            form.save()
            messages.success(request, f'Expense added successfully')
            return redirect('expenses')
        else:
            messages.error(request, form.errors)

    categories = Category.objects.all()
    context = {'categories': categories, 'form': form}
    return render(request, 'expenses/add-expense.html', context)

@login_required(login_url='login')
def expense_stats(request):
    today_date = datetime.date.today()
    year_ago = today_date - datetime.timedelta(days=365)
    expenses = Expense.objects.filter(date__gte=year_ago,
                                      date__lte=today_date,
                                      owner=request.user)
    category_amount = {}
    for expense in expenses:
        if expense.category in category_amount.keys():
            category_amount[expense.category] += expense.amount
        else:
            category_amount[expense.category] = expense.amount
    return JsonResponse(category_amount)

@login_required(login_url='login')
def expense_stats_date(request):
    expenses = Expense.objects.filter(owner=request.user)
    date_amount = {}
    for expense in expenses:
        if str(expense.date) in date_amount.keys():
            date_amount[str(expense.date)] += expense.amount
        else:
            date_amount[str(expense.date)] = expense.amount
    od = collections.OrderedDict(sorted(date_amount.items()))
    od = collections.OrderedDict(reversed(list(od.items())))
    print(od)
    return JsonResponse(od)

@login_required(login_url='login')
def expense_category_summary(request):
    currency = UserModel.objects.get(user=request.user).currency
    return render(request, 'expenses/expenses_summary.html', {'currency': currency})

