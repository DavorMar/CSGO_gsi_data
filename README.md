# CSGO_gsi_data
This is a simple code to collect data from CSGO games. Idea is to create different data tables from multiple games. Total data table holds simple summary of
all the games recorded, with most basic data(players, time , winning team, map etc). Then there is a separate table creates for each game which holds info about said game, where we find simple data 
about each round (like winning team, was it a bomb win or elimination, players in the round etc). Next there is a separate table created for each round in each game
(which comes to 16-30+ tables per game), which holds detailed info about each player in each round(like weapons, money, worth, kills, damage, headshots in that round).
Next plan is to develop a record for each grenade thrown, a record of certain details for players and  Player summary data for each game(simple kills, deaths,
assists mvps etc). Plan after that is further development of UI and implementing functions which deliver numerous statistics on demand, like averages, means, records and 
many more. 
Chunk of code that handles server side was taken from https://github.com/Erlendeikeland/csgo-gsi-python with certain tweaks. 
