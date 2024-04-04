import streamlit as st
from statsbombpy import sb
import plotly.graph_objs as go
import pandas as pd
from stqdm import stqdm

from utils_plots import *
# Placeholder functions for StatsBomb API interactions
def authenticate_with_statsbomb(username, password):
    # Simulate authentication; replace with real logic
    if username == "admin" and password == "password":
        return {"user": 'm.feigean@servettefc.ch', "passwd": 'QzG3Kdlu'}
    return None


@st.cache_data
def get_competitions(creds):
    # Using sb.competitions() directly for simplicity; add error handling as needed
    return sb.competitions(creds=creds)

@st.cache_data
def get_teams(competition_id,creds):
    # This is a simplified approach; consider caching results for efficiency
    competitions = get_competitions(creds)
    seasons = competitions[competitions['competition_id'] == competition_id].season_id.unique()
    teams = set()
    for season_id in seasons:
        matches = sb.matches(competition_id, season_id,creds=creds)
        teams.update(matches['home_team'].unique())
        teams.update(matches['away_team'].unique())
    return list(teams)

@st.cache_data
def get_seasons(competition_id,creds):
    competitions = get_competitions(creds=creds)
    season_values = competitions[competitions['competition_id'] == competition_id][['season_name','season_id']].values
    dictionary_season_values = {}
    for k,v in season_values:
        dictionary_season_values[k]=v
    return dictionary_season_values


selected_columns_from_matchesdf = [
    'match_id', 'match_date', 'season',
       'home_team', 'away_team', 'home_score', 'away_score', 'match_week',
]

@st.cache_data
def get_games(selected_team,competition_id,seasons,creds):
    games = []
    for season_id in seasons:
        try:
            matches = sb.matches(competition_id=competition_id,season_id=season_id,creds=creds)
            matches = matches[((matches['home_team']==selected_team) | (matches['away_team']==selected_team))].copy().reset_index(drop=True)
            matches = matches[selected_columns_from_matchesdf].copy()
            games.append(matches)
        except:
            continue;
    return pd.concat(games)

@st.cache_data
def get_player_match_stats(matches,selected_team,creds):
    player_matches_stats = []
    for match_id in stqdm(matches.match_id.unique()):
        season = matches[matches.match_id==match_id].season.values[0]
        match_date = matches[matches.match_id==match_id].match_date.values[0]
        try:
            player_match = sb.player_match_stats(match_id,creds=creds)
            player_match = player_match[player_match.team_name==selected_team].copy().reset_index(drop=True)
            player_match['season'] = season
            player_match['match_date'] = match_date
            player_matches_stats.append(player_match)
        except:
            continue;
    
    player_matches_stats = pd.concat(player_matches_stats).reset_index(drop=True)
    return player_matches_stats


# Placeholder function for player details
def show_player_plots(player_match_stats,player_name):
    st.write(f"Plots for {player_name} would be here.")
    np_xg_fig = plot_np_xg(player_match_stats,player_name)
    st.plotly_chart(np_xg_fig, use_container_width=True)

def main():
    # Initialize session state variables if not already set
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None

    st.title("Soccer Analytics Tool")

    # Handle login
    if st.session_state.page == 'login':
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button('Login'):
            session_token = authenticate_with_statsbomb(username, password)
            if session_token:
                st.session_state.session_token = session_token
                st.session_state.page = 'home'
                st.rerun()  # Rerun the app after login
            else:
                st.error('Failed to log in. Please check your credentials.')

    # After successful login, display the home page
    elif st.session_state.page == 'home' and st.session_state.session_token:
        # Competition selection and the rest of the home page logic
        creds = st.session_state.session_token
        competitions = get_competitions(creds)
        selected_competition = st.selectbox("Select Competition", competitions['competition_name'].unique())

        if selected_competition:
            selected_competition_id = competitions[competitions['competition_name'] == selected_competition].iloc[0]['competition_id']
            
            # Team and season selection logic
            teams = get_teams(selected_competition_id, creds)
            selected_team = st.selectbox("Select Team", teams)

            seasons_dict = get_seasons(selected_competition_id, creds)
            seasons = list(seasons_dict.keys())
            selected_seasons = st.multiselect("Select Seasons", seasons, default=seasons)
            
            selected_seasons_ids = [seasons_dict[s] for s in selected_seasons]

            if st.button("Fetch data"):
                games = get_games(selected_team, selected_competition_id, selected_seasons_ids, creds)
                player_match_stats = get_player_match_stats(games, selected_team, creds)
                st.session_state['player_match_stats'] = player_match_stats  # Store in session state
                players = player_match_stats.player_name.unique()
                st.session_state['players'] = players  # Store in session state

            # Use session state to maintain player list and selection
            if 'players' in st.session_state:
                selected_player = st.selectbox("Select Player", st.session_state['players'], key='selected_player')
                if selected_player and 'player_match_stats' in st.session_state:
                    player_match_stats = st.session_state['player_match_stats']
                    if st.button(f"Show plots for {selected_player}"):
                        ## plot np xg
                        np_xg_fig = plot_np_xg(player_match_stats, selected_player)
                        st.plotly_chart(np_xg_fig, use_container_width=True)

                        ## plot xA
                        xA_fig = plot_xA(player_match_stats,selected_player)
                        st.plotly_chart(xA_fig, use_container_width=True)

                        ## plot obv
                        obv_fig = plot_obv(player_match_stats, selected_player)
                        st.plotly_chart(obv_fig, use_container_width=True)

                        ## xGChain plot
                        xgc_fig = plot_xgChain(player_match_stats,selected_player)
                        st.plotly_chart(xgc_fig, use_container_width=True)

                        ## Mathieu Index plot
                        general_index_fig, offensive_index_fig, defensive_index_fig = plot_index_Mathieu(player_match_stats,selected_player)   
                        st.plotly_chart(general_index_fig, use_container_width=True)
                        st.plotly_chart(offensive_index_fig, use_container_width=True)
                        st.plotly_chart(defensive_index_fig, use_container_width=True)


if __name__ == "__main__":
    main()
