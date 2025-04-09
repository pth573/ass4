from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import RegularCustomer
from .serializers import RegularCustomerSerializer

class RegularCustomerViewSet (viewsets.ModelViewSet):
    queryset = RegularCustomer.objects.all()
    serializer_class = RegularCustomerSerializer