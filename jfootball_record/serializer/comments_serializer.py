from rest_framework import serializers

from django.db import models
from jfootball_record.model_definition.comments_models import Comments
from jfootball_record.model_definition.users_models import Users

# Comments用シリアライザー
class CommentsSerializer(serializers.ModelSerializer):
    comment_by = serializers.CharField(
        source="comment_by.username",
        read_only=True
    )
    class Meta:
        model=Comments
        exclude = ['record']