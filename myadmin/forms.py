from django import forms
from realrupees_app.models import *

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact_Uspage
        fields = ['name', 'email', 'phone_no', 'message']
        widgets = {
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
            'email':    forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'message':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }



class StateNameForm(forms.ModelForm):
    class Meta:
        model = State_name
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DistrictNameForm(forms.ModelForm):
    class Meta:
        model = District_name
        fields = ['state', 'name']
        widgets = {
            'state': forms.Select(attrs={'class': 'form-control'}),
            'name':  forms.TextInput(attrs={'class': 'form-control'}),
        }


class LocalityForm(forms.ModelForm):
    class Meta:
        model = Locality
        fields = ['state', 'district', 'name']
        widgets = {
            'state':    forms.Select(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'name':     forms.TextInput(attrs={'class': 'form-control'}),
        }



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Add_Property
        fields = ['heading', 'subheading', 'property_id', 'state', 'district', 
                  'locality', 'paragraph', 'youtube_url', 'google_map_link', 
                  'price', 'status', 'type']
        widgets = {
            'heading':         forms.TextInput(attrs={'class': 'form-control'}),
            'subheading':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'property_id':     forms.TextInput(attrs={'class': 'form-control'}),
            'state':           forms.Select(attrs={'class': 'form-control'}),
            'district':        forms.Select(attrs={'class': 'form-control'}),
            'locality':        forms.Select(attrs={'class': 'form-control'}),
            'paragraph':       forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'youtube_url':     forms.URLInput(attrs={'class': 'form-control'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control'}),
            'price':           forms.TextInput(attrs={'class': 'form-control'}),
            'status':          forms.Select(attrs={'class': 'form-control'}),
            'type':            forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }



class AddDistPropertyForm(forms.ModelForm):
    class Meta:
        model = Add_Dist_Property
        fields = ['image', 'heading', 'subheading', 'property_id', 'button_text', 'button_url']
        widgets = {
            'image':       forms.FileInput(attrs={'class': 'form-control'}),
            'heading':     forms.TextInput(attrs={'class': 'form-control'}),
            'subheading':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'property_id': forms.TextInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url':  forms.URLInput(attrs={'class': 'form-control'}),
        }



class BlogContentForm(forms.ModelForm):
    class Meta:
        model = Blog_Content
        fields = ['image', 'heading', 'paragraph', 'date']
        widgets = {
            'image':     forms.FileInput(attrs={'class': 'form-control'}),
            'heading':   forms.TextInput(attrs={'class': 'form-control'}),
            'paragraph': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'date':      forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'review']
        widgets = {
            'name':   forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['type', 'title', 'description', 'image', 'video']
        widgets = {
            'type':        forms.Select(attrs={'class': 'form-control'}),
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image':       forms.FileInput(attrs={'class': 'form-control'}),
            'video':       forms.FileInput(attrs={'class': 'form-control'}),
        }