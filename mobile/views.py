from django.shortcuts import render

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response  # đúng cái này
from rest_framework import status
from rest_framework import viewsets
# Create your views here.
from rest_framework import viewsets
from mobile.models import Brand, Screen, Battery, Camera, Storage, Mobile
from mobile.serializers import (
    BrandMobileSerializer, ScreenSerializer, BatterySerializer,
    CameraSerializer, StorageSerializer, MobileSerializer
)

class BrandMobileViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandMobileSerializer

class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

class BatteryViewSet(viewsets.ModelViewSet):
    queryset = Battery.objects.all()
    serializer_class = BatterySerializer

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()  # Sửa lỗi thiếu dấu "="
    serializer_class = StorageSerializer

class MobileViewSet(viewsets.ModelViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer


@api_view(['PUT'])
def update_mobile(request, pk):
    try:
        mobile = Mobile.objects.get(pk=pk)
    except Mobile.DoesNotExist:
        return Response({"error": "Mobile not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    mobile.quantity = quantity
    mobile.save()

    serializer = MobileSerializer(mobile)
    return Response(serializer.data, status=status.HTTP_200_OK)
