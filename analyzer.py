from demoparser2 import DemoParser
import pandas as pd

MY_STEAMID = 76561199014748443

def run_analysis(file_path):
    parser = DemoParser(file_path)
    
    df_deaths = parser.parse_event("player_death", player=["last_place_name"])
    df_deaths["pfeil"] = " ---->"
    my_kills_df = df_deaths[df_deaths["attacker_steamid"].astype(str) == str(MY_STEAMID)].copy()
    kill_list = my_kills_df[["attacker_name","pfeil","user_name","user_last_place_name","attacker_last_place_name","weapon"]].reset_index(drop=True)
    tot_kill_list = df_deaths[["attacker_name","pfeil","user_name","user_last_place_name","attacker_last_place_name","weapon"]].reset_index(drop=True)
    max_tick = parser.parse_event("round_end")["tick"].max()
    wanted_fields = ["kills_total", "deaths_total", "mvps", "headshot_kills_total", "utility_damage_total"]
    df_score = parser.parse_ticks(wanted_fields, ticks=[max_tick])
    
#own stats
    my_row = df_score[df_score["steamid"].astype(str) == str(MY_STEAMID)]
    my_stats = my_row.iloc[0].to_dict() if not my_row.empty else {}
#teams
    df_players = parser.parse_player_info()
    team_t = df_players[df_players.team_number == 2][["name", "steamid"]].to_dict(orient='records')
    team_ct = df_players[df_players.team_number == 3][["name", "steamid"]].to_dict(orient='records')

#final pack
    return {
        "kills": kill_list.to_dict(orient='records'),
        "personal": {
            "kills": int(my_stats.get("kills_total", 0)),
            "deaths": int(my_stats.get("deaths_total", 0)),
            "hs": int(my_stats.get("headshot_kills_total", 0)),
            "mvp": int(my_stats.get("mvps", 0)),
            "util": int(my_stats.get("utility_damage_total", 0)),
            "analyzed": 1 if my_stats.get("kills_total") else 0
        },
        "space" : {
            "tot_kills": tot_kill_list.to_dict(orient='records')
        },

        
        "teams": {
            "T": team_t,
            "CT": team_ct
        },
        "filename": file_path.split("/")[-1]
    }