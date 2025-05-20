from rest_framework import serializers
from .models import AppointmentSlot, Booking, AppointmentRequest

class AppointmentSlotSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = AppointmentSlot
        fields = ['id', 'doctor', 'doctor_name', 'date', 'time', 'is_booked']
        read_only_fields = ['is_booked']

class BookingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'patient', 'patient_name', 'slot', 'created_at']
        read_only_fields = ['created_at']

    def validate_slot(self, slot):
        if slot.is_booked:
            raise serializers.ValidationError("This slot is already booked.")
        return slot

    def create(self, validated_data):
        slot = validated_data['slot']
        slot.is_booked = True
        slot.save()
        return super().create(validated_data)

class AppointmentRequestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = AppointmentRequest
        fields = ['id', 'patient', 'patient_name', 'preferred_date', 'preferred_time', 'notes', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
