
from GSI import server
import time


"""
Currently not needed file, leaving it just for testing purposes at the moment
"""
gsi_server =  server.GSIServer(("localhost", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
gsi_server.start_server()
all_grenades = []
while True:
    data = gsi_server.get_data()
    if data.game_state:
        # print(data.all_players_data.data)
        for player_no, (player_data, player_id) in zip(data.all_players_data.all_players_dict.keys(), data.all_players_data.all_players_dict.values()):
            print(player_no, type(player_id), player_data.data)
        time.sleep(5)
    else:
        print("Game is not started yet")
        time.sleep(2)
