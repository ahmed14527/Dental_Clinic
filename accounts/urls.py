from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    
)
from .views import (RegisterView,CreateUserByAdminView)

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('api/token/logout/', TokenBlacklistView.as_view(), name='token_blacklist'), 
    path('api/admin/create-user/', CreateUserByAdminView.as_view(), name='admin_create_user')
 
]