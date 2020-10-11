from django.urls import path
from api.views import (UserListView, UserRegisterView, UserUpdateView,
                       PlotterListView, PlotterAddView, PlotterUpdateView,
                       TemplateAddView, PlotterDeleteView, TemplateListView,
                       TemplateUpdateView, UserDealerCreateView,
                       UserDealerUpdateView, UserDealerListView,
                       UserUserCreateView, UserUserUpdateView,
                       UserUserListView, PlotterDealerList, api_root)

app_name = "api"


urlpatterns = [
    path('', api_root),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/registration/', UserRegisterView.as_view(),
         name='registration'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(),
         name='user_update'),
    path('user/dealer/list/', UserDealerListView.as_view(),
         name='user_dealer_list'),
    path('user/dealer/create/', UserDealerCreateView.as_view(),
         name='user_dealer_create'),
    path('user/dealer/update/<int:pk>/', UserDealerUpdateView.as_view(),
         name='user_dealer_update'),

    path('user/user/list/', UserUserListView.as_view(),
         name='user_user_list'),
    path('user/user/create/', UserUserCreateView.as_view(),
         name='user_user_create'),
    path('user/user/update/<int:pk>/', UserUserUpdateView.as_view(),
         name='user_user_update'),

    path('plotter/user/list/', PlotterDealerList.as_view(),
         name='plotter_user_list'),
    path('plotter/list/', PlotterListView.as_view(), name='plotter_list'),
    path('plotter/create/', PlotterAddView.as_view(), name='plotter_create'),
    path('plotter/update/<int:pk>/', PlotterUpdateView.as_view(),
         name='plotter_update'),
    path('plotter/delete/<int:pk>/', PlotterDeleteView.as_view(),
         name='plotter_delete'),

    path('template/list/', TemplateListView.as_view(), name='template_list'),
    path('template/create/', TemplateAddView.as_view(),
         name='template_create'),
    path('template/update/<int:pk>/', TemplateUpdateView.as_view(),
         name='template_update'),
]
