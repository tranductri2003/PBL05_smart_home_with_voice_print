from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserSerializer
from .models import NewUser
from django_filters.rest_framework import DjangoFilterBackend
from helper.models import CustomPageNumberPagination
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response    
from rest_framework import status

# Create your views here.


class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = NewUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_name']
    ordering_fields = ['user_name']
    pagination_class = CustomPageNumberPagination
    
    
class UserRetriveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    lookup_field = "user_name"

    def get_queryset(self):
        user_name = self.kwargs['user_name']
        return NewUser.objects.filter(user_name=user_name)
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if new_password and old_password: 
                if not check_password(old_password, user.password):  # Sửa thành not để kiểm tra khi mật khẩu khớp
                    return Response({'error': 'Invalid old password.'}, status=status.HTTP_400_BAD_REQUEST)    
                else:
                    user.set_password(new_password)
                    user.save()

            return Response({'message': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

