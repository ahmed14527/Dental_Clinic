from rest_framework import viewsets, permissions
from .models import  User
from .serializers import  RegisterSerializer
from rest_framework.generics import CreateAPIView

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
class CreateUserByAdminView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser]  

    def perform_create(self, serializer):
        role = self.request.data.get('role', 'patient')
        serializer.save(role=role)