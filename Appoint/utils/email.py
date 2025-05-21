# utils/email.py
from django.core.mail import send_mail

def send_booking_confirmation_email(email, patient_name, doctor_name, date, time):
    subject = "تأكيد حجز الموعد"
    message = f"""مرحبًا {patient_name}،

تم تأكيد حجز الموعد مع الدكتور {doctor_name}.

 التاريخ: {date}
 الوقت: {time}

نتمنى لك دوام الصحة والعافية.
"""
    send_mail(subject, message, None, [email])



