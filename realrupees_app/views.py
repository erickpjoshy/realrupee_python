import os
from django.shortcuts import get_object_or_404,redirect
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required




def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            auth_login(request, user)  # Use auth_login here
            return redirect('admin')  # Redirect to the admin page after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required(login_url='admin_login')
def admin(request):
    return render(request,'admin.html')


def logout(request):
	auth.logout(request)
	return redirect('home')    
    

def login(request):
    return render(request,'login.html')

def home(request):
    properties = Add_Property.objects.order_by('-id')[:6]
    blogs = Blog_Content.objects.all().order_by('-date')[:3]
    images = GalleryImage.objects.all()
    
    # Fetch unique values for dropdown options
    unique_property_types = Add_Property.objects.values_list('type', flat=True).distinct()
    unique_states = State_name.objects.all()
    unique_districts = District_name.objects.all()
    unique_localities = Locality.objects.all()
    unique_prices = Add_Property.objects.values_list('price', flat=True).distinct()

    context = {
        'blogs': blogs,
        'properties': properties,
        'unique_property_types': unique_property_types,
        'unique_states': unique_states,
        'unique_districts': unique_districts,
        'unique_localities': unique_localities,
        'unique_prices': unique_prices,
        'images':images
    }

    return render(request, 'home.html', context)



def about_us(request):
    return render(request,'about_us.html')

def test(request):
    testimonials = Testimonial.objects.all()
    return render(request,'testimonals.html',{'testimonials':testimonials})

def property(request):
    property_list = Add_Property.objects.all().order_by('-id')  # Order by latest entries first
    districts = District_name.objects.all()

    paginator = Paginator(property_list, 20)  # Show 20 properties per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'property.html', {'page_obj': page_obj, 'districts': districts})
    

def details_property(request, property_id):
    properties = Add_Property.objects.order_by('-id')[:6]
    property = get_object_or_404(Add_Property, id=property_id)
    return render(request, 'details_property.html', {'property': property,'properties':properties})

def blog_page(request):
    return render(request,'blog_page.html')

def blog_detail(request):
    return render(request,'blog_detail.html')


    

def contact_us(request):
    return render(request,'contact_us.html')

def contact(request):
    contact_details = Contact_Uspage.objects.all()
    reversed_order = reversed(list(contact_details))
    return render(request, 'admin_contactdetail.html', {'contact_details':reversed_order})


def contact_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        contact = Contact_Uspage.objects.create(
            name=name,
            email=email,
            phone_no=phone,
            message=message

        )
        contact.save()
        messages.info(request,'We will get you soon')
        return redirect('contact_us')

def delete_contacts(request, opening_id):
    content = get_object_or_404(Contact_Uspage, id=opening_id)
    content.delete()
    return redirect('contact')


def blog_content(request):
    return render(request,'blog_content.html')


def add_property(request):
    if request.method == 'POST':
        # Get form data
        heading = request.POST.get('heading')
        subheading = request.POST.get('subheading')
        property_id = request.POST.get('property_id')
        paragraph = request.POST.get('paragraph', 'none')
        youtube_url = request.POST.get('youtube_url', None)
        google_map_link = request.POST.get('google_map_link', None)
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        locality_id = request.POST.get('locality_id')
       
        price = request.POST.get('price')
        status = request.POST.get('status')  # Retrieve status
        type = request.POST.get('type')
        # Check if images are provided
        images = request.FILES.getlist('images')
        
        # Save the data to the database
        property = Add_Property.objects.create(
            heading=heading,
            subheading=subheading,
            property_id=property_id,
            paragraph=paragraph,
            youtube_url=youtube_url,
            google_map_link=google_map_link,
            
            price=price,
            status=status , # Save status
            type=type,
            state_id=state_id,  # Save state id
            district_id=district_id,  # Save district id
            locality_id=locality_id,  # Save locality id
        )
        
        # Save images to PropertyImage model and link them to the property
        for image in images:
            property_image = PropertyImage.objects.create(image=image)
            property.images.add(property_image)
        
        # Redirect or do other actions after saving
        return redirect('add_property')  # Replace 'success_page' with your actual success page URL

    add_property = Add_Property.objects.all()
    reversed_order = reversed(list(add_property))
    states = State_name.objects.all()
    districts = District_name.objects.all()
    localities = Locality.objects.all()
    return render(request, 'add_property.html',{'add_property':reversed_order,'states': states, 'districts': districts, 'localities': localities})

def delete_property(request, opening_id):
    content = get_object_or_404(Add_Property, id=opening_id)
    content.delete()
    return redirect('add_property')


def edit_property(request, content_id):
    content = get_object_or_404(Add_Property, id=content_id)
    states = State_name.objects.all()
    districts = District_name.objects.all()
    localities = Locality.objects.all()

    if request.method == 'POST':
        # Assuming your form sends data as a POST request
        heading = request.POST.get('heading')
        subheading = request.POST.get('subheading')
        property_id = request.POST.get('property_id')
        paragraph = request.POST.get('paragraph', 'none')
        youtube_url = request.POST.get('youtube_url', None)
        google_map_link = request.POST.get('google_map_link', None)
        
        price = request.POST.get('price')
        status = request.POST.get('status')
        property_type = request.POST.get('type')
        
        # Update the Add_Property instance with the new data
        content.heading = heading
        content.subheading = subheading
        content.property_id = property_id
        content.paragraph = paragraph
        content.youtube_url = youtube_url
        content.google_map_link = google_map_link
       
        content.price = price
        content.status = status
        content.type = property_type
        
        content.state_id = request.POST.get('state_id')
        content.district_id = request.POST.get('district_id')
        content.locality_id = request.POST.get('locality_id')
        
        # Save images to PropertyImage model and link them to the property
        old_images = list(content.images.all())
        new_images = request.FILES.getlist('images')
        if old_images and not new_images:
            # Keep the existing images
            content.images.set(old_images)
        elif new_images:
            # Update the images
            new_image_objects = [PropertyImage.objects.create(image=image) for image in new_images]
            content.images.set(new_image_objects)
        
        content.save()

        return redirect('add_property')  # Redirect to the Add Property view after editing

    return render(request, 'edit_property.html', {'content': content, 'states': states, 'districts': districts, 'localities': localities})




def add_dist_property(request):
    if request.method == 'POST':
        # Get form data
        heading = request.POST.get('heading')
        subheading = request.POST.get('subheading')
        property_id = request.POST.get('property_id')
        button_text = request.POST['button_text']
        button_url = request.POST['button_url']
        
        # Check if image is provided
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None  # Set image to None if not provided
        
        # Save the data to the database
        service_content = Add_Dist_Property.objects.create(
            heading=heading,
            subheading=subheading,
            property_id=property_id,
            image=image,
            button_text=button_text,
            button_url=button_url
        )
        # Redirect or do other actions after saving
        return redirect('add_dist_property')  # Replace 'success_page' with your actual success page URL

    add_dist_property = Add_Dist_Property.objects.all()
    return render(request, 'add_dist_property.html', {'add_dist_property': add_dist_property})

def delete_dist_property(request, opening_id):
    content = get_object_or_404(Add_Dist_Property, id=opening_id)
    content.delete()
    return redirect('add_dist_property')


def edit_dist_property(request, content_id):
    content = get_object_or_404(Add_Dist_Property, id=content_id)

    if request.method == 'POST':
        # Assuming your form sends data as a POST request
        image = request.FILES.get('image', content.image)
        heading = request.POST.get('heading',content.heading)
        subheading = request.POST.get('subheading',content.subheading)
        property_id = request.POST.get('property_id',content.property_id)
        button_text = request.POST.get('button_text',content.button_text)
        button_url = request.POST.get('button_url',content.button_url)
        
       

        # Update the SwiperContent instance with the new data
        content.image = image
        content.heading = heading
        content.subheading = subheading
        content.property_id = property_id
        content.button_text = button_text
        content.button_url = button_url
       
        
        content.save()

        return redirect('add_dist_property')  # Redirect to the Swiper view after editing

    return render(request, 'edit_dist_property.html', {'content': content})


# Create your views here.

def add_blog(request):
    if request.method == 'POST':
        # Get form data
        image = request.FILES['image']
        heading = request.POST.get('heading')
        paragraph = request.POST.get('paragraph')
        date = request.POST.get('date')
        
        # Save the data to the database
        blog_content = Blog_Content.objects.create(
            image=image,
            heading=heading,
            paragraph=paragraph,
            date=date
        )
        blog_content.save()
        
        return redirect('add_blog')  # Redirect to the blog list view after adding
    blogs = Blog_Content.objects.all()

    return render(request, 'add_blogs.html',{'blogs':blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog_Content, id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})

def blog(request):
    blogs = Blog_Content.objects.all()
    return render(request,'blogs.html',{'blogs':blogs})


def edit_blog(request, blog_id):
    content = get_object_or_404(Blog_Content, id=blog_id)

    if request.method == 'POST':
        # Assuming your form sends data as a POST request
        image = request.FILES.get('image', content.image)
        heading = request.POST.get('heading', content.heading)
        paragraph = request.POST.get('paragraph', content.paragraph)
        
        # Update the Blog_Content instance with the new data
        content.image = image
        content.heading = heading
        content.paragraph = paragraph
        
        
        content.save()

        return redirect('add_blog')  # Redirect to the blog list view after editing

    return render(request, 'edit_blog.html', {'content': content})


def delete_dist_blogs(request, opening_id):
    content = get_object_or_404(Blog_Content, id=opening_id)
    content.delete()
    return redirect('add_blog')


def add_state(request):
    if request.method == 'POST':
        # Get form data
        heading = request.POST.get('state')
        
        # Save the data to the database
        blog_content = State_name.objects.create(
            name=heading,
        )
        blog_content.save()
        
        return redirect('add_state')  # Redirect to the blog list view after adding
    state = State_name.objects.all()

    return render(request, 'add_state.html',{'state':state})


def add_district(request):
    if request.method == 'POST':
        # Get form data
        state_id = request.POST.get('state_id')  # Assuming you have a hidden input field for state id
        district_name = request.POST.get('district')
        
        # Save the data to the database
        state = State_name.objects.get(id=state_id)
        district = District_name.objects.create(name=district_name, state=state)
        district.save()
        
        return redirect('add_district')  # Redirect after adding

    states = State_name.objects.all()
    return render(request, 'add_district.html', {'states': states})


def add_locality(request):
    if request.method == 'POST':
        # Get form data
        state_id = request.POST.get('state_id')
        district_id = request.POST.get('district_id')
        locality_name = request.POST.get('locality')
        
        # Save the data to the database
        state = State_name.objects.get(id=state_id)
        district = District_name.objects.get(id=district_id)
        locality = Locality.objects.create(name=locality_name, state=state, district=district)
        locality.save()
        
        return redirect('add_locality')  # Redirect after adding

    states = State_name.objects.all()
    districts = District_name.objects.all()  # You might also want to pass districts to the template
    return render(request, 'add_locality.html', {'states': states, 'districts': districts})


def district_page(request, district_id):
    district = get_object_or_404(District_name, id=district_id)
    properties_list = Add_Property.objects.filter(district=district).order_by('-id')  # Assuming ordering by ID
    
    # Setup pagination
    paginator = Paginator(properties_list, 20)  # Show 20 properties per page
    page = request.GET.get('page')
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        properties = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        properties = paginator.page(paginator.num_pages)

    return render(request, 'district_page.html', {'district': district, 'properties': properties})



def property_search(request):
    property_type = request.GET.get('property_type')
    state_id = request.GET.get('state')
    district_id = request.GET.get('district')
    locality_id = request.GET.get('locality')
    price = request.GET.get('price')

    properties = Add_Property.objects.all()

    if property_type:
        properties = properties.filter(type=property_type)
    if state_id:
        properties = properties.filter(locality__state_id=state_id)
    if district_id:
        properties = properties.filter(locality__district_id=district_id)
    if locality_id:
        properties = properties.filter(locality_id=locality_id)
    if price:
        properties = properties.filter(price=price)

    context = {
        'properties': properties,
    }
    
    return render(request, 'property_search_results.html', context)


def property_id_search(request):
    property_id = request.GET.get('property_id')
    
    if property_id:
        properties = Add_Property.objects.filter(property_id=property_id)
    else:
        properties = Add_Property.objects.none()

    context = {
        'properties': properties,
    }
    
    return render(request, 'property_search_results.html', context)



def add_testimonials(request):
    if request.method == 'POST':
        name = request.POST.get('name')
       
        review = request.POST.get('review')
       

        testimonial = Testimonial(name=name, review=review, )
        testimonial.save()
        return redirect('add_testimonials')  # Redirect to the same page after saving the testimonial

    testimonials = Testimonial.objects.all()
    return render(request, 'add_testimonials.html', {'testimonials': testimonials})



def delete_testimonials(request, opening_id):
    content = get_object_or_404(Testimonial, id=opening_id)
    content.delete()
    return redirect('add_testimonials')
    
    
def add_images(request):
    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        media_type = request.POST.get('type')   # keep type but do not restrict

        image = request.FILES.get('image')
        video = request.FILES.get('video')

        # Create object (do not remove one based on type)
        GalleryImage.objects.create(
            title=title,
            description=description,
            type=media_type,   # still stored for display
            image=image,       # save image if uploaded
            video=video,       # save video if uploaded
        )

        return redirect('add_images')

    add_images = GalleryImage.objects.all()
    return render(request, 'add_awiper_img.html', {'add_images': add_images})


def delete_gallery_image(request, opening_id):
    content = get_object_or_404(GalleryImage, id=opening_id)
    content.delete()
    return redirect('add_images')

def edit_gallery_image(request, opening_id):
    image_obj = GalleryImage.objects.get(id=opening_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        media_type = request.POST.get('type')  # Still stored but no restriction

        new_image = request.FILES.get('image')
        new_video = request.FILES.get('video')

        # Update basic fields
        image_obj.title = title
        image_obj.description = description
        image_obj.type = media_type

        # Save image if uploaded
        if new_image:
            image_obj.image = new_image

        # Save video if uploaded
        if new_video:
            image_obj.video = new_video

        image_obj.save()
        return redirect('add_images')

    return render(request, 'edit_gallery_image.html', {'image_obj': image_obj})