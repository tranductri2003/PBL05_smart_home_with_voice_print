from django.urls import path

from .views import (
    PermissionListCreateView,
    PermissionRetriveUpdateDeleteView,
)


app_name = 'permissions'

urlpatterns = [
    path('', PermissionListCreateView.as_view(), name='permission-list-create'),
    path('<str:permission_id>/',PermissionRetriveUpdateDeleteView.as_view(), name='permission-retrive-update-delete'),
]