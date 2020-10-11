import api.models as models
from rest_framework import generics
from api.serializers import (UserListSerializer, UserRegisterSerializer,
                             UserDetailList, PlotterAddSerializer,
                             TemplateAddSerializer, PlotterDetailList,
                             TemplateDetailList, UserDealerCreate,
                             UserUserCreate
                             )
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from constans import USER_CLASS
from api.permissions import IsAdministrator, IsDealer, IsUser


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
    serializer_class = UserListSerializer
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
    serializer_class = UserListSerializer
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
