from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.description} - {self.amount}'

    class Meta:
        ordering: ['-date']

