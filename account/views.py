from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .serializer import *
from .tokens import create_token

# Test View
class TestView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request):
        return Response({"message": "Hello, world!"})

# Register User    
class UserRegisterView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
# Login User
class UserLoginView(APIView):
    permission_classes = []
    def post(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        if user is not None:
            tokens = create_token(user)
            return Response(tokens, status=201)
        else:
            return Response({"message": "Email or password is incorrect"})

class UpdateUserView(generics.UpdateAPIView, generics.GenericAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UpdateUserForGetSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)