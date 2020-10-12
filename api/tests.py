from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from constans import USER_CLASS
from api.models import User, Plotter, Template
from django.contrib.auth.models import Group


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:registration'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticateGetTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='xx')
        self.client.login(username='admin', password='xx')

    def test_user_list_authenticated(self):
        response = self.client.get(reverse('api:user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_dealer_list(self):
        response = self.client.get(reverse('api:user_dealer_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_user_list(self):
        response = self.client.get(reverse('api:user_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plotter_user_list(self):
        response = self.client.get(reverse('api:plotter_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plotter_list(self):
        response = self.client.get(reverse('api:plotter_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_template_list(self):
        response = self.client.get(reverse('api:template_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:user_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_dealer_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:user_dealer_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_user_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:user_user_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_plotter_user_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:plotter_user_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_plotter_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:plotter_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_template_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('api:template_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionsGetTest(APITestCase):

    def setUp(self):

        self.group_administrator = Group.objects.get_or_create(
            name='administrator')[0]
        self.group_dealer = Group.objects.get_or_create(name='dealer')[0]
        self.group_user = Group.objects.get_or_create(name='user')[0]
        self.client = APIClient()
        self.user_administrator = User.objects.create_user(
            username='administrator',
            email='administrator@administrator.com',
            password='administrator',
        )
        self.user_dealer = User.objects.create_user(
            username='dealer',
            email='dealer@dealer.com',
            password='dealer',
        )
        self.user_user = User.objects.create_user(
            username='user',
            email='user',
            password='user',
        )

    def test_user_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        self.user_administrator.save()
        response = self.client.get(reverse('api:user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        self.user_dealer.save()
        response = self.client.get(reverse('api:user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        self.user_user.save()
        response = self.client.get(reverse('api:user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.get(reverse('api:user_dealer_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_dealer_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.get(reverse('api:user_dealer_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.get(reverse('api:user_dealer_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.get(reverse('api:user_user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.get(reverse('api:user_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_user_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.get(reverse('api:user_user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_user_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.get(reverse('api:plotter_user_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_user_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.get(reverse('api:plotter_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plotter_user_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.get(reverse('api:plotter_user_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plotter_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.get(reverse('api:plotter_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_plotter_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.get(reverse('api:plotter_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.get(reverse('api:plotter_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_list_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.get(reverse('api:template_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_template_list_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.get(reverse('api:template_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_list_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.get(reverse('api:template_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatePostTest(AuthenticateGetTest):

    def test_user_dealer_create_authenticate(self):
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_dealer_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_dealer_create_on_authenticate(self):
        self.client.force_authenticate(user=None)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_dealer_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_user_create_authenticate(self):
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_user_create_on_authenticate(self):
        self.client.force_authenticate(user=None)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_plotter_create_authenticate(self):
        data = {'user': self.user.id, 'format': 'A4', 'count': '13'}
        response = self.client.post(reverse('api:plotter_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_plotter_create_on_authenticate(self):
        self.client.force_authenticate(user=None)
        data = {'user': self.user.id, 'format': 'A4', 'count': '13'}
        response = self.client.post(reverse('api:plotter_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_template_create_authenticate(self):
        data = {'name': 'test', 'length': '123',
                'width': '1244', 'count': '123'}
        response = self.client.post(reverse('api:template_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_template_create_on_authenticate(self):
        self.client.force_authenticate(user=None)
        data = {'name': 'test', 'length': '123',
                'width': '1244', 'count': '123'}
        response = self.client.post(reverse('api:template_create'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionsPostTest(PermissionsGetTest):

    def test_user_dealer_create_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_dealer_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_dealer_create_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_dealer_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_create_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_dealer_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_create_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_create_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_user_create_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {"username": "test", "email": "test@test.com",
                "first_name": "test", "password": "test"}
        response = self.client.post(reverse('api:user_user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_create_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'user': self.user_administrator.id,
                'format': 'A4', 'count': '13'}
        response = self.client.post(reverse('api:plotter_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_plotter_create_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'user': self.user_dealer.id, 'format': 'A4', 'count': '13'}
        response = self.client.post(reverse('api:plotter_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_plotter_create_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'user': self.user_user.id, 'format': 'A4', 'count': '13'}
        response = self.client.post(reverse('api:plotter_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_create_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'name': 'test', 'length': '123',
                'width': '1244', 'count': '123'}
        response = self.client.post(reverse('api:template_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_template_create_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'name': 'test', 'length': '123',
                'width': '1244', 'count': '123'}
        response = self.client.post(reverse('api:template_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_create_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'name': 'test', 'length': '123',
                'width': '1244', 'count': '123'}
        response = self.client.post(reverse('api:template_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PermissionsPutTest(PermissionsGetTest):

    def setUp(self):

        super().setUp()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@test_user.com',
            password='test1user',
        )
        self.dealer = User.objects.create_user(
            username='test_dealer',
            email='test_dealer@test_dealer.com',
            password='test1dealer',
            class_user=USER_CLASS['Dealer'],
        )
        self.dealer_add_user = User.objects.create_user(
            username='dealer_add_user',
            email='dealer_add_user@dealer_add_user.com',
            password='dealer1add1user',
            dealer_id=self.user_dealer.id,
        )
        self.plotter = Plotter.objects.create(
            user=self.dealer,
            format='A5',
            count=33,
        )
        self.template = Template.objects.create(
            name='template',
            length='123',
            width='321',
            count=12,
        )

    def test_user_update_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse('api:user_update',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['password'], '12345')

    def test_user_update_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse('api:user_update',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse('api:user_update',
                                           kwargs={"pk": self.user.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_update_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse(
            'api:user_dealer_update',
            kwargs={"pk": self.dealer.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.dealer.id)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['password'], '12345')

    def test_user_dealer_update_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse('api:user_dealer_update',
                                           kwargs={"pk": self.dealer.pk}),
                                   data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_update_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse('api:user_dealer_update',
                                           kwargs={"pk": self.dealer.pk}),
                                   data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_update_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse(
            'api:user_user_update',
            kwargs={"pk": self.dealer_add_user.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_user_update_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse(
            'api:user_user_update',
            kwargs={"pk": self.dealer_add_user.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.dealer_add_user.id)
        self.assertEqual(response.data['username'], 'test')
        self.assertEqual(response.data['email'], 'test@test.com')
        self.assertEqual(response.data['password'], '12345')

    def test_user_user_update_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'username': 'test', 'email': 'test@test.com',
                'password': '12345'}
        response = self.client.put(reverse(
            'api:user_user_update',
            kwargs={"pk": self.dealer_add_user.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_update_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'user': self.user_administrator.id,
                'format': 'A1', 'count': 10}
        response = self.client.put(reverse(
            'api:plotter_update',
            kwargs={"pk": self.plotter.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_administrator.id)
        self.assertEqual(response.data['format'], 'A1')
        self.assertEqual(response.data['count'], 10)

    def test_plotter_update_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'user': self.user_administrator.id,
                'format': 'A1', 'count': 10}
        response = self.client.put(reverse(
            'api:plotter_update',
            kwargs={"pk": self.plotter.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_administrator.id)
        self.assertEqual(response.data['format'], 'A1')
        self.assertEqual(response.data['count'], 10)

    def test_plotter_update_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'user': self.user_administrator.id,
                'format': 'A1', 'count': 10}
        response = self.client.put(reverse(
            'api:plotter_update',
            kwargs={"pk": self.plotter.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_update_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        data = {'name': 'test', 'length': '456', 'width': '654', 'count': 33}
        response = self.client.put(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['length'], '456')
        self.assertEqual(response.data['width'], '654')
        self.assertEqual(response.data['count'], 33)

    def test_template_update_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        data = {'name': 'test', 'length': '456', 'width': '654', 'count': 33}
        response = self.client.put(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_update_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        data = {'name': 'test', 'length': '456', 'width': '654', 'count': 33}
        response = self.client.put(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PermissionsDeleteTest(PermissionsPutTest):

    def test_user_delete_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.delete(reverse('api:user_update',
                                              kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_delete_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.delete(reverse('api:user_update',
                                              kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.delete(reverse('api:user_update',
                                              kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_delete_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.delete(reverse('api:user_dealer_update',
                                              kwargs={"pk": self.dealer.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_dealer_delete_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.delete(reverse('api:user_dealer_update',
                                              kwargs={"pk": self.dealer.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_dealer_delete_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.delete(reverse('api:user_dealer_update',
                                              kwargs={"pk": self.dealer.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_delete_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.delete(reverse(
            'api:plotter_delete',
            kwargs={"pk": self.plotter.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_plotter_delete_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.delete(reverse(
            'api:plotter_delete',
            kwargs={"pk": self.plotter.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_plotter_delete_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.delete(reverse(
            'api:plotter_delete',
            kwargs={"pk": self.plotter.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_delete_permissions_administrator(self):
        self.client.login(username='administrator', password='administrator')
        self.user_administrator.groups.add(self.group_administrator)
        response = self.client.delete(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_template_delete_permissions_dealer(self):
        self.client.login(username='dealer', password='dealer')
        self.user_dealer.groups.add(self.group_dealer)
        response = self.client.delete(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_delete_permissions_user(self):
        self.client.login(username='user', password='user')
        self.user_user.groups.add(self.group_user)
        response = self.client.delete(reverse(
            'api:template_update',
            kwargs={"pk": self.template.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
