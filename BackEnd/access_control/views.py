from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import PermissionSerializer
from .models import DevicePermission
from django_filters.rest_framework import DjangoFilterBackend
from helper.models import CustomPageNumberPagination
from rest_framework.response import Response    
from rest_framework import status

# Create your views here.


class PermissionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PermissionSerializer
    queryset = DevicePermission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['permission_id']
    ordering_fields = ['permission_id']
    pagination_class = CustomPageNumberPagination
    
    
class PermissionRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PermissionSerializer
    lookup_field = "permission_id"

    def get_queryset(self):
        permission_id = self.kwargs['permission_id']
        return DevicePermission.objects.filter(permission_id=permission_id)
    
    def update(self, request, *args, **kwargs):
        permission = self.get_object()
        serializer = self.get_serializer(permission, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Information updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

