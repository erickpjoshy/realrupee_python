from django.db import models
from django.contrib.auth.models import User

class Contact_Uspage(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=255)
    message = models.TextField()


class State_name(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class District_name(models.Model):
    state = models.ForeignKey(State_name, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Locality(models.Model):
    state = models.ForeignKey(State_name, on_delete=models.CASCADE)
    district = models.ForeignKey(District_name, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Add_Property(models.Model):
    STATUS_CHOICES = (
        ('For Sale', 'For Sale'),
        ('Sold', 'Sold'),
    )
    
    heading = models.CharField(max_length=100)
    subheading = models.TextField()
    property_id = models.CharField(max_length=255)
    
    state = models.ForeignKey(State_name, on_delete=models.CASCADE, default=1)  # Provide default value
    district = models.ForeignKey(District_name, on_delete=models.CASCADE, default=1)  # Provide default value
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, default=1)
    paragraph = models.TextField(default='none')
    youtube_url = models.URLField(max_length=200, null=True, blank=True)
    google_map_link = models.URLField(max_length=200, null=True, blank=True)
    images = models.ManyToManyField('PropertyImage', related_name='properties')
    price = models.CharField(max_length=255, default='None')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='For Sale')
    type  = models.CharField(max_length=255,default='None')
    
    def __str__(self):
        return self.heading

class PropertyImage(models.Model):
    image = models.ImageField(upload_to='mamamia_images/')
    
    def __str__(self):
        return self.image.name


class Add_Dist_Property(models.Model):
    image = models.ImageField(upload_to='mamamia_images/')
    heading = models.CharField(max_length=100)
    subheading = models.TextField()
    property_id = models.CharField(max_length=255)
    button_text = models.CharField(max_length=255, blank=True, default='Default Button Text')
    button_url = models.URLField(blank=True, default='https://example.com')
    def __str__(self):
        return self.heading


class Blog_Content(models.Model):
    image = models.ImageField(upload_to='mamamia_images/')
    heading = models.CharField(max_length=100)
    paragraph = models.TextField()
    date = models.DateField(max_length=255)
    
    def __str__(self):
        return self.heading


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    
    
    review = models.TextField()

    def __str__(self):
        return self.name


# Create your models here.



class GalleryImage(models.Model):

    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    image = models.ImageField(
        upload_to='swiper_images/',
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to='swiper_videos/',
        blank=True,
        null=True
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='image'
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title or "Gallery Item"


