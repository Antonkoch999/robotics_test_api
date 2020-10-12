"""This module contains the logic of our application."""
import api.models as models
from rest_framework import generics
from api.serializers import (UserListSerializer, UserRegisterSerializer,
                             UserDetailList, PlotterAddSerializer,
                             TemplateAddSerializer, PlotterDetailList,
                             TemplateDetailList, UserDealerCreate,
                             UserUserCreate, DealerListSerializer,
                             UserUserListSerializer
                             )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from constans import USER_CLASS
from api.permissions import IsAdministrator, IsDealer, IsUser
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET'])
def api_root(request) -> Response:
    """Entry endpoints of our API.

    :param request: HTTP GET request
    :return:        Instance of Response class
    """
    return Response({
        'users list': reverse('api:user_list', request=request),
        'user registration': reverse('api:registration', request=request),
        'user dealer list': reverse('api:user_dealer_list', request=request),
        'user dealer create': reverse('api:user_dealer_create',
                                      request=request),
        'user user list': reverse('api:user_user_list', request=request),
        'user user create': reverse('api:user_user_create', request=request),
        'plotter user list': reverse('api:plotter_user_list', request=request),
        'plotter list': reverse('api:plotter_list', request=request),
        'plotter create': reverse('api:plotter_create', request=request),
        'template list': reverse('api:template_list', request=request),
        'template create': reverse('api:template_create', request=request),
    })


class UserRegisterView(generics.CreateAPIView):
    """This class view for creating a user model instance."""

    serializer_class = UserRegisterSerializer


class UserListView(generics.ListAPIView):
    """This class view to display a user model instances all.

    View is available only to the group 'administrator'.
    """

    serializer_class = UserListSerializer
    queryset = models.User.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """This class view to display a detail user model instances all.

    View is available only to the group 'administrator'.
    """

    serializer_class = UserDetailList
    queryset = models.User.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerListView(generics.ListAPIView):
    """This class view to display a user model instances.

    With attribute class_user = 'Dealer'.
    View is available only to the group 'administrator'.
    """

    serializer_class = DealerListSerializer
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerCreateView(generics.ListCreateAPIView):
    """This class view for creating and display a user model instances.

    With attribute class_user = 'Dealer'. View and create are available only to
    the group 'administrator'.
    """

    serializer_class = UserDealerCreate
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """This class view for updating and deleting specific user model instance.

    With attribute class_user = 'Dealer'.
    Update and Delete are available only to the group 'administrator'.
    """

    serializer_class = UserDetailList
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserUserListView(generics.ListAPIView):
    """This class view to display a user model instances.

    Added by the user with group 'dealer'.
    View is available only to the group 'dealer'.
    """

    serializer_class = UserUserListSerializer
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )

    def get_queryset(self) -> list:
        """Get list of user model instances.

        With attribute dealer_id equals id authenticated user.

        :return: list of user model instances
        """
        user = self.request.user.pk
        return models.User.objects.filter(dealer_id=user)


class UserUserCreateView(generics.CreateAPIView):
    """This class view for creating a user model instance.

    With attribute dealer_id equals id of user who is adding.
    Adding is available only to the group 'dealer'.
    """

    serializer_class = UserUserCreate
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )


class UserUserUpdateView(generics.RetrieveUpdateAPIView):
    """This class view to display a user model instance.

    With attribute dealer_id equals id authenticated user.
    View is available only to the group 'dealer'.
    """

    serializer_class = UserDetailList
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )

    def get_queryset(self) -> list:
        """Get list of user model instances.

        With attribute dealer_id equals equals id authenticated user.

        :return: list of user model instances
        """
        user = self.request.user.pk
        return models.User.objects.filter(dealer_id=user)


class PlotterDealerList(generics.ListAPIView):
    """This class view to display a plotter model instances.

    With attribute user equals id authenticated user.
    View is available only to group 'dealer' and 'user'.
    """

    serializer_class = PlotterDetailList
    permission_classes = (IsDealer | IsUser | IsAdminUser, IsAuthenticated, )

    def get_queryset(self) -> list:
        """Get list of plotter model instances.

        With attribute user equals id authenticated user.

        :return: list of plotter model instances
        """
        user = self.request.user.pk
        return models.Plotter.objects.filter(user=user)


class PlotterListView(generics.ListAPIView):
    """This view class to display a plotter model instances all.

    View is available only to the group 'administrator'.
    """

    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class PlotterAddView(generics.CreateAPIView):
    """This view class for creating a plotter model instance.

    Creating is available only to group 'administrator' and 'dealer'.
    """

    serializer_class = PlotterAddSerializer
    permission_classes = (IsAdministrator | IsDealer | IsAdminUser,
                          IsAuthenticated, )


class PlotterUpdateView(generics.RetrieveUpdateAPIView):
    """This view class for updating a plotter model instance.

    Updating is available only to group 'administrator' and 'dealer'.
    """

    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsDealer | IsAdminUser,
                          IsAuthenticated, )


class PlotterDeleteView(generics.RetrieveDestroyAPIView):
    """This view class for deleting a plotter model instance.

    Deleting is available only to the group 'administrator'.
    """

    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateListView(generics.ListAPIView):
    """This view class to display a template model instances all.

    View is available only to the group 'administrator'.
    """

    serializer_class = TemplateDetailList
    queryset = models.Template.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateAddView(generics.CreateAPIView):
    """This view class for creating a plotter model instance.

    Creating is available only to the group 'administrator'.
    """

    serializer_class = TemplateAddSerializer
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """This view class for update and delete a template model instance.

    Updating and Deleting are available only to the group 'administrator'.
    """

    serializer_class = TemplateDetailList
    queryset = models.Template.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )

