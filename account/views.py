from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Account
from account.serializers import RegisterSerializer, MyTokenObtainPairSerializer, AccountSerializer
# from product.models import Cart
from .permissions import AnonPermissionOnly, IsVendor


class MyObtainPairView(TokenObtainPairView):
    permission_classes = (AnonPermissionOnly,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterApiView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        serializers = RegisterSerializer(data=request.data)
        if serializers.is_valid():
            user = User.objects.create(
                username=request.data['username'],
                email=request.data['email'],
            )
            user.set_password(request.data['password'])
            user.save()
            account = Account.objects.create(
                user=user,
                first_name=request.data['first_name'],
                phone=request.data['phone'],
                is_vendor=request.data['is_vendor']
            )
            account.save()
            # cart = Cart.objects.create(
            #     user=user
            # )
            # cart.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountListApiView(APIView):
    permission_classes = [IsVendor]

    def get(self, request):
        users = Account.objects.all()
        serializer = AccountSerializer(users, many=True)
        # serializer.data['user'] =
        return Response(serializer.data)


# class AccountListApiView(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get(self, request):
#         users = Account.objects
#         serializer = RegisterSerialize(users, many=True)
#         return Response(serializer.data)