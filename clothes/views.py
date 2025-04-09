from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response  # đúng cái này
from rest_framework import status
# Create your views here.
from rest_framework import viewsets
from clothes.models import Brand, Size, Material, Color, Clothes
from clothes.serializers import BrandSerializer, SizeSerializer, MaterialSerializer, ColorSerializer, ClothesSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer


@api_view(['PUT'])
def update_clothes(request, pk):
    try:
        clothes = Clothes.objects.get(pk=pk)
    except Clothes.DoesNotExist:
        return Response({"error": "Clothes not found"}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get("quantity")
    if quantity is None:
        return Response({"error": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

    clothes.quantity = quantity
    clothes.save()

    serializer = ClothesSerializer(clothes)
    return Response(serializer.data, status=status.HTTP_200_OK)
