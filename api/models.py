"""This module create entities."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from constans import USER_CLASS
# Create your models here.
from rest_framework.reverse import reverse
from django.contrib.auth.models import Group, Permission


class User(AbstractUser):
    """This class expands the user entity."""

    CLASS_USER = ((USER_CLASS[key], key) for key in USER_CLASS.keys())
    class_user = models.CharField(max_length=15,
                                  null=True, blank=True,
                                  choices=CLASS_USER, default='3')
    dealer_id = models.IntegerField(null=True, blank=True)

    def get_dealer_url(self) -> str:
        """Get URL of specific dealer.

        :return: string format /api/v1/user/dealer/update/pk/
        """
        return reverse('api:user_dealer_update', kwargs={'pk': self.pk})

    def get_user_url(self) -> str:
        """Get URL of specific user.

        :return: string format /api/v1/user/update/pk/
        """
        return reverse('api:user_update', kwargs={'pk': self.pk})

    def get_user_user_url(self) -> str:
        """Get URL of specific user added by the user.

        :return: string format /api/v1/yser/user/update/pk/
        """
        return reverse('api:user_user_update', kwargs={'pk': self.pk})

    def __str__(self):
        """Give a name to the class instance."""
        return f'{self.first_name} profile'


class Plotter(models.Model):
    """This class create Plotter entity."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    format = models.CharField(max_length=25, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def get_plotter_update(self) -> str:
        """Get URL of specific plotter.

        :return: string format /api/v1/plotter/update/pk/
        """
        return reverse('api:plotter_update', kwargs={'pk': self.pk})

    def get_plotter_delete(self) -> str:
        """Get URL of specific plotter.

        :return: string format /api/v1/plotter/delete/pk/
        """
        return reverse('api:plotter_delete', kwargs={'pk': self.pk})

    def __str__(self):
        """Give a name to the class instance."""
        return f'{self.user} plotter'


class Template(models.Model):
    """This class create Template entity."""

    name = models.CharField(max_length=50, blank=True)
    length = models.CharField(max_length=15, blank=True)
    width = models.CharField(max_length=15, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def get_template_change(self) -> str:
        """Get URL of specific template.

        :return: string format /api/v1/template/update/pk/
        """
        return reverse('api:template_update', kwargs={'pk': self.pk})

    def __str__(self):
        """Give a name to the class instance."""
        return f'{self.name} lekalo'
