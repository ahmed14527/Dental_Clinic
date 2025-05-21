# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, VerifyCodeSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "تم تفعيل الحساب بنجاح."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "تم تسجيل الخروج بنجاح."})
        except Exception as e:
            return Response({"error": "حدث خطأ أثناء تسجيل الخروج."}, status=400)
