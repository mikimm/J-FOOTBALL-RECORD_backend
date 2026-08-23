from dataclasses import dataclass, field ,asdict
import json
from typing import Any, Optional

from jfootball_record.adaptor.adaptor import Adaptor
from jfootball_record.exception.exceptions import ExternalAPIError
from jfootball_record.helpers.convert_function import convert_to_dataclass
from operator import attrgetter

from jfootball_record.model_definition.teams_models import Teams

# --- 最下層 ---
@dataclass
class Goals:
    score: int = 0   # "for" は予約語なので score にする
    against: int = 0

# --- stats要素 ---
@dataclass
class Stats:
    played: int = 0
    win: int = 0
    draw: int = 0
    lose: int = 0
    goals: Goals = field(default_factory=Goals)


# --- team要素 ---
@dataclass
class Team:
    id: int = 0
    name: str = ""
    image: str = ""


# --- standings要素 ---
@dataclass
class Standing:
    rank: int = 0
    team: Team = field(default_factory=Team)
    points: int = 0
    goalsDiff: int = 0
    group: str = ""
    form: Optional[str] = None
    description: Optional[str] = None

    all: Stats = field(default_factory=Stats)


# --- root ---
@dataclass
class Response:
    standings: list[Standing] = field(default_factory=[Standing])
    
        
def league_usecase_handle(sort_key:str,order:str,division_id:str) -> dict:
    try:
        output= Adaptor.get_ranking(division_id=division_id)
    except Exception as e:
        raise ExternalAPIError(e)
    #取得した辞書型をResponseオブジェクトに変換。Responseオブジェクトに存在しないキーは変換の対象にならない。
    class_response = convert_to_dataclass(Response,{'standings':output})
    
    #scoreキーに外部APIのall.goals.forの値を代入
    goals_for_list=[i["all"]["goals"]["for"] for i in output]
    for i,cs in enumerate(class_response.standings):
        cs.all.goals.score=goals_for_list[i]
        team=Teams.objects.values_list('team_name', 'team_logo').get(api_foot_ball_team_id=cs.team.id)
        cs.team.name=team[0]
        cs.team.image=team[1]
    #ソートに紐づくクエリがある場合に実行
    if sort_key and order:
        order = True if order ==  "asc" else False
        class_response.standings.sort(key=attrgetter(sort_key),reverse=order)
    #クラス化したobjを辞書型へ再帰的に変換
    output=asdict(class_response)
    return output
    
    