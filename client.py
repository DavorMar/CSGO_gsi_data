
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
        for grenade,grenade_data in data.grenades_data.data.items():
            print(grenade_data)
            try:
                print(grenade_data["position"])
            except:
                print("NO POSITION DATA FOR ", grenade_data)
                time.sleep(10)
        time.sleep(0.1)
    else:
        print("Game is not started yet")
        time.sleep(2)
