# patients/views.py
from rest_framework import generics, permissions
from .models import Patient
from .serializers import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    """
    API View to list all patients or create a new one.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # Only authenticated (logged-in) users can access this endpoint.
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # When a new patient is created, automatically set the
        # 'registered_by' field to the current logged-in user.
        serializer.save(registered_by=self.request.user)

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update, or delete a single patient.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # Only authenticated users can access this as well.
    permission_classes = [permissions.IsAuthenticated]