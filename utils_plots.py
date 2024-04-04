import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import plotly.graph_objects as go


def plot_np_xg(player_match_stats,player_name):
    selected = player_match_stats[player_match_stats.player_name==player_name].copy()
    selected['player_match_np_xg_per90'] = selected['player_match_minutes']*selected['player_match_np_xg']/90.0
    selected.sort_values(by='match_date', inplace=True)
    selected.reset_index(drop=True, inplace=True)

    # Calculate the moving average
    window = 5  
    selected['Moving_Avg'] = selected['player_match_np_xg_per90'].rolling(window=window).mean()

    # Trend line
    z = np.polyfit(selected.index, selected['player_match_np_xg_per90'], 1)
    p = np.poly1d(z)

    # Plotting with Plotly
    fig = go.Figure()

    # Moving Average
    fig.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg'], mode='lines+markers', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash',width=2),marker=dict(color='red', size=5, opacity=1)))
    
    # Trend Line
    fig.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines+markers', name='Trend', line=dict(color='green', dash='dot'),marker=dict(color='green', size=5, opacity=1)))

    # Update plot layout
    fig.update_layout(title=f'{player_name} Non-Penalty xG per 90mn Over Time with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='Non-Penalty xG per 90mn',
                    legend_title='Legend')

    return fig


def plot_xA(player_match_stats,player_name):
    ## Select player data
    selected = player_match_stats[player_match_stats.player_name==player_name].copy()
    selected['player_match_xa_per90'] = selected['player_match_minutes']*selected['player_match_xa']/90.0
    selected.sort_values(by='match_date', inplace=True)
    selected.reset_index(drop=True, inplace=True)
    selected.dropna(subset=['player_match_obv'], inplace=True)

    # Calculate the moving average
    window = 5  
    selected['Moving_Avg'] = selected['player_match_xa_per90'].rolling(window=window).mean()

    # Trend line
    z = np.polyfit(selected.index, selected['player_match_xa_per90'], 1)
    p = np.poly1d(z)

    # Plotting with Plotly
    fig = go.Figure()

    # Moving Average
    fig.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))

    # Trend Line
    fig.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))

    # Update plot layout
    fig.update_layout(title=f'{player_name} xA per 90mn Over Time with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='xA per 90mn',
                    legend_title='Legend')

    return fig


def plot_obv(player_match_stats,player_name):
    ## Select player data
    selected = player_match_stats[player_match_stats.player_name==player_name].copy()
    selected['player_match_obv_per90'] = selected['player_match_minutes']*selected['player_match_obv']/90.0
    selected.sort_values(by='match_date', inplace=True)
    selected.reset_index(drop=True, inplace=True)
    selected.dropna(subset=['player_match_obv'], inplace=True)

    # Calculate the moving average
    window = 5  
    selected['Moving_Avg'] = selected['player_match_obv_per90'].rolling(window=window).mean()

    # Trend line
    z = np.polyfit(selected.index, selected['player_match_obv_per90'], 1)
    p = np.poly1d(z)

    # Plotting with Plotly
    fig = go.Figure()

    # Moving Average
    fig.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))

    # Trend Line
    fig.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))

    # Update plot layout
    fig.update_layout(title=f'{player_name} obv per 90mn Over Time with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='obv per 90mn',
                    legend_title='Legend')

    return fig


def plot_xgChain(player_match_stats,player_name):
    ## Select player data
    selected = player_match_stats[player_match_stats.player_name==player_name].copy()
    selected['player_match_xgbuildup_per90'] = selected['player_match_minutes']*selected['player_match_xgbuildup']/90.0
    selected.sort_values(by='match_date', inplace=True)
    selected.reset_index(drop=True, inplace=True)
    selected.dropna(subset=['player_match_xgbuildup'], inplace=True)

    # Calculate the moving average
    window = 5  
    selected['Moving_Avg'] = selected['player_match_xgbuildup_per90'].rolling(window=window).mean()

    # Trend line
    z = np.polyfit(selected.index, selected['player_match_xgbuildup_per90'], 1)
    p = np.poly1d(z)

    # Plotting with Plotly
    fig = go.Figure()

    # Moving Average
    fig.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))

    # Trend Line
    fig.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))

    # Update plot layout
    fig.update_layout(title=f'{player_name} xgChain per 90mn: Build-up Over Time with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='xgChain',
                    legend_title='Legend')

    return fig


def prepare_data_for_index_mathieu(player_match_stats):

    player_stats_with_index = player_match_stats.copy()
    player_stats_with_index.columns = player_stats_with_index.columns.map(lambda x: x.removeprefix("player_match_"))

    ### OFFENSIVE INDEX
    player_stats_with_index['index'] = ((player_stats_with_index['np_shots']*4)+(player_stats_with_index['np_xg']*9)+(player_stats_with_index['xa']*8)+
                    (player_stats_with_index['op_key_passes']*4)+(player_stats_with_index['through_balls']*6)+(player_stats_with_index['op_passes_into_box']*6)+
                    player_stats_with_index['touches_inside_box']*5+(player_stats_with_index['dribbles']*4)+
                    (player_stats_with_index['forward_passes']*1)+(player_stats_with_index['op_f3_forward_passes']*5)+(player_stats_with_index['successful_crosses']*3)+
                    (player_stats_with_index['passes_inside_box']*3)+(player_stats_with_index['obv_pass']*8)+(player_stats_with_index['obv_shot']*8)+ (player_stats_with_index['deep_progressions']*7)+
                    (player_stats_with_index['obv_dribble_carry']*7)+(player_stats_with_index['np_psxg']*9)+(player_stats_with_index['dispossessions']*(-2))+
                    (player_stats_with_index['successful_long_balls']*4)+(player_stats_with_index['turnovers']*(-8))+(player_stats_with_index['touches']*0.5))

    ### DEFENSIVE INDEX
    player_stats_with_index['indexDef'] = ((player_stats_with_index['tackles']*6)+(player_stats_with_index['interceptions']*6)-(player_stats_with_index['dribbled_past']*(-6))+
                    (player_stats_with_index['shots_blocked']*4)+(player_stats_with_index['clearances']*4)+(player_stats_with_index['successful_aerials']*8)+(((player_stats_with_index['aerials'])-(player_stats_with_index['successful_aerials']))*(-7))+
                    (player_stats_with_index['aggressive_actions']*7)+(player_stats_with_index['pressure_regains']*9)+
                    (player_stats_with_index['pressures']*8)+(player_stats_with_index['pressure_duration_total']*6)+
                    (player_stats_with_index['counterpressures']*7)+(player_stats_with_index['pressured_action_fails']*(-3))+
                    (player_stats_with_index['counterpressured_action_fails']*(-2))+(player_stats_with_index['pressure_duration_total']*6)+
                    (player_stats_with_index['ball_recoveries']*8)+
                    (player_stats_with_index['fhalf_ball_recoveries']*5)+
                    (player_stats_with_index['obv_defensive_action']*7))


    player_stats_with_index['Index_G']= player_stats_with_index['index']+player_stats_with_index['indexDef']
    player_stats_with_index = player_stats_with_index[['player_name','index','Index_G','indexDef','match_id','minutes','match_date']].dropna()
    player_stats_with_index['index_General_p90'] = 90* player_stats_with_index['Index_G'] / player_stats_with_index['minutes']
    player_stats_with_index['index_Def_p90'] = 90* player_stats_with_index['indexDef'] / player_stats_with_index['minutes']
    player_stats_with_index['index_Off_p90'] = 90* player_stats_with_index['index'] / player_stats_with_index['minutes']

    return player_stats_with_index


def plot_index_Mathieu(player_match_stats,player_name):
    
    player_stats_with_index = prepare_data_for_index_mathieu(player_match_stats)
    ## Select player data
    selected = player_stats_with_index[player_stats_with_index.player_name==player_name].copy()
    selected.sort_values(by='match_date', inplace=True)
    selected.reset_index(drop=True, inplace=True)

    # Calculate the moving average
    window = 5  
    selected['Moving_Avg_General'] = selected['index_General_p90'].rolling(window=window).mean()
    selected['Moving_Avg_Off'] = selected['index_Off_p90'].rolling(window=window).mean()
    selected['Moving_Avg_Def'] = selected['index_Def_p90'].rolling(window=window).mean()

    #### GENERAL INDEX PLOT
    z = np.polyfit(selected.index, selected['index_General_p90'], 1)
    p = np.poly1d(z)
    fig_G = go.Figure()
    fig_G.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg_General'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))
    fig_G.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))
    fig_G.update_layout(title=f'{player_name} General Performance index with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='General Performance index',
                    legend_title='Legend')


    #### OFFENSIVE INDEX PLOT
    # Trend line
    z = np.polyfit(selected.index, selected['index_Off_p90'], 1)
    p = np.poly1d(z)
    fig_Off = go.Figure()
    fig_Off.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg_Off'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))
    fig_Off.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))
    fig_Off.update_layout(title=f'{player_name} Offensive Performance index with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='Offensive Performance index',
                    legend_title='Legend')
    
    #### DEFENSIVE INDEX PLOT
    # Trend line
    z = np.polyfit(selected.index, selected['index_Def_p90'], 1)
    p = np.poly1d(z)
    fig_Def = go.Figure()
    fig_Def.add_trace(go.Scatter(x=selected['match_date'], y=selected['Moving_Avg_Def'], mode='lines', name=f'{window}-game Moving Avg', line=dict(color='red', dash='dash')))
    fig_Def.add_trace(go.Scatter(x=selected['match_date'], y=p(selected.index), mode='lines', name='Trend', line=dict(color='green', dash='dot')))
    fig_Def.update_layout(title=f'{player_name} Defensive Performance index with Moving Average',
                    xaxis_title='Match Date',
                    yaxis_title='Defensive Performance index',
                    legend_title='Legend')
    
    return fig_G,fig_Off,fig_Def
