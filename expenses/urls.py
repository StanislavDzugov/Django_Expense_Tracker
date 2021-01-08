from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<str:pk>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<str:pk>', views.delete_expense, name='delete-expense'),
    path('search-expense/', csrf_exempt(views.search_expense), name='search-expense'),
    path('expense-stats/', csrf_exempt(views.expense_stats), name='expense-stats'),
    path('expense-stats-date/', csrf_exempt(views.expense_stats_date), name='expense-stats-date'),
    path('expense-summary/', views.expense_category_summary, name='expense-summary'),
]