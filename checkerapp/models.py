from django.db import models


# Create your models here.
class CheckerModel(models.Model):
    password = models.CharField(max_length=50)

    data = models.TextField()

    def __str__(self):
        return 'data=' + self.password + ":" + self.data


class Meta:
    ordering = ['password', ]