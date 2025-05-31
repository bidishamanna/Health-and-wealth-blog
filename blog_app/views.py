from django.shortcuts import render

# Create your views here.
import os
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,parser_classes
from rest_framework import status
from .models import Blog
from category.models import Categories
from account.models import User

from .serializer import BlogSerializer
from django.db.models.query import QuerySet
from rest_framework.parsers import MultiPartParser,FormParser
import re
from django.conf import settings
@api_view(['POST'])

@parser_classes([MultiPartParser,FormParser])

def blog_post(request):
    if "image" not in request.FILES:

        return Response({'error': 'No image file provided.'}, status-status.HTTP_400_BAD_REQUEST)
    
    title = request.data.get('title')
    content = request.data.get('content')
    category_name = request.data.get('category')
    author_id = request.data.get('author')
    image_file = request.FILES['image']
    file_path = os.path.join(settings.MEDIA_ROOT, image_file.name)

   
    try:
        category = Categories.objects.get(name=category_name)

    except Categories.DoesNotExist:
        return Response({'Message': "Category not found"}, status=400)
    
    try :
        user = User.objects.get(id=author_id)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)


    

    with open(file_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    blog = Blog.objects.create(
        title=title,
        content=content,
        category=category,
        author = user,
        filename=image_file.name  
    )

    image_url = request.build_absolute_uri(settings.MEDIA_URL + 'blog_images/' + image_file.name)

    return Response({
        'message': 'Blog created successfully!',
        'blog': {
            'title': blog.title,
            'filename': blog.filename,
            'image_url': image_url,
            'created_at' : blog.created_at,
            'category_name' : category.name,
            'author_id' : author_id,
            'author_name' : user.name

        }
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_blogs(request):
    blog = Blog.objects.all().order_by('-created_at') #The - (minus sign) before a field in .order_by() tells Django to sort the results descendingly.
    serializer = BlogSerializer(blog, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def blog_get(request):
    if request.method == 'GET':
        blog: QuerySet = Blog.objects.all()
        if not blog.exists():
            return Response({'message': 'No blog found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data, status=200)
    
@api_view(['PATCH'])
def blog_patch(request, pk):
    try:
        # Fetch the customer instance based on the primary key (id)
        blog = BlogSerializer.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use partial=True to allow partial updates (only updating the 'name' field)
    serializer = BlogSerializer(blog, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def blog_put(request):
    pk = request.data.get('id')
    if not pk:
        return Response({'error': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

    # Deserialize the incoming data
    serializer = BlogSerializer(blog, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['DELETE'])
def blog_delete(request):
    pk = request.data.get('id')
    if not pk:
        return Response({'error': 'ID not provided'}, status=400)
    try:
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        return Response({'message': 'Customer deleted successfully'}, status=200)
    except Blog.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=400)
    





