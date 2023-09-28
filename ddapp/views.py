from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from ddapp.models import CustomUser as User
from rest_framework_jwt.settings import api_settings
from .models import CustomUser, Roadmap, Task, PasswordResetToken
from .serializers import UserSerializer, RoadmapSerializer, TaskSerializer, PasswordResetRequestSerializer
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserProfileView(View):
    template_name = 'user_profile.html'

    @method_decorator(login_required)
    def get(self, request):
        try:
            user = self.request.user
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            return render(request, self.template_name, {'error_message': 'User not found'})
        
        context = {'user': user}
        return render(request, self.template_name, context)

class RoadmapViewSet(viewsets.ModelViewSet):
    queryset = Roadmap.objects.all()
    serializer_class = RoadmapSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roadmap = serializer.save(owner=request.user)
        return Response(RoadmapSerializer(roadmap).data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roadmap = get_object_or_404(Roadmap, id=request.data['roadmap'])
        task = serializer.save(roadmap=roadmap)
        return Response(TaskSerializer(task).data)

class RegisterView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
    
        # Retrieve the user instance
        user = User.objects.get(username=serializer.data['username'])

        # Generate the JWT token
        payload = api_settings.JWT_PAYLOAD_HANDLER(user)
        token = api_settings.JWT_ENCODE_HANDLER(payload)

        headers = self.get_success_headers(serializer.data)
        return Response({'token': token, 'user': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # Create a token and save to the database
                token = PasswordResetToken.objects.create(user=user)
                
                # Send email (this will print to console for now)
                send_mail(
                    'Password Reset Request',
                    f'Use the following token to reset your password: {token.token}',
                    'noreply@daydreamr.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with given email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)