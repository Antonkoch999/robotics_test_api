from django.db import models
from django.contrib.auth.models import AbstractUser
from constans import USER_CLASS
# Create your models here.
from rest_framework.reverse import reverse


class User(AbstractUser):
    CLASS_USER = ((USER_CLASS[key], key) for key in USER_CLASS.keys())
    class_user = models.CharField(max_length=15,
                                  null=True, blank=True,
                                  choices=CLASS_USER, default='3')
    dealer_id = models.IntegerField(null=True, blank=True)

    def get_dealer_url(self):
        return reverse('api:user_dealer_update', kwargs={'pk': self.pk})

    def get_user_url(self):
        return reverse('api:user_update', kwargs={'pk': self.pk})

    def get_user_user_url(self):
        return reverse('api:user_user_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.first_name} profile'


class Plotter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    format = models.CharField(max_length=25, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def get_plotter_update(self):
        return reverse('api:plotter_update', kwargs={'pk': self.pk})

    def get_plotter_delete(self):
        return reverse('api:plotter_delete', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user} plotter'


class Template(models.Model):
    name = models.CharField(max_length=50, blank=True)
    length = models.CharField(max_length=15, blank=True)
    width = models.CharField(max_length=15, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def get_template_change(self):
        return reverse('api:template_update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} lekalo'
