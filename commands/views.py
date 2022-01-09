from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import slack
import re
from utils.scheduler import scheduleMeet
from pprint import pprint

SLACK_VERIFICATION_TOKEN = getattr(settings, "SLACK_VERIFICATION_TOKEN", None)
SLACK_BOT_USER_TOKEN = getattr(settings, "SLACK_BOT_USER_TOKEN", None)

client = slack.WebClient(SLACK_BOT_USER_TOKEN)

BOT_ID = client.api_call("auth.test")["user_id"]


class PlanCommand(APIView):
    def post(self, request):

        payload = request.data

        if not payload.get("token", None) == SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        team_id = payload.get("team_id", None)
        meet_info = payload.get("text", None)
        if not (team_id and meet_info):
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        members = client.users_list(team_id=team_id)["members"]
        members = list(
            filter(lambda member: member["is_email_confirmed"], members))

        emails = list(
            map(
                lambda member: {"email": member["profile"]["email"]},
                members,
            )
        )
        if not emails:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. No Team mates found !!",
                },
                status=status.HTTP_200_OK,
            )

        meet_link = re.findall(r"<((?:http|https).+)>", meet_info)
        meet_link = list(
            filter(lambda link: link.startswith(
                "https://meet.google.com"), meet_link)
        )
        if not meet_link:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. INVALID G-meet link !!",
                },
                status=status.HTTP_200_OK,
            )
        if len(meet_link) > 1:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You cannot add multiple G-meet links as of now !!",
                },
                status=status.HTTP_200_OK,
            )
        meet_link = meet_link[0]

        s_datetime = re.findall(
            r"(\d{1,2}(?:\.|/|-)\d{1,2}(?:\.|/|-)(?:\d{2}|\d{4})/\d{0,2}:\d{0,2})", meet_info
        )
        if not s_datetime:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You did not mention start time !!",
                },
                status=status.HTTP_200_OK,
            )

        if len(s_datetime) > 1:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You cannot add multiple start times as of now !!",
                },
                status=status.HTTP_200_OK,
            )

        s_datetime = s_datetime[0].split("/")
        s_date = s_datetime[0]

        if "." in s_date:
            s_date = s_date.split(".")
        elif "-" in s_date:
            s_date = s_date.split("-")
        else:
            s_date = s_datetime[:3]

        s_time = s_datetime[-1].split(":")
        hour = s_time[0]
        minute = s_time[1]
        if not hour:
            hour = 0
        if not minute:
            minute = 0
        hour = int(hour)
        minute = int(minute)

        year = s_date[-1]
        if len(year) == 2:
            year = f"20{year}"
        year = int(year)

        month = int(s_date[1])
        day = int(s_date[0])

        duration = re.findall(r"duration:(\d{1})", meet_info)
        if not duration:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You did not enter your meet duration !!",
                },
                status=status.HTTP_200_OK,
            )
        if len(duration) > 1:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You cannot add multilpe meet durations as of now !!",
                },
                status=status.HTTP_200_OK,
            )

        duration = int(duration[0])

        meet_info = meet_info.split(",")
        meet_info = list(map(lambda info: info.strip(), meet_info))
        if not meet_info:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. You did not enter your meet name !!",
                },
                status=status.HTTP_200_OK,
            )
        meet_name = meet_info[0]

        try:
            meet_datetime = datetime(year=year, month=month,
                                     day=day, hour=hour, minute=minute, second=0)
        except:
            return Response(
                {
                    "response_type": "ephemeral",
                    "text": "Sorry, slash commando, that didn't work. Your datetime format was incorrect !!",
                },
                status=status.HTTP_200_OK,
            )

        try:
            print("\n\n")
            print(meet_name)
            print(meet_link)
            print(meet_datetime)
            print(duration)
            print(emails)
            print("\n")
            meet = scheduleMeet(meet_name=meet_name, meet_link=meet_link,
                                s_datetime=meet_datetime, duration=duration, emails=emails)
            pprint(meet)
            print("\n\n")
        except Exception as e:
            print(e)
            return Response(
                {"text": "Sorry, slash commando, that didn't work. We could not schedule your meeting !!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"text": "Thank You !! Your meeting has been scheduled."},
            status=status.HTTP_200_OK,
        )


class Events(APIView):
    def post(self, request):

        slack_message = request.data

        if slack_message.get("token", None) != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type", None) == "url_verification":
            return Response(data=slack_message, status=status.HTTP_200_OK)

        event_message = slack_message.get("event", None)
        if event_message:
            channel = event_message.get("channel", None)
            text = event_message.get("text", "")

            if not event_message.get("user", None) == BOT_ID:
                # client.chat_postMessage(channel=channel, text=text)
                print(f"Message found: {text} in channel: {channel}")

        return Response(status=status.HTTP_200_OK)
