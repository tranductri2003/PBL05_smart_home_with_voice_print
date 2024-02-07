from django.urls import path

from .views import (
    ApplianceListCreateView,
    ApplianceRetriveUpdateDeleteView,
)


app_name = 'appliances'

urlpatterns = [
    path('', ApplianceListCreateView.as_view(), name='appliance-list-create'),
    path('<str:appliance_id>/',ApplianceRetriveUpdateDeleteView.as_view(), name='appliance-retrive-update-delete'),
]