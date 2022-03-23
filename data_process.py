import pandas as pd
import os
from datetime import date, datetime

class DataProcessor:
    def __init__(self,folder):

        self.main_folder = fr"projects\{folder}"

        self.matches_data_folder = fr"projects\{folder}\matches_data"
        self.rounds_data_folder = fr"projects\{folder}\rounds_data"
        self.players_data_folder = fr"projects\{folder}\players_data"

        if len(os.listdir(fr"projects\{folder}")) <= 2:#can be anything less than 3 basically
            os.mkdir(self.matches_data_folder)
            os.mkdir(self.rounds_data_folder)
            os.mkdir(self.players_data_folder)

        self.total = TotalData(self.main_folder)
        self.matches = MatchData(self.main_folder)
        self.rounds = RoundData(self.main_folder)
        self.players = PlayerData(self.main_folder)
        self.grenades = GrenadesData(self.main_folder)



    def process_data(self,data):
        self.data = data
        self.total.write_data(data)
        self.matches.write_data(data, self.total.last_match)
        self.rounds.write_data(data, self.matches.current_round, self.total.last_match)
        self.players.write_data(data)
        self.grenades.write_data(data)




class TotalData:
    def __init__(self, main_folder):
        self.file = fr"{main_folder}\total_data.csv"
        try:
            self.df = pd.read_csv(self.file)
        except FileNotFoundError:
            self.df = pd.DataFrame(
                columns=["match","provider_id", "all_players", "winning_team", "map", "start_time", "end_time", "date"],index = None)

    def check_game_phase(self):
        ct_score = self.data.map_data.team_ct["score"]
        t_score = self.data.map_data.team_t["score"]
        if ct_score == 16 or t_score == 16 or (t_score == 15 and ct_score == 15):
            game_active = False
        else:
            game_active = True
        return game_active


    def write_data(self, data):
        self.data = data
        today = date.today()
        today_pretty_written = today.strftime("%d/%m/%Y")
        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        player_list = []
        for name, value in self.data.all_players_data.all_players_dict.items():
            player_list.append(value[1])

        try:
            last_data = self.df.iloc[-1]
            self.last_match = self.df.iloc[-1,self.df.columns.get_loc("match")]

            match_number = self.last_match + 1
        except IndexError:
            match_number = 1
            self.last_match = 1
            last_data = {"provider_id":None, "all_players": None, "map": None}
        if self.check_game_phase():
            data_to_write = {"match": match_number ,"provider_id": data.provider_data.steamid,
                             "all_players": player_list, "map": data.map_data.name,
                             "start_time": current_time, "end_time": "x", "date": today_pretty_written}
            if (last_data["provider_id"] == data_to_write["provider_id"] and
                    last_data["all_players"] == data_to_write["all_players"]
                    and last_data["map"] == data_to_write["map"]) \
                    or len(data_to_write["all_players"]) != 10:
                pass
            else:
                self.df = self.df.append(data_to_write, ignore_index = True)
                self.df.to_csv(self.file, index = False)
                print("Written new game")
        else:
            if self.df.iloc[-1, self.df.columns.get_loc("end_time")] == "x":
                self.df.iloc[-1, self.df.columns.get_loc("end_time")] = current_time
                ct_score = self.data.map_data.team_ct["score"]
                t_score = self.data.map_data.team_t["score"]
                if ct_score == 16:
                    self.df.iloc[-1, self.df.columns.get_loc("winning_team")] = "CT"
                elif t_score == 16:
                    self.df.iloc[-1, self.df.columns.get_loc("winning_team")] = "T"
                else:
                    self.df.iloc[-1, self.df.columns.get_loc("winning_team")] = "draw"
                self.df.to_csv(self.file, index=False)
                print("Written end of game")
            else:
                pass



class MatchData:
    def __init__(self, main_folder):
        self.folder = fr"{main_folder}\matches_data"

    def write_data(self, data, match_number):
        current_game_id = match_number
        self.file = fr"{self.folder}\match_{current_game_id}.csv"
        try:
            self.df = pd.read_csv(self.file)
        except FileNotFoundError:
            self.df = pd.DataFrame(
                columns=["round","round_win_team", "round_win_type",
                         "round_win_players", "start_time", "end_time"],index = None)

        time_now = datetime.now()
        current_time = time_now.strftime("%H:%M:%S")
        current_round = data.map_data.round + 1

        try:
            last_round = self.df.iloc[-1, self.df.columns.get_loc("round")]
        except IndexError:
            last_round = 0
        print(last_round,current_round)
        self.current_round = current_round
        if data.round_data.phase != "over" and last_round != current_round:
            data_to_write = {"round": current_round, "round_win_players": [], "start_time": current_time, "end_time": "x"}
            print("New round")
            self.df = self.df.append(data_to_write, ignore_index= True)
            self.df.to_csv(self.file, index=False)

        elif last_round == current_round-1:
            if data.round_data.phase == "over" and self.df.iloc[-1, self.df.columns.get_loc("end_time")] == "x":
                win_team = data.round_data.data["win_team"]
                winning_players = []
                for player, value in data.all_players_data.data.items():
                    if value["team"] == win_team:
                        winning_players.append(player)

                try:
                    bomb_status = data.round_data.data["bomb"]
                except KeyError:
                    bomb_status = "elimination/time"


                self.df.iloc[-1, self.df.columns.get_loc("round_win_team")] = win_team
                self.df.iloc[-1, self.df.columns.get_loc("round_win_players")] = str(winning_players)
                self.df.iloc[-1, self.df.columns.get_loc("end_time")] = current_time
                self.df.iloc[-1, self.df.columns.get_loc("round_win_type")] = bomb_status
                print("End round")
                self.df.to_csv(self.file, index=False)



class RoundData:
    def __init__(self, main_folder):
        self.folder = fr"projects\{main_folder}\rounds_data"

    def write_data(self, data, current_round, current_match):
        pass

class PlayerData:
    def __init__(self, main_folder):
        self.folder = fr"projects\{main_folder}\players_data"

    def write_data(self, data):
        pass

class GrenadesData:
    def __init__(self, main_folder):
        try:
            self.df = pd.read_csv(fr"{main_folder}\grenades_data.csv")
        except FileNotFoundError:
            self.df = pd.DataFrame(
                columns=["grenade_no", "round_id", "match_id", "type", "start_position",
                         "end_position", "map", "by_player", "start_time", "end_time"])

    def write_data(self, data):
        pass



