from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response  # đúng cái này
from rest_framework import status
from rest_framework import viewsets
from rest_framework import viewsets
from .models import Brand, Storage, Screen, GPU, Laptop
from .serializers import BrandSerializer, StorageSerializer, ScreenSerializer, GPUSerializer, LaptopSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

class GPUViewSet(viewsets.ModelViewSet):
    queryset = GPU.objects.all()
    serializer_class = GPUSerializer

class LaptopViewSet(viewsets.ModelViewSet):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer

@api_view(['PUT'])
def update_laptop(request, pk):
    try:
        laptop = Laptop.objects.get(pk=pk)
    except Laptop.DoesNotExist:
        return Response({"error": "Laptop not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    laptop.quantity = quantity
    laptop.save()

    serializer = LaptopSerializer(laptop)
    return Response(serializer.data, status=status.HTTP_200_OK)
