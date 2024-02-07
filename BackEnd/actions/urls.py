from django.urls import path

from .views import (
    ActionListCreateView,
    ActionRetriveUpdateDeleteView,
)


app_name = 'actions'

urlpatterns = [
    path('', ActionListCreateView.as_view(), name='action-list-create'),
    path('<str:action_id>/',ActionRetriveUpdateDeleteView.as_view(), name='action-retrive-update-delete'),
]