"""
this class gets called from data_process.py TotalData class, which restarts ChgDetect on each new match.
It will serve as a tool to detect changes in player stats, so players table can be updated

"""

class ChgDetect:
    def __init__(self, players_data):
        self.player_dict = {}
        self.bomb_planter = None
        self.bomb_defuser = None
        self.bomb_status = False
        for player_data, player_id in players_data.all_players_dict.values():
            self.player_dict[f"{player_id}"] = {"kills" : 0, "deaths" : 0 , "assists" : 0, "score" : 0, "mvps" : 0,
                                                "bombs_planted" : 0, "bombs_defused": 0}


    def register_players_change(self, players_data):
        list_of_changes = []
        for player_data, player_id in players_data.all_players_dict.values():
            for key in ["kills", "deaths", "assists", "score", "mvps"]:
                recorded_player_value = player_data.data["match_stats"][key]
                written_player_value = self.player_dict[f"{player_id}"][key]
                difference = recorded_player_value - written_player_value
                for _ in range(difference):
                    list_of_changes.append([player_id, key])
                    self.player_dict[f"{player_id}"][key] += 1
        return list_of_changes

    def register_bomb_plant_defuse(self, bomb_data):
        list_of_changes = []
        bomb_state = bomb_data.state

        if bomb_state == "planting":
            self.bomb_planter = bomb_data.owner
        elif bomb_state == "planted":
            if not self.bomb_status:
                list_of_changes.append([self.bomb_planter,"bombs_planted"])
                self.player_dict[f"{self.bomb_planter}"]["bombs_planted"] += 1
                self.bomb_status = True
        elif bomb_state == "defusing":
            self.bomb_defuser = bomb_data.owner
        elif bomb_state == "defused":
            if self.bomb_status:
                list_of_changes.append([self.bomb_defuser, "bombs_defused"])
                self.player_dict[f"{self.bomb_defuser}"]["bombs_defused"] += 1
                self.bomb_status = False


        return list_of_changes

    def get_changes(self, players_data, bomb_data):
        all_changes = []
        player_changes = self.register_players_change(players_data)
        bomb_changes = self.register_bomb_plant_defuse(bomb_data)
        for player_change in player_changes:
            all_changes.append(player_change)
        for bomb_change in bomb_changes:
            all_changes.append(bomb_change)
        return all_changes







