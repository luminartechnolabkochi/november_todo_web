from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Todos(models.Model):
    task_name=models.CharField(max_length=120)
    completed=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.task_name


# loaclhost:8000:/todos/accounts/register
#
