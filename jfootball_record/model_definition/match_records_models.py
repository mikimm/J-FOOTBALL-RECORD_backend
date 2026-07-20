from django.db import models

from jfootball_record.model_definition.teams_models import Teams
from jfootball_record.model_definition.users_models import Users

class MatchRecords(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    record=models.TextField(max_length=1000)
    home_team =models.ForeignKey(Teams,related_name="home",on_delete=models.SET_NULL,null=True)
    home_score=models.IntegerField()
    away_team =models.ForeignKey(Teams,related_name="away",on_delete=models.SET_NULL,null=True)
    away_score=models.IntegerField()
    round=models.IntegerField()
    match_day=models.DateField()
    created_by=models.ForeignKey(Users,on_delete=models.CASCADE,db_column='created_by')