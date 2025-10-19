from django.urls import path,re_path
from . import views
from  django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    path('admin-login/',views.AdminLoginAPIView.as_view(),name='api-admin-login'),
    path('home-api/',views.HomeAPIView.as_view(),name='api-home'),
    path('all-testimonials/',views.TestimonialAPIView.as_view(),name='api-all-testimonials'),
    path('property-list/',views.PropertyListAPIView.as_view(),name='api-property-list'),
    path('property-detail/<int:property_id>/',views.PropertyDetailAPIView.as_view(),name='api-property-detail'),
    path('contact-us-data/',views.ContactUspageListAPIView.as_view(),name='api-contact-us-data'),
    path('contact-create/', views.CreateContactUspageAPIView.as_view(), name='api-contact-create'),
    path('contact-delete/<int:contact_id>/', views.DeleteContactUspageAPIView.as_view(), name='api-contact-delete'),
    path('property-create/', views.CreatePropertyAPIView.as_view(), name='api-property-create'),
    path('property-update/<int:property_id>/', views.UpdatePropertyAPIView.as_view(), name='api-property-update'),
    path('property-delete/<int:property_id>/', views.DeletePropertyAPIView.as_view(), name='api-property-delete'),
    path('dist-property-create/', views.CreateDistPropertyAPIView.as_view(), name='dist-property-create'),
    path('dist-property-update/<int:property_id>/', views.UpdateDistPropertyAPIView.as_view(), name='dist-property-update'),
    path('dist-property-delete/<int:property_id>/', views.DeleteDistPropertyAPIView.as_view(), name='dist-property-delete'),


    path('create-blog/', views.CreateBlogAPIView.as_view(), name='api-create-blog'),
    path('blog-update/<int:blog_id>/', views.UpdateBlogAPIView.as_view(), name='api-blog-update'),
    path('blog-delete/<int:blog_id>/', views.DeleteBlogAPIView.as_view(), name='api-blog-delete'),


    path('create-state/', views.CreateStateAPIView.as_view(), name='api-create-state'),

    path('create-district/', views.CreateDistrictAPIView.as_view(), name='api-create-district'),

    path('create-locality/', views.CreateLocalityAPIView.as_view(), name='api-create-locality'),

    path('create-testimonial/', views.CreateTestimonialAPIView.as_view(), name='api-create-testimonial'),
    path('delete-testimonial/<int:testimonial_id>/', views.DeleteTestimonialAPIView.as_view(), name='api-delete-testimonial'),



    path('create-gallery-image/', views.CreateGalleryImageAPIView.as_view(), name='api-create-gallery-image'),
    path('delete-gallery-image/<int:image_id>/', views.DeleteGalleryImageAPIView.as_view(), name='api-delete-gallery-image'),


    path('property-filter/', views.PropertySearchAPIView.as_view(), name='api-property-filter'),



]