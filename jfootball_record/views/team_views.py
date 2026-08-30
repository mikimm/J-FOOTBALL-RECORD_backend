from django.http import JsonResponse
from rest_framework import generics
from jfootball_record.exception.exception_handler import hundle_exception
from jfootball_record.model_definition.teams_models import Teams
from jfootball_record.serializer.teams_serializer import TeamsSerializer
from rest_framework.views import APIView
from jfootball_record.usecase.team_usecase import team_usecase_handle
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class TeamListView(generics.ListAPIView):
    serializer_class = TeamsSerializer
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        # URLからリーグIDを取得してフィルタ
        league_id = self.kwargs['league_id']
        return Teams.objects.filter(league_id=league_id)


class TeamDetailView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        try:
            output=team_usecase_handle(team_id=self.kwargs['team_id'])
        except Exception as e:
            return hundle_exception(e)
        return JsonResponse(output)