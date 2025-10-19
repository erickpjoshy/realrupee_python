from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from realrupees_app.models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class AdminLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_staff:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'is_staff': user.is_staff,
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        

class HomeAPIView(APIView):
    def get(self, request):
        properties = Add_Property.objects.order_by('-id')[:6]
        blogs = Blog_Content.objects.all().order_by('-date')[:3]
        images = GalleryImage.objects.all()
        
        # Dropdown values
        unique_property_types = list(
            Add_Property.objects.values_list('type', flat=True).distinct()
        )
        unique_prices = list(
            Add_Property.objects.values_list('price', flat=True).distinct()
        )
        states = State_name.objects.all()
        districts = District_name.objects.all()
        localities = Locality.objects.all()

        data = {
            "properties": AddPropertySerializer(properties, many=True, context={'request':request}).data,
            "blogs": BlogContentSerializer(blogs, many=True, context={'request':request}).data,
            "unique_property_types": unique_property_types,
            "unique_states": StateSerializer(states, many=True, context={'request':request}).data,
            "unique_districts": DistrictSerializer(districts, many=True, context={'request':request}).data,
            "unique_localities": LocalitySerializer(localities, many=True, context={'request':request}).data,
            "unique_prices": unique_prices,
            "images": GalleryImageSerializer(images, many=True, context={'request':request}).data,
        }

        return Response(data)


class TestimonialAPIView(APIView):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        serializer = TestimonialSerializer(testimonials, many=True, context={'request': request})
        return Response(serializer.data)
    


class PropertyListPagination(PageNumberPagination):
    page_size = 20  # default
    page_size_query_param = 'page_size'  # allows ?page_size=10 override
    max_page_size = 100


class PropertyListAPIView(APIView):
    def get(self, request):
        properties = Add_Property.objects.all().order_by('-id')
        districts = District_name.objects.all()

        paginator = PropertyListPagination()
        result_page = paginator.paginate_queryset(properties, request)

        property_serializer = AddPropertySerializer(result_page, many=True, context={'request': request})
        district_serializer = DistrictSerializer(districts, many=True, context={'request': request})

        return paginator.get_paginated_response({
            'properties': property_serializer.data,
            'districts': district_serializer.data
        })



class PropertyDetailAPIView(APIView):
    def get(self, request, property_id):
        try:
            property_instance = Add_Property.objects.get(property_id=property_id)
        except Add_Property.DoesNotExist:
            return Response(
                {"error": "Property not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AddPropertySerializer(property_instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class ContactUspageListAPIView(APIView):
    def get(self, request):
        contacts = Contact_Uspage.objects.all().order_by('-id')
        serializer = ContactUspageSerializer(contacts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CreateContactUspageAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        message = request.data.get('message')

        # Basic validation
        if not all([name, email, phone, message]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        contact = Contact_Uspage.objects.create(
            name=name,
            email=email,
            phone_no=phone,
            message=message
        )

        return Response(
            {'success': True, 'message': 'Contact created successfully.', 'id': contact.id},
            status=status.HTTP_201_CREATED
        )


# 2️⃣ Delete Contact API
class DeleteContactUspageAPIView(APIView):
    def delete(self, request, contact_id):
        contact = get_object_or_404(Contact_Uspage, id=contact_id)
        contact.delete()
        return Response({'success': True, 'message': 'Contact deleted successfully.'}, status=status.HTTP_200_OK)



class CreatePropertyAPIView(APIView):
    def post(self, request):
        try:
            data = request.data

            # Create Add_Property object
            property_obj = Add_Property.objects.create(
                heading=data.get('heading'),
                subheading=data.get('subheading'),
                property_id=data.get('property_id'),
                paragraph=data.get('paragraph', 'none'),
                youtube_url=data.get('youtube_url'),
                google_map_link=data.get('google_map_link'),
                price=data.get('price'),
                status=data.get('status'),
                type=data.get('type'),
                state_id=data.get('state_id'),
                district_id=data.get('district_id'),
                locality_id=data.get('locality_id'),
            )

            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                prop_img = PropertyImage.objects.create(image=image)
                property_obj.images.add(prop_img)

            return Response(
                {"success": True, "message": "Property created successfully", "id": property_obj.id},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 2️⃣ Update Property
# -------------------------
class UpdatePropertyAPIView(APIView):
    def put(self, request, property_id):
        try:
            property_obj = get_object_or_404(Add_Property, id=property_id)
            data = request.data

            # Update fields
            property_obj.heading = data.get('heading', property_obj.heading)
            property_obj.subheading = data.get('subheading', property_obj.subheading)
            property_obj.property_id = data.get('property_id', property_obj.property_id)
            property_obj.paragraph = data.get('paragraph', property_obj.paragraph)
            property_obj.youtube_url = data.get('youtube_url', property_obj.youtube_url)
            property_obj.google_map_link = data.get('google_map_link', property_obj.google_map_link)
            property_obj.price = data.get('price', property_obj.price)
            property_obj.status = data.get('status', property_obj.status)
            property_obj.type = data.get('type', property_obj.type)
            property_obj.state_id = data.get('state_id', property_obj.state_id)
            property_obj.district_id = data.get('district_id', property_obj.district_id)
            property_obj.locality_id = data.get('locality_id', property_obj.locality_id)

            # Update or retain images
            new_images = request.FILES.getlist('images')
            if new_images:
                new_image_objs = [PropertyImage.objects.create(image=img) for img in new_images]
                property_obj.images.set(new_image_objs)

            property_obj.save()

            return Response(
                {"success": True, "message": "Property updated successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 3️⃣ Delete Property
# -------------------------
class DeletePropertyAPIView(APIView):
    def delete(self, request, property_id):
        property_obj = get_object_or_404(Add_Property, id=property_id)
        property_obj.delete()
        return Response({"success": True, "message": "Property deleted successfully"}, status=status.HTTP_200_OK)







class CreateDistPropertyAPIView(APIView):
    def post(self, request):
        try:
            heading = request.data.get('heading')
            subheading = request.data.get('subheading')
            property_id = request.data.get('property_id')
            button_text = request.data.get('button_text', 'Default Button Text')
            button_url = request.data.get('button_url', 'https://example.com')
            image = request.FILES.get('image', None)

            dist_property = Add_Dist_Property.objects.create(
                heading=heading,
                subheading=subheading,
                property_id=property_id,
                button_text=button_text,
                button_url=button_url,
                image=image
            )

            return Response({
                "success": True,
                "message": "Dist property created successfully",
                "id": dist_property.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 2️⃣ Update Dist Property
# -------------------------
class UpdateDistPropertyAPIView(APIView):
    def put(self, request, property_id):
        try:
            dist_property = get_object_or_404(Add_Dist_Property, id=property_id)

            dist_property.heading = request.data.get('heading', dist_property.heading)
            dist_property.subheading = request.data.get('subheading', dist_property.subheading)
            dist_property.property_id = request.data.get('property_id', dist_property.property_id)
            dist_property.button_text = request.data.get('button_text', dist_property.button_text)
            dist_property.button_url = request.data.get('button_url', dist_property.button_url)

            # Update image if provided, otherwise keep existing
            if 'image' in request.FILES:
                dist_property.image = request.FILES['image']

            dist_property.save()

            return Response({"success": True, "message": "Dist property updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# 3️⃣ Delete Dist Property
# -------------------------
class DeleteDistPropertyAPIView(APIView):
    def delete(self, request, property_id):
        dist_property = get_object_or_404(Add_Dist_Property, id=property_id)
        dist_property.delete()
        return Response({"success": True, "message": "Dist property deleted successfully"}, status=status.HTTP_200_OK)
    




class CreateBlogAPIView(APIView):
    def post(self, request):
        try:
            image = request.FILES.get('image')
            heading = request.data.get('heading')
            paragraph = request.data.get('paragraph')
            date = request.data.get('date')

            blog = Blog_Content.objects.create(
                image=image,
                heading=heading,
                paragraph=paragraph,
                date=date
            )

            return Response({"success": True, "message": "Blog created", "id": blog.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Update Blog
class UpdateBlogAPIView(APIView):
    def put(self, request, blog_id):
        blog = get_object_or_404(Blog_Content, id=blog_id)
        blog.image = request.FILES.get('image', blog.image)
        blog.heading = request.data.get('heading', blog.heading)
        blog.paragraph = request.data.get('paragraph', blog.paragraph)
        blog.save()
        return Response({"success": True, "message": "Blog updated"}, status=status.HTTP_200_OK)

# Delete Blog
class DeleteBlogAPIView(APIView):
    def delete(self, request, blog_id):
        blog = get_object_or_404(Blog_Content, id=blog_id)
        blog.delete()
        return Response({"success": True, "message": "Blog deleted"}, status=status.HTTP_200_OK)






class CreateStateAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        state = State_name.objects.create(name=name)
        return Response({"success": True, "id": state.id, "name": state.name}, status=status.HTTP_201_CREATED)



class CreateDistrictAPIView(APIView):
    def post(self, request):
        state_id = request.data.get('state_id')
        name = request.data.get('name')
        district = District_name.objects.create(name=name, state_id=state_id)
        return Response({"success": True, "id": district.id, "name": district.name}, status=status.HTTP_201_CREATED)
    


class CreateLocalityAPIView(APIView):
    def post(self, request):
        state_id = request.data.get('state_id')
        district_id = request.data.get('district_id')
        name = request.data.get('name')
        locality = Locality.objects.create(name=name, state_id=state_id, district_id=district_id)
        return Response({"success": True, "id": locality.id, "name": locality.name}, status=status.HTTP_201_CREATED)




class CreateTestimonialAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        review = request.data.get('review')
        testimonial = Testimonial.objects.create(name=name, review=review)
        return Response({"success": True, "id": testimonial.id}, status=status.HTTP_201_CREATED)

class DeleteTestimonialAPIView(APIView):
    def delete(self, request, testimonial_id):
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        testimonial.delete()
        return Response({"success": True, "message": "Deleted"}, status=status.HTTP_200_OK)
    




class CreateGalleryImageAPIView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        gallery_image = GalleryImage.objects.create(image=image)
        return Response({"success": True, "id": gallery_image.id}, status=status.HTTP_201_CREATED)

class DeleteGalleryImageAPIView(APIView):
    def delete(self, request, image_id):
        gallery_image = get_object_or_404(GalleryImage, id=image_id)
        gallery_image.delete()
        return Response({"success": True, "message": "Deleted"}, status=status.HTTP_200_OK)





class PropertySearchAPIView(APIView):
    def get(self, request):
        # Accept all params via query_params
        property_type = request.query_params.get('property_type')
        state_id = request.query_params.get('state_id')
        district_id = request.query_params.get('district_id')
        locality_id = request.query_params.get('locality_id')
        price = request.query_params.get('price')
        status = request.query_params.get('status')
        heading = request.query_params.get('heading')
        property_id = request.query_params.get('property_id')

        # Start with all properties
        properties = Add_Property.objects.all()

        # Apply filters
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
        if status:
            properties = properties.filter(status=status)
        if heading:
            properties = properties.filter(heading__icontains=heading)
        if property_id:
            properties = properties.filter(property_id__icontains=property_id)

        # Build response
        data = []
        for p in properties:
            images = [img.image.url for img in p.images.all()]
            data.append({
                "id": p.id,
                "heading": p.heading,
                "property_id": p.property_id,
                "type": p.type,
                "price": p.price,
                "status": p.status,
                "state_id": p.state_id,
                "district_id": p.district_id,
                "locality_id": p.locality_id,
                "images": images,
            })

        return Response({"properties": data})
