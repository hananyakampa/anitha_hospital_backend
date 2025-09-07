# patients/models.py
import uuid
from django.db import models
from django.conf import settings # To link to our custom User model

class Patient(models.Model):
    # Enum for Gender choices
    class GenderChoices(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    # --- Core Patient Information ---
    # Unique Health ID - The primary identifier for a patient in the hospital.
    # We will generate this automatically.
    uhid = models.CharField(max_length=10, unique=True, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)

    # --- Contact Information ---
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    address = models.TextField()

    # --- Emergency Contact ---
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=15)

    # --- Record Keeping ---
    # Links to the user (e.g., receptionist) who registered the patient.
    # on_delete=models.PROTECT prevents deleting a user if they have registered patients.
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='registered_patients'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.uhid})"

    def save(self, *args, **kwargs):
        # Generate a unique UHID on the first save.
        if not self.uhid:
            # Generate a 6-character hex string from a UUID and make it uppercase.
            # E.g., "A8C2E4"
            self.uhid = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)