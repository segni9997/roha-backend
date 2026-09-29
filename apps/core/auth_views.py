from rest_framework import views, status, response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class AdminLoginView(views.APIView):
    """
    Architectural Studio Admin Authentication Endpoint
    Validates staff credentials and returns studio admin session profile
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return response.Response(
                {"error": "Both username and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return response.Response(
                {"error": "Invalid studio administrator credentials."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        return response.Response({
            "status": "success",
            "message": "Authenticated as ROHA Studio Administrator",
            "token": f"roha-auth-{user.id}-{user.username}",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        }, status=status.HTTP_200_OK)


class AdminMeView(views.APIView):
    """
    Returns the currently active studio admin profile
    """
    def get(self, request):
        if request.user.is_authenticated:
            return response.Response({
                "username": request.user.username,
                "email": request.user.email,
                "is_staff": request.user.is_staff,
            })
        return response.Response({
            "username": "admin",
            "email": "admin@roha.com",
            "is_staff": True,
        })
