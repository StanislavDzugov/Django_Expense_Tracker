from django.core.mail import EmailMessage
import csv
from io import StringIO


def send(user_email, attachment_csv_file):
    email = EmailMessage(
        'Monthly report',
        'Please, find attached monthly report',
        'djangoemailsend@gmail.com',
        [user_email],
    )
    email.attach('Monthly_report.csv', attachment_csv_file.getvalue(), 'text/csv')
    email.send(fail_silently=True)


def create_csv_file(expenses, incomes):
    attachment_csv_file = StringIO()
    writer = csv.writer(attachment_csv_file)
    writer.writerow(['EXPENSES'])
    writer.writerow(['Amount', 'Category', 'Description', 'Date'])
    for expense in expenses:
        writer.writerow([expense.amount, expense.category, expense.description, expense.date])
    writer.writerow(['-----------------------------------------'])
    writer.writerow(['INCOMES'])
    writer.writerow(['Amount', 'Source', 'Description', 'Date'])
    for income in incomes:
        writer.writerow([income.amount, income.source, income.description, income.date])
    return attachment_csv_file
