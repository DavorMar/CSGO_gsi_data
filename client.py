
from GSI import server
import time


"""
Currently not needed file, leaving it just for testing purposes at the moment
"""
gsi_server =  server.GSIServer(("localhost", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
gsi_server.start_server()


data = gsi_server.get_data()
if data.game_state:
    for name, value in data.all_players_data.all_players_dict.items():
        print(value[1])
else:
    print("Game is not started yet")
time.sleep(2)