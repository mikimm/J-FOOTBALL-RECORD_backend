from rest_framework import generics
from jfootball_record.serializer.comments_serializer import CommentsSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class CommentsView(generics.CreateAPIView):
    serializer_class = CommentsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer,user_id):
        record_id = self.kwargs['record_id']
        serializer.save(record_id=record_id,comment_by_id=user_id)
