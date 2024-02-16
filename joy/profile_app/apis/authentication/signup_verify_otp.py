import dataclasses

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from profile_app.models.user import User
from profile_app.services.otp import OTP_LENGTH, OTPService

@dataclasses.dataclass
class SignUpVerifyOTPRequest:
    email: str
    password: str
    phone_number: str

class SignUpVerifyOTP(APIView):
    def post(self, raw_request: Request) -> Response:
        request = SignUpVerifyOTPRequestSerializer.deserialize_request(raw_request)
        user = self.create_user(request)
        return Response()

    @classmethod
    def create_user(cls, request: SignUpVerifyOTPRequest) -> User:
        user = User()
        user.email = request.email
        user.set_password(request.password)
        user.phone_number = request.phone_number

        user.save()
        return user

class SignUpVerifyOTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=OTP_LENGTH, max_length=OTP_LENGTH)
    password = serializers.CharField(min_length=6)
    phone_number = serializers.CharField(min_length=11, max_length=11)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return SignUpVerifyOTPRequest(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )

    @classmethod
    def deserialize_request(cls, raw_request: Request) -> SignUpVerifyOTPRequest:
        serialized_request = SignUpVerifyOTPRequestSerializer(data=raw_request.data)
        serialized_request.is_valid(raise_exception=True)
        print("WHAT IS 1")
        cls.validate_request(serialized_request.validated_data)
        print("WHAT IS 2")

        request: SignUpVerifyOTPRequest = serialized_request.save()
        return request

    @classmethod
    def validate_request(cls, validated_data):
        print("WHAT IS 3")
        print("what is validated data", validated_data)
        if not OTPService.is_otp_valid(validated_data['otp'], validated_data['email']):
            raise ValidationError(detail={'detail': 'Wrong OTP'})
