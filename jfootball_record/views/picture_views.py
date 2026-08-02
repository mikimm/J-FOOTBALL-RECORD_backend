from rest_framework import generics
from jfootball_record.model_definition.picture_models import Picture
from jfootball_record.serializer.picture_serializer import UploadedPictureSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class PictureView(generics.CreateAPIView,generics.RetrieveAPIView):
    serializer_class = UploadedPictureSerializer
    queryset = Picture.objects.all().prefetch_related('record')
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response({"record": serializer.get_record(serializer.instance, image=serializer.data) }, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self,serializer,user_id):
        record=serializer.create_record(user_id)
        serializer.save(record_id=record.id)

