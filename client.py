
from GSI import server
import time

gsi_server =  server.GSIServer(("localhost", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
gsi_server.start_server()


data = gsi_server.get_data()
if data.game_state:
    print(data.map_data.round_wins)
else:
    print("Game is not started yet")
time.sleep(2)