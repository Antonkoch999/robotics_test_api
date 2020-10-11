from django.db import models
from django.contrib.auth.models import AbstractUser
from constans import USER_CLASS
# Create your models here.
from django.contrib.auth.models import Group, Permission


group1 = Group.objects.get_or_create(name='administrator')
group2 = Group.objects.get_or_create(name='dealer')
group3 = Group.objects.get_or_create(name='user')
can_add_plotter = Permission.objects.get(name='Can add plotter')
can_change_plotter = Permission.objects.get(name='Can change plotter')
can_delete_plotter = Permission.objects.get(name='Can delete plotter')
can_view_plotter = Permission.objects.get(name='Can view plotter')

can_add_template = Permission.objects.get(name='Can add template')
can_change_template = Permission.objects.get(name='Can change template')
can_delete_template = Permission.objects.get(name='Can delete template')
can_view_template = Permission.objects.get(name='Can view template')

can_add_user = Permission.objects.get(name='Can add user')
can_change_user = Permission.objects.get(name='Can change user')
can_delete_user = Permission.objects.get(name='Can delete user')
can_view_user = Permission.objects.get(name='Can view user')

group1[0].permissions.add(can_add_plotter)
group1[0].permissions.add(can_change_plotter)
group1[0].permissions.add(can_delete_plotter)
group1[0].permissions.add(can_view_plotter)

group1[0].permissions.add(can_add_template)
group1[0].permissions.add(can_change_template)
group1[0].permissions.add(can_delete_template)
group1[0].permissions.add(can_view_template)

group1[0].permissions.add(can_add_user)
group1[0].permissions.add(can_change_user)
group1[0].permissions.add(can_delete_user)
group1[0].permissions.add(can_view_user)

group2[0].permissions.add(can_add_user)
group2[0].permissions.add(can_change_user)
group2[0].permissions.add(can_add_plotter)
group2[0].permissions.add(can_change_plotter)
group2[0].permissions.add(can_view_plotter)
group2[0].permissions.add(can_view_user)

group3[0].permissions.add(can_view_plotter)


class User(AbstractUser):
    CLASS_USER = ((USER_CLASS[key], key) for key in USER_CLASS.keys())
    class_user = models.CharField(max_length=15,
                                  null=True, blank=True,
                                  choices=CLASS_USER, default='3')
    dealer_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} profile'


class Plotter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    format = models.CharField(max_length=25, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} plotter'


class Template(models.Model):
    name = models.CharField(max_length=50, blank=True)
    length = models.CharField(max_length=15, blank=True)
    width = models.CharField(max_length=15, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} lekalo'


