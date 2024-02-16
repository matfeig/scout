from statsbombpy import sb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# set up credentials for StatsBomb API access
user="m.feigean@servettefc.ch" #replace between the quotation marks with the email address that you use to login to StatsBomb IQ
password="QzG3Kdlu" #replace between the quotation marks with the password that you use to login to StatsBomb IQ

comp=80 #statsbomb competition id
season=281 #statsbomb season id
team="Servette" #team name, as it appears in IQ
window=5 #rolling average window
team_color1="#870E26"
team_color2="black"

oppo_metrics=["player_match_passes","player_match_goals"] 

our_metrics=["player_match_np_xg","player_match_deep_progressions","player_match_obv_dribble_carry",
             "player_match_obv","player_match_obv_shot","player_match_obv_defensive_action",
             "player_match_passes_inside_box"] 

file_path="/Users/matfeig/Desktop/" 

matches = sb.matches(competition_id = comp, season_id = season, creds={"user": user, "passwd": password})
matches = matches[(matches['home_team'] == team)|(matches['away_team'] == team)]
matches=matches.sort_values(by=['match_date'])
matches=matches[matches["match_status"]=="available"]
list_matches=matches.match_id.tolist()

data = []
for n in list_matches:
      match_events=sb.player_match_stats(match_id=n, creds={"user": user, "passwd": password})
      teams=list(match_events.team_name.unique())
      match_events["opponent"]=np.where(match_events["team_name"]==team,teams[1],teams[0])
      data.append(match_events)
data=pd.concat(data)
data=data.reset_index(drop=True)

temp_df=data.drop_duplicates(subset=['match_id'])
temp_df.index.name = 'game_week'
temp_df=temp_df.reset_index()
temp_df=temp_df[["match_id","game_week"]]

data=pd.merge(data,temp_df, how="left",on=["match_id"])

kpi_values = {
    "player_match_passes": 399,
    "player_match_goals": 0.9,
    "player_match_np_xg":1.69,
    "player_match_deep_progressions":53,
    "player_match_obv_dribble_carry":0.93,
    "player_match_obv":2.54,
    "player_match_obv_shot":0.48,
    "player_match_obv_defensive_action":1.08,
    "player_match_passes_inside_box": 3.5
}

for metric in oppo_metrics:
    df=data.groupby(['game_week','team_name']).agg({metric: ['sum']})
    df.columns=df.columns.droplevel()
    df=df.reset_index()
    df=df[df["team_name"]!=team].reset_index(drop=True)
    
    avg = df["sum"].mean()
    kpi = kpi_values[metric]

    
    rolling = df["sum"].rolling(window).mean()
    
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_facecolor("white")
    
    bars = df.team_name
    x_pos = np.arange(len(df))
    
    ax.bar(x_pos, df["sum"],color=team_color1, alpha=0.75)    
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(bars, rotation=45)
    ax.plot(rolling, lw=2, color=team_color2, zorder=5,label=f"{window} match rolling average")
    ax.grid(True,axis='y',color="grey",lw=0.5)
    metric_label=metric.replace("player_","")
    metric_label=metric_label.replace("_"," ")
    ax.set(xlabel=f"{metric_label}")    
    ax.legend(loc="upper left")
    
    ax.axhline(y = avg, color = "grey", linestyle = 'dashed',lw=2,label="Avg")
    ax.axhline(y = kpi, color = "#870E26", linestyle = 'dashed',lw=2,label="kpi")
    
    fig.text(x=0.12, y=0.92, s=f"{team} Opposition trendline | {metric_label}", fontsize=22, fontweight='bold') 
    
    try:
        fig.savefig(f'{file_path}{metric}.png', dpi = 100, bbox_inches='tight')
    except:
        pass
        
for metric in our_metrics:
    df=data.groupby(['game_week','opponent']).agg({metric: ['sum']})
    df.columns=df.columns.droplevel()
    df=df.reset_index()
    df=df[df["opponent"]!=team].reset_index(drop=True)
        
    avg = df["sum"].mean()
    kpi = kpi_values[metric]
    
    rolling = df["sum"].rolling(window).mean()
    
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.set_facecolor("white")
    
    bars = df.opponent
    x_pos = np.arange(len(df))
    
    ax.bar(x_pos, df["sum"],color=team_color1, alpha=0.75)    
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(bars, rotation=45)
    ax.plot(rolling, lw=2, color=team_color2, zorder=5,label=f"{window} match rolling average")
    ax.grid(True,axis='y',color="grey",lw=0.5)
    metric_label=metric.replace("player_","")
    metric_label=metric_label.replace("_"," ")
    ax.set(xlabel=f"{metric_label}")    
    ax.legend(loc="upper left")
    
    ax.axhline(y = avg, color = "grey", linestyle = 'dashed',lw=2,label="Avg")
    ax.axhline(y = kpi, color = "#870E26", linestyle = 'dashed',lw=2,label="kpi")
    
    fig.text(x=0.1, y=0.95, s=f"{team} trendline | {metric_label}", fontsize=22, fontweight='bold') 
    
    try:
        fig.savefig(f'{file_path}{metric}.png', dpi = 100, bbox_inches='tight')
    except:
        pass
    
    
    
    