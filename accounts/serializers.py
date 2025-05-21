from rest_framework import serializers
from .models import CustomUser, EmailVerificationCode
from .utils import send_verification_email
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        code_obj = EmailVerificationCode.objects.create(user=user)
        code_obj.generate_code()
        send_verification_email(user.email, code_obj.code)
        return user

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            code_obj = EmailVerificationCode.objects.get(user=user)
        except (CustomUser.DoesNotExist, EmailVerificationCode.DoesNotExist):
            raise serializers.ValidationError("المستخدم أو الكود غير صحيح.")

        if code_obj.code != data['code']:
            raise serializers.ValidationError("كود غير صحيح.")

        user.is_active = True
        user.save()
        code_obj.delete()  
        return data




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "تم تفعيل الحساب بنجاح."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError("لم يتم تفعيل هذا الحساب بعد.")
        return data