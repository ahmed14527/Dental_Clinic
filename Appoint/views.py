from rest_framework import viewsets, throttling, status
from rest_framework.response import Response
from .models import AppointmentSlot, Booking, AppointmentRequest
from .serializers import AppointmentSlotSerializer, BookingSerializer, AppointmentRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import AppointmentRequest
from firebase_notify.models import DeviceToken
from firebase_notify.utils.firebase_notify import send_firebase_notification
from .utils.email import send_booking_confirmation_email  

# Throttling
class StandardAnonThrottle(throttling.AnonRateThrottle):
    rate = '10/minute'

class StandardUserThrottle(throttling.UserRateThrottle):
    rate = '100/hour'

class ThrottleMixin:
    throttle_classes = [StandardAnonThrottle, StandardUserThrottle]


# ----- Appointment Slot ----- 
class AppointmentSlotViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = AppointmentSlot.objects.all()  
    serializer_class = AppointmentSlotSerializer  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return AppointmentSlot.objects.filter(doctor=user) 
        return AppointmentSlot.objects.all()  

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)  


# ----- Booking ----- 
class BookingViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = Booking.objects.all()  
    serializer_class = BookingSerializer 
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Booking.objects.filter(patient=user)  
        elif user.role == 'doctor':
            return Booking.objects.filter(slot__doctor=user)  
        return Booking.objects.none() 

    def perform_create(self, serializer):
        slot = serializer.validated_data['slot']
        if slot.is_booked:
            return Response({'error': 'This slot is already booked.'}, status=status.HTTP_400_BAD_REQUEST)

        slot.is_booked = True
        slot.save()

        booking = serializer.save(patient=self.request.user)

        # إرسال الإيميل بعد الحجز
        patient = self.request.user
        doctor_name = slot.doctor.get_full_name() or slot.doctor.username
        send_booking_confirmation_email(
            email=patient.email,
            patient_name=patient.get_full_name() or patient.username,
            doctor_name=doctor_name,
            date=slot.date,
            time=slot.time
        )


# ----- Appointment Request ----- 
class AppointmentRequestViewSet(ThrottleMixin, viewsets.ModelViewSet):
    queryset = AppointmentRequest.objects.all()  
    serializer_class = AppointmentRequestSerializer  
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return AppointmentRequest.objects.filter(patient=user) 
        elif user.role in ['doctor', 'admin']:
            return AppointmentRequest.objects.all()  
        return AppointmentRequest.objects.none() 

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)  


class UpdateUrgentBookingStatus(APIView):
    permission_classes = [IsAuthenticated]   

    def post(self, request, booking_id):
        status = request.data.get("status")
        if status not in ['approved', 'rejected']:
            return Response({"error": "Invalid status"}, status=400)

        try:
            booking = AppointmentRequest.objects.get(id=booking_id)
            booking.status = status
            booking.save()

            # إرسال الإشعار
            patient = booking.patient
            tokens = DeviceToken.objects.filter(user=patient)

            title = "تحديث حالة الحجز"
            body = "تمت الموافقة على حجزك المستعجل." if status == 'approved' else "تم رفض طلب الحجز المستعجل الخاص بك."

            for token in tokens:
                send_firebase_notification(token.token, title, body)

            return Response({
                "message": f"Status updated to {status} and notification sent to patient."
            })

        except AppointmentRequest.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)