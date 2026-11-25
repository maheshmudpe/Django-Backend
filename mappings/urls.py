
from django.urls import path

from .views import (
    MappingListCreateView,
    PatientMappingListView,
    MappingDeleteView,
)

urlpatterns = [
    path(
        "",
        MappingListCreateView.as_view(),
        name="mapping-list-create"
    ),
    path(
        "patients/<uuid:patient_id>/",
        PatientMappingListView.as_view(),
        name="patient-mappings"
    ),
    path(
        "<uuid:mapping_id>/",
        MappingDeleteView.as_view(),
        name="mapping-delete"
    ),
]
