from myadmin.views import *
from django.urls import path



urlpatterns = [

    path('', login, name='panel-login'),
    path('logout/', logout, name='panel-logout'),
    path('superadmin-dashboard/', index, name='superadmin-dashboard'),

    path('contact-us/',                  contact_us_list,   name='contact-us-list'),
    path('contact-us/create/',           contact_us_create, name='contact-us-create'),
    path('contact-us/update/<int:pk>/',  contact_us_update, name='contact-us-update'),
    path('contact-us/delete/<int:pk>/',  contact_us_delete, name='contact-us-delete'),


    path('state-name/',                 state_name_list,   name='state-name-list'),
    path('state-name/create/',          state_name_create, name='state-name-create'),
    path('state-name/update/<int:pk>/', state_name_update, name='state-name-update'),
    path('state-name/delete/<int:pk>/', state_name_delete, name='state-name-delete'),


    path('district-name/',                 district_name_list,   name='district-name-list'),
    path('district-name/create/',          district_name_create, name='district-name-create'),
    path('district-name/update/<int:pk>/', district_name_update, name='district-name-update'),
    path('district-name/delete/<int:pk>/', district_name_delete, name='district-name-delete'),
        


]