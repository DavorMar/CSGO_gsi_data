import numpy as np
import pandas as pd
import time
import os

class DataProcessor:
    def __init__(self,folder):
        self.main_folder = folder
        try:
            self.total_data_df = pd.read_csv(fr"{self.main_folder}\total_data.csv")
        except FileNotFoundError:
            self.total_data_df = pd.DataFrame(
                columns=["match", "team_1", "team_2", "winning team", "score", "start_time", "end_time", "map" "date"])
        try:
            self.grenades_data_csv = pd.read_csv(fr"{self.main_folder}\grenades_data.csv")
        except FileNotFoundError:
            self.grenades_data_csv = pd.DataFrame(
                columns=["grenade_no", "round_id", "match_id", "type", "start_position",
                         "end_position", "map", "by_player", "start_time", "end_time"])

        self.matches_data_folder = fr"projects\{folder}\matches_data"
        self.rounds_data_folder = fr"projects\{folder}\rounds_data"
        self.players_data_folder = fr"projects\{folder}\players_data"

        if len(os.listdir(fr"projects\{folder}")) <= 2:#can be anything less than 3 basically
            os.mkdir(self.matches_data_folder)
            os.mkdir(self.rounds_data_folder)
            os.mkdir(self.players_data_folder)


    def process_data(self,data):
        self.data = data

    def write_total_data(self):
        pass



# class TotalData:
#     def __init__(self, data, main_folder):
#
#
# class RoundData:
#     def __init__(self, data, main_folder):
#         pass
#
# class MatchData:
#     def __init__(self, data, main_folder):
#         pass
#
# class PlayerData:
#     def __init__(self, data, main_folder):
#         pass
#
# class GrenadesData:
#     def __init__(self, data, main_folder):
#         pass



