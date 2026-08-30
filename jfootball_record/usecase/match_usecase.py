from dataclasses import asdict, dataclass, field
import json
import re
from typing import Any, Optional

from jfootball_record.adaptor.adaptor import Adaptor
from jfootball_record.exception.exceptions import ExternalAPIError, NotFoundError
from jfootball_record.helpers.convert_function import convert_to_dataclass
from jfootball_record.model_definition.teams_models import Teams

# --- Goals ---
@dataclass
class Goals:
    home: int | None = 0
    away: int | None= 0

# --- Fixture ---
@dataclass
class Fixture:
    date: str = ""
    def __post_init__(self):
        self.date=re.sub('T.*','',self.date)
    
# --- League ---
@dataclass
class League:
    name: str = ""
    round: str = ""
    def __post_init__(self):
        self.round=re.sub(r"\D", "",self.round)

# --- home ---
@dataclass
class Home:
    id: int = 0
    name: str = ""
    logo: str =""
    
# --- away ---
@dataclass
class Away:
    id: int = 0
    name: str = ""
    logo: str =""

# --- Match --- 
@dataclass
class Match:
    home: Home = field(default_factory=Home)
    away: Away = field(default_factory=Away)

# --- root ---
@dataclass
class Response:
    fixture: Fixture = field(default_factory=Fixture)
    league:  League = field(default_factory=League)
    teams:  Match = field(default_factory=Match)
    goals:  Goals = field(default_factory=Goals)
    
def match_usecase_handle(**kwargs) -> list:
    team_id=kwargs['team_id']
    response:list=[]
    try:
        t=Teams.objects.get(id=team_id)
    except Teams.DoesNotExist:
            raise NotFoundError("team not found")
    try:
        output= Adaptor.get_match(team_id= t.api_foot_ball_team_id)
    except Exception as e:
        raise ExternalAPIError(e)
    for o in output:
        class_response = convert_to_dataclass(Response,o)
        try:
            t=Teams.objects.get(api_foot_ball_team_id=class_response.teams.home.id)
        except Teams.DoesNotExist:
            raise NotFoundError("team not found")
        class_response.teams.home.name= t.team_name
        class_response.teams.home.id=t.id
        try:
            t=Teams.objects.get(api_foot_ball_team_id=class_response.teams.away.id)
        except Teams.DoesNotExist:
            raise NotFoundError("team not found")
        class_response.teams.away.name= t.team_name
        class_response.teams.away.id=t.id
        #クラス化したobjを辞書型へ再帰的に変換
        response.append(asdict(class_response))
    return response
    