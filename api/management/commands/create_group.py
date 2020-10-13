from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        groups = {'administrator': None, 'dealer': None, 'user': None}

        for group in groups.keys():
            groups[group] = Group.objects.get_or_create(name=group)[0]
            groups[group].save()

        permission_administrator_list = (
            'Can add plotter', 'Can change plotter',
            'Can delete plotter', 'Can view plotter',
            'Can add template', 'Can change template',
            'Can delete template',
            'Can view template',
            'Can add user', 'Can change user',
            'Can delete user',
            'Can view user')

        permission_dealer_list = ('Can add user', 'Can change user',
                                  'Can add plotter', 'Can change plotter',
                                  'Can view plotter', 'Can view user')

        permission_user_list = ('Can view plotter',)

        permission_dealer = Permission.objects.filter(
            name__in=permission_dealer_list)
        permission_user = Permission.objects.filter(
            name__in=permission_user_list)
        permission_administrator = Permission.objects.filter(
            name__in=permission_administrator_list)

        groups['administrator'].permissions.add(*permission_administrator)
        groups['dealer'].permissions.add(*permission_dealer)
        groups['user'].permissions.add(*permission_user)
        groups['administrator'].save()
        groups['user'].save()
        groups['dealer'].save()
