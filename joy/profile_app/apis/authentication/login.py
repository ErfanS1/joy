import dataclasses

from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from profile_app.services.authentication import authenticate


class Login(APIView):
    def post(self, raw_request: Request) -> Response:
        request: LoginRequest = LoginRequestSerializer.deserialize_request(raw_request)
        user = authenticate(email=request.email, password=request.password)

        if user is None:
            # todo add logs
            raise AuthenticationFailed()

        # todo write email service
        # send_email()
        return Response(data={"login successful"}, status=HTTP_200_OK)


@dataclasses.dataclass
class LoginRequest:
    email: str
    password: str


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    @classmethod
    def deserialize_request(cls, raw_request: Request) -> LoginRequest:
        serialized_request = LoginRequestSerializer(data=raw_request.data)
        serialized_request.is_valid(raise_exception=True)
        request: LoginRequest = serialized_request.save()
        return request

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return LoginRequest(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
