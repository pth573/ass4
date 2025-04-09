from django.shortcuts import render
# Create your views here.

from rest_framework import viewsets
from.models import VIPCustomer
from.serializers import VIPCustomerSerializer

class VIPCustomerViewSet (viewsets. ModelViewSet):
    queryset = VIPCustomer.objects.all()
    serializer_class = VIPCustomerSerializer