from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.shortcuts import redirect

from .oauth_logic import GithubAppStrategy
from .serializers import UserSerializer
from .helpers import get_auth_token


# Create your views here.


class GithubSignup(APIView):
    def get(self, request, *args, **kwargs):
        handler = GithubAppStrategy.get_or_create_object()
        return redirect(handler.get_full_client_authorization_url(request))

    def post(self, request, *args, **kwargs):
        url = request.data.get("full_url")
        if not url:
            return Response(
                {"message": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
        handler = GithubAppStrategy.get_or_create_object()
        user = handler.process_callback_information(url, request)

        if not user:
            return Response(
                {"message": "invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(get_auth_token(user))
