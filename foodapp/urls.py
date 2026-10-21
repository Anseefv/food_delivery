from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


boyprofile_list = BoyProfileViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

boyprofile_detail = BoyProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

partnerprofile_list = PartnerProfileViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

partnerprofile_detail = PartnerProfileViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    
# login and registractions
    path('register/',CustomerRegister.as_view()),
    path('login/',obtain_auth_token),
    path('login/addboy/',DeliveryBoyRegister.as_view()),
    path('login/resturent_partner/',ResturentPartnerRegister.as_view()),
    path('login/boyprofile/', boyprofile_list, name='boyprofile-list'),
    path('login/boyprofile/<int:pk>/', boyprofile_detail, name='boyprofile-detail'),
    path('login/partnerprofile/', partnerprofile_list, name='partnerprofile-list'),
    path('login/partnerprofile/<int:pk>/', partnerprofile_detail, name='partnerprofile-detail'),

    
    
]
