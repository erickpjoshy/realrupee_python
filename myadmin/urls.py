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


    path('locality/',                 locality_list,   name='locality-list'),
    path('locality/create/',          locality_create, name='locality-create'),
    path('locality/update/<int:pk>/', locality_update, name='locality-update'),
    path('locality/delete/<int:pk>/', locality_delete, name='locality-delete'),


    path('property/',                       property_list,         name='property-list'),
    path('property/create/',                property_create,       name='property-create'),
    path('property/update/<int:pk>/',       property_update,       name='property-update'),
    path('property/delete/<int:pk>/',       property_delete,       name='property-delete'),
    path('property/image-delete/<int:pk>/', property_image_delete, name='property-image-delete'),


    path('dist-property/',                 dist_property_list,   name='dist-property-list'),
    path('dist-property/create/',          dist_property_create, name='dist-property-create'),
    path('dist-property/update/<int:pk>/', dist_property_update, name='dist-property-update'),
    path('dist-property/delete/<int:pk>/', dist_property_delete, name='dist-property-delete'),

    path('blog-content/',                 blog_content_list,   name='blog-content-list'),
    path('blog-content/create/',          blog_content_create, name='blog-content-create'),
    path('blog-content/update/<int:pk>/', blog_content_update, name='blog-content-update'),
    path('blog-content/delete/<int:pk>/', blog_content_delete, name='blog-content-delete'),

    path('testimonial/',                 testimonial_list,   name='testimonial-list'),
    path('testimonial/create/',          testimonial_create, name='testimonial-create'),
    path('testimonial/update/<int:pk>/', testimonial_update, name='testimonial-update'),
    path('testimonial/delete/<int:pk>/', testimonial_delete, name='testimonial-delete'),


    path('gallery/',                 gallery_list,   name='gallery-list'),
    path('gallery/create/',          gallery_create, name='gallery-create'),
    path('gallery/update/<int:pk>/', gallery_update, name='gallery-update'),
    path('gallery/delete/<int:pk>/', gallery_delete, name='gallery-delete'),


        


]