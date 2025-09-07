# patients/urls.py
from django.urls import path
from .views import PatientListCreateView, PatientDetailView

urlpatterns = [
    # Maps to /api/patients/
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    # Maps to /api/patients/1/, /api/patients/2/, etc.
    path('<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
]