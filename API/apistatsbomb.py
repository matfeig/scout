#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 18:31:26 2022

@author: matfeig
"""
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC

class Statsbomb(ABC):
    def __init__(self, username=None, password=None):
        self.event_spec = ['id', 'index', 'period', 'timestamp', 'minute', 'second', 'type',
                           'possession', 'possession_team', 'play_pattern', 'team', 'player',
                           'position', 'location', 'duration', 'under_pressure', 'off_camera',
                           'out', 'related_events', 'tactics',
                           '50_50', 'bad_behaviour', 'ball_receipt', 'ball_recovery', 'block',
                           'carry', 'clearance', 'counterpress', 'dribble', 'duel', 'foul_committed',
                           'foul_won', 'goalkeeper', 'half_end', 'half_start', 'injury_stoppage',
                           'interception', 'miscontrol', 'pass', 'player_off', 'shot', 'substitution'
                          ]
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.open_url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/'
        self.api_url = 'https://data.statsbombservices.com/api/'
        
    def get_data(self, url):
        resp = requests.get(url=url, auth=self.auth)
        resp.raise_for_status()
        return resp.json()
        
    def flatten_event(self, data, match_id):
        related = []
        freeze = []
        tactics = []
        for row in data:    
            for key in list(row):
                if key not in self.event_spec:  # check matches event spec
                    raise AssertionError(f'{key} not in the StatsBomb event specification version 4.0')
                if isinstance(row[key], dict):  # unpack nested columns
                    for nested_key in list(row[key]):
                        nested_value = row[key][nested_key]

                        if nested_key == 'end_location':
                            if len(nested_value) == 2:
                                row['end_x'], row['end_y'] = nested_value
                            elif len(nested_value) == 3:
                                row['end_x'], row['end_y'], row['end_z'] = nested_value
                            else:
                                msg = 'end_location length not equal to 2 (x, y) or 3 (x, y, z)'
                                raise AssertionError(msg)

                        elif nested_key == 'aerial_won':
                            row[f'{nested_key}'] = nested_value

                        elif nested_key in ['outcome', 'body_part', 'technique', 'aerial_won']:
                            for k in nested_value:
                                row[f'{nested_key}_{k}'] = nested_value[k]

                        elif nested_key == 'type':
                            for k in nested_value:
                                row[f'sub_{nested_key}_{k}'] = nested_value[k]

                        elif nested_key not in ['freeze_frame', 'lineup']:
                            if isinstance(nested_value, dict):
                                for k in nested_value:
                                    row[f'{key}_{nested_key}_{k}'] = nested_value[k]
                            else:
                                row[f'{key}_{nested_key}'] = nested_value

                        elif nested_key == 'freeze_frame':
                            freeze.append(self.flatten_freeze(nested_value, match_id, row['id']))

                        else:
                            tactics.append(self.flatten_tactics(nested_value, match_id, row['id']))

                    del row[key]

            # unpack the timestamp
            if 'timestamp' in row:
                parsed_date = datetime.strptime(row['timestamp'], "%H:%M:%S.%f")
                row['timestamp_minute'] = parsed_date.minute
                row['timestamp_second'] = parsed_date.second
                row['timestamp_millisecond'] = int(parsed_date.microsecond / 1000)
                del row['timestamp']

            # unpack the location column
            if 'location' in row:
                if len(row['location']) == 2:
                    row['x'], row['y'] = row['location']
                else:
                    raise AssertionError('location length not equal to 2 (x, y)')
                del row['location']

            # remove related_events
            if 'related_events' in row:
                related.append({'id': row['id'],
                                'index': row['index'],
                                'type_name': row['type_name'],
                                'id_related': row['related_events']})
                del row['related_events']

        freeze = pd.concat(freeze).reset_index(drop=True)
        tactics = pd.concat(tactics).reset_index(drop=True)

        return data, related, freeze, tactics
    
    def flatten_freeze(self, data, match_id, event_id):
        for row in data:
            for key in list(row):
                value = row[key]
                if key == 'location':
                    row['x'], row['y'] = value
                    del row['location']
                elif key in ['player', 'position']:
                    for nested_key in value:
                        row[f'{key}_{nested_key}'] = value[nested_key]
                    del row[key]
        df = self.clean_freeze_tactics(data, match_id, event_id, key='event_freeze_id')
        return df
    
    def flatten_tactics(self, data, match_id, event_id):
        for row in data:
            for key in list(row):
                if key in ['player', 'position']:
                    value = row[key]
                    for nested_key in value:
                        row[f'{key}_{nested_key}'] = value[nested_key]
                    del row[key]
        df = self.clean_freeze_tactics(data, match_id, event_id, key='event_tactics_id')    
        return df

    def flatten_lineups(self, data):
        all_players = []
        for row in data:
            for player in row['lineup']:
                player['team_id'] = row['team_id']
                player['team_name'] = row['team_name']
                player['country_id'] = player['country']['id']
                player['country_name'] = player['country']['name']
                if player['player_nickname'] is None:
                    player['player_nickname'] = player['player_name']
                all_players.append(player)
                del player['country']
                del player['positions']  # if flattened would be multiple lines
                del player['cards']  # if flattened would be multiple lines
        return pd.DataFrame(all_players)
    
    def flatten_match(self, data):
        for row in data:
            for key in list(row):
                value = row[key]
                if isinstance(value, dict):
                    for nested_key in list(value):
                        nested_value = value[nested_key]
                        if isinstance(nested_value, list):
                            nested_value = nested_value[0]
                        if isinstance(nested_value, dict):
                            for k in list(nested_value):
                                if k in ['country', 'managers']:
                                    for sub_key in nested_value[k]:
                                        row[f'{key}_{nested_key}_{k}_{sub_key}'] = nested_value[k][sub_key]
                                else:
                                    row[f'{key}_{nested_key}_{k}'] = nested_value[k]
                        elif key in ['competition_stage', 'stadium', 'referee']:
                            row[f'{key}_{nested_key}'] = nested_value
                        elif nested_key == 'country_name':
                            row[f'{key}_{nested_key}'] = nested_value
                        elif key == 'metadata':
                            row[f'{key}_{nested_key}'] = nested_value
                        else:
                            row[nested_key] = nested_value
                    del row[key]
        return pd.DataFrame(data)
    
    def clean_freeze_tactics(self, data, match_id, event_id, key):
        df = pd.DataFrame(data)
        df['match_id'] = match_id
        df['id'] = event_id
        df.index.name = key
        df.reset_index(inplace=True)
        df[key] = df[key] + 1
        return df

    def clean_event(self, data, match_id):
        df = pd.DataFrame(data)
        df['match_id'] = match_id

        # sorting data by time and possession
        df.sort_values(['minute', 'second', 'timestamp_minute',
                        'timestamp_second', 'timestamp_millisecond', 'possession'], inplace=True)
        df.reset_index(inplace=True, drop=True)

        # there are a few errors with through ball not always being marked in the technique name
        if 'pass_through_ball' in df.columns:
            df.loc[df.pass_through_ball.notnull(), 'technique_name'] = 'Through Ball'

        # drop cols that are covered by other columns
        # (e.g. pass technique covers through, ball, inswinging etc.)
        cols_to_drop = ['pass_through_ball', 'pass_outswinging', 'pass_inswinging',  'clearance_head',
                        'clearance_left_foot', 'clearance_right_foot', 'pass_straight',
                        'clearance_other', 'goalkeeper_punched_out',
                        'goalkeeper_shot_saved_off_target', 'shot_saved_off_target',
                        'goalkeeper_shot_saved_to_post', 'shot_saved_to_post', 'goalkeeper_lost_out',
                        'goalkeeper_lost_in_play',  'goalkeeper_success_out',
                        'goalkeeper_success_in_play', 'goalkeeper_saved_to_post',
                        'shot_kick_off', 'goalkeeper_penalty_saved_to_post']
        df.drop(cols_to_drop, axis=1, errors='ignore', inplace=True)

        # replace weird * character in the type_name for ball receipt
        df['type_name'] = df['type_name'].replace({'Ball Receipt*': 'Ball Receipt'})

        # amend dtypes
        for col in ['counterpress', 'under_pressure', 'off_camera', 'out']:
            if col in df.columns:
                df[col] = df[col].astype(float)

        return df

    def clean_related(self, related, df, match_id):
        df_related = pd.DataFrame(related)
        # replace weird * character in the type_name for ball receipt
        df_related['type_name'] = df_related['type_name'].replace({'Ball Receipt*': 'Ball Receipt'})
        df_related = df_related.explode('id_related')
        cols = ['id', 'index', 'type_name']
        df_related = df_related.merge(df[cols].rename({'id': 'id_related'}, axis='columns'),
                                      how='left', on='id_related', validate='m:1',
                                      suffixes=['', '_related'])
        df_related['match_id'] = match_id
        df_carry = df_related[df_related.type_name == 'Carry'].copy()
        df_carry.rename({'id': 'id_related',
                         'index': 'index_related',
                         'type_name': 'type_name_related',
                         'id_related': 'id',
                         'index_related': 'index',
                         'type_name_related': 'type_name'},
                        axis='columns', inplace=True)
        df_related = pd.concat([df_related, df_carry]).drop_duplicates()
        return df_related
    
class StatsbombOpen(Statsbomb):
    def competitions(self):
        url = f'{self.open_url}competitions.json'
        data = self.get_data(url)
        df = pd.DataFrame(data)
        date_cols = ['match_available', 'match_available_360', 'match_updated']
        df[date_cols] = df[date_cols].astype(np.datetime64)
        return df
    
    def matches(self, competition, season):
        url = f'{self.open_url}matches/{competition}/{season}.json'
        data = self.get_data(url)
        df = self.flatten_match(data)
        df['kick_off'] = pd.to_datetime(df.match_date + ' ' + df.kick_off)
        date_cols = ['match_date', 'last_updated', 'last_updated_360',
                     'home_team_managers_dob', 'away_team_managers_dob']
        for date in date_cols:
            df[date] = pd.to_datetime(df[date])
        return df
    
    def lineups(self, match):
        url = f'{self.open_url}/lineups/{match}.json'
        data = self.get_data(url)   
        return self.flatten_lineups(data)
    
    def events(self, match):
        url = f'{self.open_url}events/{match}.json'
        data = self.get_data(url)   
        data, related, df_freeze, df_tactics = self.flatten_event(data, match)
        df = self.clean_event(data, match)
        df_related = self.clean_related(related, df, match)

        df_dict = {'events': df,
                   'related_events': df_related,
                   'shot_freeze_frames': df_freeze,
                   'tactics_lineups': df_tactics}

        return df_dict
    
class StatsbombApi(Statsbomb):
    def competitions(self, version=4):
        url = f'https://data.statsbombservices.com/api/v{version}/competitions'
        data = self.get_data(url)
        df = pd.DataFrame(data)
        date_cols = ['match_available', 'match_available_360', 'match_updated']
        df[date_cols] = df[date_cols].astype(np.datetime64)
        return df
    
    def matches(self, competition, season, version=5):
        url = (f'https://data.statsbombservices.com/api/v{version}/'
               f'competitions/{competition}/seasons/{season}/matches')
        data = self.get_data(url)
        df = self.flatten_match(data)
        df['kick_off'] = pd.to_datetime(df.match_date + ' ' + df.kick_off)
        date_cols = ['match_date', 'last_updated', 'last_updated_360',
                     'home_team_managers_dob', 'away_team_managers_dob']
        for date in date_cols:
            df[date] = pd.to_datetime(df[date])
        return df
    
    def lineups(self, match, version=2):
        url = f'https://data.statsbombservices.com/api/v{version}/lineups/{match}'
        data = self.get_data(url)   
        return self.flatten_lineups(data)
    
    def events(self, match, version=6):
        url = f'https://data.statsbombservices.com/api/v{version}/events/{match}'
        data = self.get_data(url)   
        data, related, df_freeze, df_tactics = self.flatten_event(data, match)
        df = self.clean_event(data, match)
        df_related = self.clean_related(related, df, match)

        df_dict = {'events': df,
                   'related_events': df_related,
                   'shot_freeze_frames': df_freeze,
                   'tactics_lineups': df_tactics}

        return df_dict
    
    ### Test it ## 
    
s = StatsbombApi(username=m.feigean@servettefc.ch", password="QzG3Kdlu")

    
events_dict = s.events(3764741, version=3)
events_dict.keys()
events_dict['events'].head(2)
events_dict['related_events'].head(2)
events_dict['shot_freeze_frames'].head(2)
events_dict['tactics_lineups'].head(2)
df_competition = s.competitions()
df_competition.head(2)
df_lineup = s.lineups(3764741)
df_lineup.head(2)
df = s.matches(competition=80, season=90)
df.head(2)

















