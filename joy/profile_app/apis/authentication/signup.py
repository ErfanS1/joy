import dataclasses

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profile_app.models.user import User

@dataclasses.dataclass
class SignUpRequest:
    email: str
    password: str
    phone_number: str

class SignUp(APIView):
    def post(self, raw_request: Request) -> Response:
        request = SignUpRequestSerializer.deserialize_requset(raw_request)

        user = self.create_user(request)
        return Response({'user': user.email, 'id': user.id}, status=200)

    @classmethod
    def create_user(cls, request: SignUpRequest) -> User:
        user = User()
        user.email = request.email
        user.set_password(request.password)
        user.phone_number = request.phone_number

        user.save()

        return user




class SignUpRequestSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return SignUpRequest(**validated_data)

    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    phone_number = serializers.CharField(min_length=11, max_length=11)

    @classmethod
    def deserialize_requset(cls, raw_request: Request) -> SignUpRequest:
        serialized_request = SignUpRequestSerializer(data=raw_request.data)
        serialized_request.is_valid(raise_exception=True)
        request: SignUpRequest = serialized_request.save()

        return request

    @classmethod
    def validate_email(cls, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError({'detail': 'Email Already Exists'})

        return value


