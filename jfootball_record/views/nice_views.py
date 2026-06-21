
from rest_framework.response import Response
from jfootball_record.exception.exception_handler import hundle_exception
from jfootball_record.model_definition.match_records_models import MatchRecords
from jfootball_record.model_definition.nice_models import Nice
from jfootball_record.serializer.nice_serializer import NiceSerializer
from rest_framework import viewsets,mixins
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class NiceView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = NiceSerializer
    lookup_url_kwarg = "record_id"
    lookup_field="record_id"
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
         
    def perform_create(self,serializer,user_id):
        record_id = self.kwargs.get(self.lookup_url_kwarg)
        serializer.check_create(data={"post_by_id":user_id,"record_id":record_id})
        serializer.save(record_id=record_id,post_by_id=user_id)

        
    def list(self, request, *args, **kwargs):
        record_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            mobj=MatchRecords.objects.get(id=record_id)
        except Exception as e:
            return hundle_exception(e)
        count=Nice.objects.filter(record=mobj).count()
        return JsonResponse({"いいね":count},status=status.HTTP_200_OK)
