import json

from rest_framework import generics
from jfootball_record.model_definition.comments_models import Comments,Users
from jfootball_record.serializer.comments_serializer import CommentsSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentsView(generics.ListCreateAPIView):
    serializer_class = CommentsSerializer
    queryset = None
    # authentication_classes = (SessionAuthentication,)
    # permission_classes = (IsAuthenticated, )
    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,request.user.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer,user_id):
        record_id = self.kwargs['record_id']
        serializer.save(record_id=record_id,comment_by_id=1)
    # コメント一覧をrecord_idで絞り込み
    def get(self, request, *args, **kwargs):
        record_id = self.kwargs['record_id']
        self.queryset = Comments.objects.filter(record_id=record_id)
        return self.list(request, *args, **kwargs)
    # コメントの総数を返すようにオーバーライド
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"count":self.queryset.count(),"comments":serializer.data})

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accepts the WebSocket connection.
        print("connection")
        await self.accept()

    # leave a Group
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive comment from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['message']

        # save comment db
        res = await self.save_comment_to_db(comment)
        # send comment to group(chat グループに属する全てのクライアントに対してブロードキャスト)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_comment',
                'comment': res.comment,
                'comment_by':res.comment_by.username
            }
        )
    # Receive comment from group
    async def chat_comment(self, event):
        comment = event['comment']
        comment_by = event['comment_by']
        # WebSocketを介してメッセージを送信
        await self.send(text_data=json.dumps({
            'comment': comment,
            'comment_by': comment_by
        }))

    @database_sync_to_async
    def save_comment_to_db(self, comment_text):
        record_id=self.scope["url_route"]['kwargs']['record_id']
        comment=Comments.objects.create(
                record_id= record_id,
                comment=comment_text,
                comment_by_id=1)
        comment=Comments.objects.select_related("comment_by").get(id=comment.id)
        return comment