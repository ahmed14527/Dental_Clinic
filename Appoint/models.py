from django.db import models
from accounts.models import User

class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.username} - {self.date} {self.time}"

class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.slot}"
    
    
    
class AppointmentRequest(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.preferred_date} {self.preferred_time} - {self.status}"