from dataclasses import asdict, dataclass, field
import json
from typing import Any, Optional

from jfootball_record.adaptor.adaptor import Adaptor
from jfootball_record.exception.exceptions import ExternalAPIError, NotFoundError
from jfootball_record.helpers.convert_function import convert_to_dataclass
from jfootball_record.model_definition.teams_models import Teams

# --- 最下層 ---
@dataclass
class Goals:
    score: int = 0   # "for" は予約語なので score にする
    against: int = 0


# --- team ---
@dataclass
class Team:
    name: str = ""
    founded: int | None | str = None
    logo: str = ""
    def __post_init__(self):
        if self.founded is None:
            self.founded = "---"
    
@dataclass
# --- team ---
class Venue:
    name: str = ""
    address: str = ""
    city: str = ""
    capacity: int = 0
    surface: str = ""
    image: str = ""


# --- root ---
@dataclass
class Response:
    team: Team = field(default_factory=Team)
    venue: Venue = field(default_factory=Team)
    
        
def team_usecase_handle(**kwargs) -> dict:
    team_id=kwargs['team_id']
    try:
        t=Teams.objects.get(id=team_id)
    except Teams.DoesNotExist:
            raise NotFoundError("team not found")
    try:
        output= Adaptor.get_team(team_id= t.api_foot_ball_team_id)
    except Exception as e:
        raise ExternalAPIError(e)
    #取得した辞書型をResponseオブジェクトに変換。Responseオブジェクトに存在しないキーは変換の対象にならない。
    class_response = convert_to_dataclass(Response,output)
    class_response.team.name=t.team_name
    #クラス化したobjを辞書型へ再帰的に変換
    output=asdict(class_response)
    try:
        squads= Adaptor.get_squads(team_id= t.api_foot_ball_team_id)
    except Exception as e:
        raise ExternalAPIError(e)
    output.update(squads)
    return output