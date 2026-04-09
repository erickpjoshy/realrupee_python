from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.shortcuts import render,redirect
from django.contrib import messages
from myadmin.models import *
from myadmin.forms import *
from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import os
import subprocess
# percentage and amount  coupon
import csv
from django.http import HttpResponse
import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.utils import timezone  
import datetime
from dateutil.relativedelta import relativedelta
import requests
from realrupees_app.models import *



captcha_secret_key = '6LdMIXIsAAAAAFU5VuIN8ALXIb9RY8dBlBOlLX7s'

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")   # ✅ changed
        password = request.POST.get("password")
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify reCAPTCHA
        data = {
            'secret': captcha_secret_key,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        test_result = True  # keep True for testing
        new_result = result.get('success')

        if test_result:  # or use: if new_result:
            
            user = auth.authenticate(
                request,
                username=username,   
                password=password
            )

            if user is not None:
                auth.login(request, user)

                # ✅ optional session store
                request.session["username"] = username

                if user.is_superuser:
                    return redirect("superadmin-dashboard")

                return redirect("/")  # or your dashboard

            messages.error(request, "Invalid username or password")
            return redirect("panel-login")

        else:
            messages.error(request, "Invalid Captcha. Please try again.")
            return redirect("panel-login")

    return render(request, "admin-login.html")


def logout(request):
    auth.logout(request)
    return redirect('panel-login')


def index(request):
    context = {

    }
    return render(request, 'superadmin-dashboard.html',context)




################################### Contact Us #############################

def contact_us_list(request):
    page = 'Contact Us'
    contacts = Contact_Uspage.objects.all().order_by('-id')
    return render(request, 'admin-list.html', {'contacts': contacts, 'page': page})


def contact_us_create(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            new = form.save()
            return redirect('contact-us-list')
        else:
            print('form errors:', form.errors)
    else:
        form = ContactUsForm()

    return render(request, 'contact-us-form.html', {'form': form})


def contact_us_update(request, pk):
    contact = get_object_or_404(Contact_Uspage, pk=pk)
    if request.method == "POST":
        form = ContactUsForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact-us-list')
        else:
            print('form errors:', form.errors)
    else:
        form = ContactUsForm(instance=contact)

    return render(request, 'contact-us-form.html', {'form': form, 'contact': contact})


def contact_us_delete(request, pk):
    contact = get_object_or_404(Contact_Uspage, pk=pk)
    contact.delete()
    return redirect('contact-us-list')








def state_name_list(request):
    page = 'State Name'
    states = State_name.objects.all().order_by('name')
    return render(request, 'admin-list.html', {'states': states, 'page': page})


def state_name_create(request):
    if request.method == "POST":
        form = StateNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('state-name-list')
        else:
            print('form errors:', form.errors)
    else:
        form = StateNameForm()

    return render(request, 'state-name-form.html', {'form': form})


def state_name_update(request, pk):
    state = get_object_or_404(State_name, pk=pk)
    if request.method == "POST":
        form = StateNameForm(request.POST, instance=state)
        if form.is_valid():
            form.save()
            return redirect('state-name-list')
        else:
            print('form errors:', form.errors)
    else:
        form = StateNameForm(instance=state)

    return render(request, 'state-name-form.html', {'form': form, 'state': state})


def state_name_delete(request, pk):
    state = get_object_or_404(State_name, pk=pk)
    state.delete()
    return redirect('state-name-list')




############################## Districts #############################################################


def district_name_list(request):
    page = 'District Name'
    districts = District_name.objects.all().order_by('state__name', 'name')
    return render(request, 'admin-list.html', {'districts': districts, 'page': page})


def district_name_create(request):
    if request.method == "POST":
        form = DistrictNameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('district-name-list')
        else:
            print('form errors:', form.errors)
    else:
        form = DistrictNameForm()

    return render(request, 'district-name-form.html', {'form': form})


def district_name_update(request, pk):
    district = get_object_or_404(District_name, pk=pk)
    if request.method == "POST":
        form = DistrictNameForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            return redirect('district-name-list')
        else:
            print('form errors:', form.errors)
    else:
        form = DistrictNameForm(instance=district)

    return render(request, 'district-name-form.html', {'form': form, 'district': district})


def district_name_delete(request, pk):
    district = get_object_or_404(District_name, pk=pk)
    district.delete()
    return redirect('district-name-list')



############################ Localty ########################


def locality_list(request):
    page = 'Locality'
    localities = Locality.objects.all().order_by('state__name', 'district__name', 'name')
    return render(request, 'myadmin/admin-list.html', {'localities': localities, 'page': page})


def locality_create(request):
    if request.method == "POST":
        form = LocalityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('locality-list')
        else:
            print('form errors:', form.errors)
    else:
        form = LocalityForm()

    return render(request, 'myadmin/locality-form.html', {'form': form})


def locality_update(request, pk):
    locality = get_object_or_404(Locality, pk=pk)
    if request.method == "POST":
        form = LocalityForm(request.POST, instance=locality)
        if form.is_valid():
            form.save()
            return redirect('locality-list')
        else:
            print('form errors:', form.errors)
    else:
        form = LocalityForm(instance=locality)

    return render(request, 'myadmin/locality-form.html', {'form': form, 'locality': locality})


def locality_delete(request, pk):
    locality = get_object_or_404(Locality, pk=pk)
    locality.delete()
    return redirect('locality-list')