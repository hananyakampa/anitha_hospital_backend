# patients/serializers.py
from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    # We can show the username of the registering staff member.
    registered_by_username = serializers.ReadOnlyField(source='registered_by.username')

    class Meta:
        model = Patient
        fields = '__all__' # Include all fields from the model
        # These fields are set by the system, not by the API user.
        read_only_fields = ('uhid', 'registered_by')