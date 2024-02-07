from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ApplianceSerializer
from .models import Appliance
from django_filters.rest_framework import DjangoFilterBackend
from helper.models import CustomPageNumberPagination
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response    
from rest_framework import status

# Create your views here.


class ApplianceListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ApplianceSerializer
    queryset = Appliance.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['appliance_id']
    ordering_fields = ['appliance_id']
    pagination_class = CustomPageNumberPagination
    
    
class ApplianceRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ApplianceSerializer
    lookup_field = "appliance_id"

    def get_queryset(self):
        appliance_id = self.kwargs['appliance_id']
        return Appliance.objects.filter(appliance_id=appliance_id)
    
    def update(self, request, *args, **kwargs):
        appliance = self.get_object()
        serializer = self.get_serializer(appliance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Information updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

