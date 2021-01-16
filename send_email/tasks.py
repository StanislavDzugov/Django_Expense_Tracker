from celery import shared_task
from ExpenseTracker.celery import app
from .service import send
from .service import create_csv_file
from django.contrib.auth.models import User
from expenses.models import Expense
from income.models import Income


@app.task
def send_beat_email():
    users = User.objects.all()
    for user in users:
        expenses = Expense.objects.filter(owner=user)
        incomes = Income.objects.filter(owner=user)
        user_email = user.email
        send(user_email, create_csv_file(expenses, incomes))
