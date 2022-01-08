from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)


class Events(APIView):
    def post(self, request):

        slack_message = request.data

        if slack_message.get("token", None) != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type", None) == "url_verification":
            return Response(slack_message, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)
