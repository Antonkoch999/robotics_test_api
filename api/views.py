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
def api_root(request):
    """
    The entry endpoint of our API.
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
    serializer_class = UserRegisterSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = models.User.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailList
    queryset = models.User.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerListView(generics.ListAPIView):
    serializer_class = DealerListSerializer
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerCreateView(generics.ListCreateAPIView):
    serializer_class = UserDealerCreate
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserDealerUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailList
    queryset = models.User.objects.filter(class_user=USER_CLASS['Dealer'])
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class UserUserListView(generics.ListAPIView):
    serializer_class = UserUserListSerializer
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user.pk
        return models.User.objects.filter(dealer_id=user)


class UserUserCreateView(generics.CreateAPIView):
    serializer_class = UserUserCreate
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )


class UserUserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailList
    permission_classes = (IsDealer | IsAdminUser, IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user.pk
        return models.User.objects.filter(dealer_id=user)


class PlotterDealerList(generics.ListAPIView):
    serializer_class = PlotterDetailList
    permission_classes = (IsDealer | IsUser | IsAdminUser, IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user.pk
        return models.Plotter.objects.filter(user=user)


class PlotterListView(generics.ListAPIView):
    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class PlotterAddView(generics.CreateAPIView):
    serializer_class = PlotterAddSerializer
    permission_classes = (IsAdministrator | IsDealer | IsAdminUser,
                          IsAuthenticated, )


class PlotterUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsDealer | IsAdminUser,
                          IsAuthenticated, )


class PlotterDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = PlotterDetailList
    queryset = models.Plotter.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateListView(generics.ListAPIView):
    serializer_class = TemplateDetailList
    queryset = models.Template.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateAddView(generics.CreateAPIView):
    serializer_class = TemplateAddSerializer
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )


class TemplateUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TemplateDetailList
    queryset = models.Template.objects.all()
    permission_classes = (IsAdministrator | IsAdminUser, IsAuthenticated, )

