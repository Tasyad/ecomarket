from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        write_only=True,
        required=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    is_vendor = serializers.ChoiceField(choices=((True, 'Vendor'),
                                        (False, 'Customer'))

    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'phone', 'password', 'password2', 'is_vendor']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn`t match."}
            )
        return attrs

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['user', 'first_name', 'phone', 'is_vendor']

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     account = Account.objects.create(
    #         user=user,
    #         first_name=validated_data['first_name'],
    #         second_name=validated_data['second_name'],
    #         phone=validated_data['phone'],
    #         is_vendor=validated_data['is_vendor']
    #     )
    #     account.save()
    #     return user