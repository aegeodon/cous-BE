from django.shortcuts import render

import os
import base64
import json

import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from coususers.models import CousUser
from courses.models import Course
from places.models import Place
from tags.models import Tag
from coususers.serializers import KakaoLoginRequestSerializer, CousUserPatchSerializer, CousUserResponseSerializer
from .serializers import CourseSerializer, CourseResponseSerializer, CoursePostSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course_post(request):
    serializer = CoursePostSerializer(data=request.data)
    if serializer.is_valid():
        inputData = serializer.validated_data

        course = Course(
            description=inputData['description'],
            content=inputData['content'],
            area=inputData['area'],
            cousUser=request.user
        )
        course.save()

        for p in inputData['places']:
            Place(course=course, address=p['address']).save()
        for t in inputData['tags']:
            Tag(course=course, tagName=t['tagName']).save()

        resSerializer = CourseResponseSerializer(course)
        return Response(resSerializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def course_access_one(request, pk):
    course = Course.objects.get(pk=pk)
    
    serializer = CourseResponseSerializer(course)
    return Response(serializer.data)