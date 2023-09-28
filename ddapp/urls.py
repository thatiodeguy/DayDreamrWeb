from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.contrib.auth import views as auth_views

from .views import UserViewSet, RoadmapViewSet, TaskViewSet, RegisterView, PasswordResetRequestView, UserProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roadmaps', RoadmapViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', obtain_jwt_token, name='login'),
    path('token-refresh/', refresh_jwt_token, name='token_refresh'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
