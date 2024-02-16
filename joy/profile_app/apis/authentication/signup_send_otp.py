import dataclasses

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT

from profile_app.models.user import User
from profile_app.services.otp import OTPService

@dataclasses.dataclass
class SignUpRequest:
    email: str

class SignUpSendOTP(APIView):
    def post(self, raw_request: Request) -> Response:
        request = SignUpRequestSerializer.deserialize_requset(raw_request)

        # send otp to email
        OTPService().send_otp(request.email)
        return Response(status=HTTP_204_NO_CONTENT)

class SignUpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return SignUpRequest(**validated_data)

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


