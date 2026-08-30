from typing import Any
import requests

from backend.settings import SEASON, TIME_ZONE, X_API_SPORTS_KEY

class Adaptor():
    #外部API呼び出し関数
    def _call_api(url:str,parameter:dict) ->dict:
        headers = {"x-apisports-key": X_API_SPORTS_KEY}
        response = requests.get(url, params=parameter,headers=headers)
        if response.status_code !=200:
            raise Exception(response.json())  
        return_data = {"status": response.status_code, "data": response.json()}     
        return return_data
    #順位取得
    @classmethod
    def get_ranking(cs,**kwargs) -> dict:
        division_id=kwargs["division_id"]
        parameter = {
        "league": division_id,
        "season": SEASON 
        }
        output=cs._call_api("https://v3.football.api-sports.io/standings",parameter)
        return output["data"]["response"][0]["league"]["standings"][0]
    #チーム詳細取得
    @classmethod
    def get_team(cs,**kwargs) -> dict:
        team_id=kwargs["team_id"]
        parameter = {
        "id": {team_id}
        }
        output=cs._call_api("https://v3.football.api-sports.io/teams",parameter)
        return output["data"]["response"][0]
    #所属選手一覧取得
    @classmethod
    def get_squads(cs,**kwargs) -> dict:
        team_id=kwargs["team_id"]
        parameter = {
        "team": {team_id}
        }
        output=cs._call_api("https://v3.football.api-sports.io/players/squads?",parameter)
        output["data"]["response"][0].pop("team")
        return output["data"]["response"][0]
    #選手詳細取得
    @classmethod
    def get_players(cs,**kwargs) -> dict:
        player_id=kwargs["player_id"]
        parameter = {
        "id": {player_id},
        "season": SEASON
        }
        output=cs._call_api("https://v3.football.api-sports.io/players/?",parameter)
        return output["data"]["response"][0]
    #試合結果取得
    @classmethod
    def get_match(cs,**kwargs) -> list:
        team_id=kwargs["team_id"]
        parameter = {
        "timezone": TIME_ZONE,
        "season": SEASON,
        "team":team_id
        }
        output=cs._call_api("https://v3.football.api-sports.io/fixtures/?",parameter)
        return output["data"]["response"]
    
