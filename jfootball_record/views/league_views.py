from django.http import JsonResponse
from jfootball_record.exception.exception_handler import hundle_exception
from rest_framework.views import APIView
from rest_framework import status

from jfootball_record.usecase.league_usecase import league_usecase_handle
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

allow_pattern=[
    {'sort': ['points'], 'order': ['desc']},
    {'sort': ['points'], 'order': ['asc']},
    {'sort': ['goalsDiff'], 'order': ['desc']},
    {'sort': ['goalsDiff'], 'order': ['asc']},
    {'sort': ['all.win'], 'order': ['desc']},
    {'sort': ['all.win'], 'order': ['asc']},
    {'sort': ['all.lose'], 'order': ['desc']},
    {'sort': ['all.lose'], 'order': ['asc']},
    {'sort': ['all.draw'], 'order': ['desc']},
    {'sort': ['all.draw'], 'order': ['asc']},
    {'sort': ['all.goals.score'], 'order': ['desc']},
    {'sort': ['all.goals.score'], 'order': ['asc']},
    {'sort': ['all.goals.against'], 'order': ['desc']},
    {'sort': ['all.goals.against'], 'order': ['asc']},
    {'sort': ['rank'], 'order': ['desc']},
    {'sort': ['rank'], 'order': ['asc']},
]

allow_division=[98,99,100]
class LeagueRankingView(APIView):
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        division_id=kwargs["division_id"]
        if not division_id in allow_division:
            return JsonResponse({"error":"bad request"},status=status.HTTP_400_BAD_REQUEST)
        if not self.request.GET:
            sort_key=None
            order=None
        elif not self.request.GET in allow_pattern:
            return JsonResponse({"error":"bad request"},status=status.HTTP_400_BAD_REQUEST)
        else:
            sort_key=self.request.GET["sort"]
            order=self.request.GET["order"]
        try:
            output=league_usecase_handle(sort_key,order,division_id)
        except Exception as e:
            return hundle_exception(e)
        return JsonResponse(output)