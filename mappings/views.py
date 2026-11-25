
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Mapping
from .serializers import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mapping.objects.filter(
            patient__created_by=self.request.user
        )

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]

        if patient.created_by != self.request.user:
            raise PermissionDenied(
                "You can only assign doctors to your own patients."
            )

        serializer.save()


class PatientMappingListView(generics.ListAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Mapping.objects.filter(
            patient_id=self.kwargs["patient_id"],
            patient__created_by=self.request.user
        )


class MappingDeleteView(generics.DestroyAPIView):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "mapping_id"

    def get_queryset(self):
        return Mapping.objects.filter(
            patient__created_by=self.request.user
        )
