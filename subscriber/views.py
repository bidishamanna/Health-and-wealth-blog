from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Subscriber
from .serializer import SubscriberSerializer
from django.db.models.query import QuerySet
import re

@api_view(['POST'])
def post_subscriber(request):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{1,}[a-zA-Z]{2,}$'

    email = request.data.get("email")

    if not re.fullmatch(email_regex, email):
        return Response({"Message" : "Please give correct email"}, status=400)

    if Subscriber.objects.filter(email=email).exists():
        return Response({"Message" : "Email is already exist"}, status=400)
    
    subscriber = Subscriber.objects.create(
        email = email
    )

    return Response({
        "Message" : "Subscribed Successfull !!",
        "Email" : subscriber.email
    })




@api_view(['GET'])
def get_subscriber(request):
    subscribers = Subscriber.objects.all().order_by('subscribeOn')

    if not subscribers.exists():

        return Response({
            "subscribers": "No subscriber found"
        }, status=400)
    
    subscriber_serializer = SubscriberSerializer(subscribers, many=True)
        
    return Response({
        "subscribers": subscriber_serializer.data
    }, status=200)

    
      
@api_view(['DELETE'])
def delete_subscriber(request):
    try:
        id = request.data.get("id")
        subscriber = get_object_or_404(Subscriber, id=id)
        subscriber.delete()
        return Response({"message":"Subscriber delete!!"})
    except Exception as e:
        return Response({ "error": "Something went wrong while deleting subscribers.",
            "details": str(e)
        })