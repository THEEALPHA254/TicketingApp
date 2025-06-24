from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

@api_view(['POST'])
def login(request):
    serializer = ClientLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Determine the user's role
        if user.is_superuser:
            user_type = "superadmin"
        elif user.is_staff:
            user_type = "admin"
        else:
            user_type = "user"

        # Serialize user data
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "user_type": user_type  # Add user role to response
        }

        # Add tokens to user data
        user_data['access'] = str(access_token)
        user_data['refresh'] = str(refresh)

        return Response(user_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#register view
@api_view(['POST'])
def register(request):
    serializer = ClientRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_role(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_superuser:
            user_role = "Super Admin"
        elif user.is_staff:
            user_role = "Admin"
        else:
            user_role = "Regular User"
        
        return Response({"user_type": user_role}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def users(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    if not user.is_superuser:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



