from django.db import router
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router=DefaultRouter()
router.register('movies',viewsets_movie)
router.register('guests',viewsets_guest)
router.register('reservation',viewsets_reservation)

urlpatterns = [

    path('home',no_rest_no_model,name='home'),

    path('from_model',no_rest_from_model,name='from_model'),

    path('FBV_List',FBV_List,name='FBV_List'),

    path('FBV_pk/<int:pk>',FBV_pk,name='FBV_pk'),

    path('CBV_List',CBV_List.as_view(),name='CBV_List'),

    path('CBV_List/<int:pk>',CVB_pk.as_view(),name='CBV_List'),

    path('mixins_list',mixins_list.as_view(),name='mixins_list'),

    path('mixins_list/<int:pk>',mixins_pk.as_view(),name='mixins_list'),

    path('generic_list',generic_list.as_view(),name='generic_list'),


    path('generic_list/<int:pk>',generic_pk.as_view(),name='generic_list'),


    path('viewsets_movie',include(router.urls)),
    path('viewsets_guest',include(router.urls)),
    path('viewsets_reservation',include(router.urls)),


    path('find_movie',find_movie,name='find_movie'),
    path('new_resv',new_resv,name='new_resv'),
    
    # token authentication  
    path('api_token_auth',obtain_auth_token),

]
