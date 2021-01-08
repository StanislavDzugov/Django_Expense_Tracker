from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.description} - {self.amount}'

    class Meta:
        ordering: ['-date']
