from django.urls import path

from .views import (
    UserListCreateView,
    UserRetriveUpdateDeleteView,
)


app_name = 'users'

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<str:user_name>/',UserRetriveUpdateDeleteView.as_view(), name='user-retrive-update-delete'),
]