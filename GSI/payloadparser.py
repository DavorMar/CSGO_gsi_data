
"""
Dispatching data into multiple classes for easier calls 
"""
class PayloadParser:
    def __init__(self):
        self.game_state = False
        self.map_data = None
        self.round_data = None
        self.all_players_data = None
        self.grenades_data = None
        self.provider_data = None
        self.len = 0
        self.bomb_data = None

    def empty_data(self):
        self.game_state = False

    def parse_data(self, payload):
        self.payload = payload

        # self.player_data = Player(payload[""])
        self.all_players_data = AllPlayers(payload["allplayers"])
        self.map_data = Map(payload["map"])
        self.round_data = Round(payload["round"])
        self.bomb_data = Bomb(payload["bomb"])

        self.grenades_data = Grenades(payload["grenades"])
        self.provider_data = Provider(payload["provider"])
        self.game_state = True




class Map:
    def __init__(self, map_data):
        self.data = map_data
        # self.round_wins = self.data["round_wins"]#dictionary of rounds
        self.mode = self.data["mode"]
        self.name = self.data["name"]
        self.phase = self.data["phase"]
        self.round = self.data["round"]
        self.team_ct = self.data["team_ct"]#dictionary[score, timeouts_remaining,
        self.team_t = self.data["team_t"]

class Bomb:
    def __init__(self, bomb_data):
        self.data = bomb_data
        self.state = self.data["state"]
        try:
            self.owner = self.data["player"]
        except KeyError:
            self.owner = None

class Round:
    def __init__(self,round_data):
        self.data = round_data
        self.phase = self.data["phase"]

class AllPlayers:
    def __init__(self, allplayers_data):
        self.data = allplayers_data
        # self.all_player_dict = {self.player_0:{}, self.player_1:{}, self.player_2:{},self.player_3:{},
        #                         self.player_4:{}, self.player_5:{}, self.player_6:{}, self.player_7:{},
        #                         self.player_8:{}, self.player_9:{}}
        self.all_players_dict = {}


        for number, (player, data) in enumerate(sorted(self.data.items())):
            self.all_players_dict[f"player_{number}"] = [Player(data), player]

class Player:
    def __init__(self, player_data):
        self.data = player_data
        self.name = player_data["name"]
        # self.observer_slot = player_data["observer_slot"]
        self.team = player_data["team"]
        self.match_stats = player_data["match_stats"]
        self.kills = self.match_stats["kills"]
        self.assists = self.match_stats["assists"]
        self.deaths = self.match_stats["deaths"]
        self.mvps = self.match_stats["mvps"]
        self.score = self.match_stats["score"]
        self.position = self.data["position"]
        self.forward = self.data["forward"]
        self.state = self.data["state"]
        self.health = self.state["health"]
        self.armor = self.state["armor"]
        self.helmet = self.state["helmet"]
        self.flashed = self.state["flashed"]
        self.burning = self.state["burning"]
        self.money = self.state["money"]
        self.round_kills = self.state["round_kills"]
        self.round_killhs = self.state["round_killhs"]
        self.round_totaldmg = self.state["round_totaldmg"]
        self.equip_value = self.state["equip_value"]
        self.weapons = self.data["weapons"]
        # if self.team == "CT":
        #     self.defusekit = self.state["defusekit"]
        # else:
        #     self.defusekit = False


class Grenades:
    def __init__(self, grenades_data):
        self.data = grenades_data

class Provider:
    def __init__(self, provider_data):
        self.data = provider_data
        self.name = self.data["name"]
        self.appid = self.data["appid"]
        self.version = self.data["version"]
        self.steamid = self.data["steamid"]
        self.timestamp = self.data["timestamp"]


