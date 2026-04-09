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