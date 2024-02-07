from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ActionSerializer
from .models import Action
from django_filters.rest_framework import DjangoFilterBackend
from helper.models import CustomPageNumberPagination
from rest_framework.response import Response    
from rest_framework import status

# Create your views here.


class ActionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActionSerializer
    queryset = Action.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action_id']
    ordering_fields = ['action_id']
    pagination_class = CustomPageNumberPagination
    
    
class ActionRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActionSerializer
    lookup_field = "action_id"

    def get_queryset(self):
        action_id = self.kwargs['action_id']
        return Action.objects.filter(action_id=action_id)
    
    def update(self, request, *args, **kwargs):
        action = self.get_object()
        serializer = self.get_serializer(action, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Information updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

