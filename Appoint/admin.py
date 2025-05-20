from django.contrib import admin
from .models import AppointmentSlot, Booking, AppointmentRequest

@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'time', 'is_booked')
    list_filter = ('doctor', 'date', 'is_booked')
    search_fields = ('doctor__username',)
    ordering = ('date', 'time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'slot', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient__username', 'slot__doctor__username')

@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'preferred_date', 'created_at')
    search_fields = ('patient__username', 'notes')
    ordering = ('-created_at',)
