from dataclasses import asdict, dataclass, field
import json
from typing import Any, Optional

from jfootball_record.adaptor.adaptor import Adaptor
from jfootball_record.exception.exceptions import ExternalAPIError, NotFoundError
from jfootball_record.helpers.convert_function import convert_to_dataclass
from jfootball_record.model_definition.teams_models import Teams

    
def players_usecase_handle(**kwargs) -> dict:
    team_id=kwargs['team_id']
    player_id=kwargs['player_id']
    try:
        t=Teams.objects.get(id=team_id)
    except Teams.DoesNotExist:
            raise NotFoundError("team not found")
    try:
        output= Adaptor.get_squads(team_id= t.api_foot_ball_team_id)
    except Exception as e:
        raise ExternalAPIError(e)
    exist_flag=False
    for player in output["players"]:
        if player["id"] == player_id:
            exist_flag=True
            break
    if not exist_flag:
        raise NotFoundError("player not found")
    else:
        try:
            output= Adaptor.get_players(player_id= player_id,division_id=t.league.id)
        except Exception as e:
            raise ExternalAPIError(e)
    return output
    