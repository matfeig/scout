#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 11:39:53 2021

@author: matfeig
"""

import tqdm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from matplotlib.collections import LineCollection
import pandas as pd
from mplsoccer.pitch import Pitch, add_image
from mplsoccer.statsbomb import read_event, EVENT_SLUG
import PIL
from urllib.request import urlopen
from statsbombpy import sb
from statsbombpy import api_client
from statsbombpy import config
import requests as req
import os
import warnings

#I had to copy some functions that were giving me problems
# so...    *********************START OF CRAP**************************************

def get_resource(url: str, creds: dict) -> list:
    auth = req.auth.HTTPBasicAuth(creds["user"], creds["passwd"])
    resp = req.get(url, auth=auth)
    if resp.status_code != 200:
        print(f"{url} -> {resp.status_code}")
        resp = []
    else:
        resp = resp.json()
    return resp

def read_event(path_or_buf, related_event_df=True, shot_freeze_frame_df=True, tactics_lineup_df=True, warn=True):
    """ Extracts individual event json and loads as a dictionary of up to
    four pandas.DataFrame: 'event', 'related event', 'shot_freeze_frame', and 'tactics_lineup'.
    
    Parameters
        ----------
        path_or_buf : a valid JSON str, path object or file-like object
            Any valid string path is acceptable. The string could be a URL. Valid
            URL schemes include http, ftp, s3, and file. For file URLs, a host is
            expected. A local file could be:
            ``file://localhost/path/to/table.json``.
            If you want to pass in a path object, pandas accepts any
            ``os.PathLike``.
            By file-like object, we refer to objects with a ``read()`` method,
            such as a file handler (e.g. via builtin ``open`` function)
            or ``StringIO``.
            
        related_event_df : bool, default True
            Whether to return a 'related_event' Dataframe in the returned dictionary.   
        
        shot_freeze_frame_df : bool, default True
            Whether to return a 'shot_freeze_frame' in the returned dictionary.   
        
        tactics_lineup_df : bool, default True
            Whether to return a 'tactics_lineup' Dataframe in the returned dictionary.

        warn : bool, default True
            Whether to warn about Statsbomb's data license agreement.
            
        Returns
        -------
        Dict of up to 4 pandas.DataFrame.
            Dict keys: 'event', 'related_event', 'shot_freeze_frame', 'tactics_lineup'.


        Examples
        --------
        # read from path - note change path to navigate to open-data folder
        from mplsoccer.statsbomb import read_event
        import os
        PATH_TO_EDIT = os.path.join('open-data','data','events','7430.json')
        dict_dfs = read_event(PATH_TO_EDIT)

        # read from url
        from mplsoccer.statsbomb import read_event, EVENT_SLUG
        import os
        URL = os.path.join(EVENT_SLUG,'7430.json')
        dict_dfs = read_event(URL)
    """
    if warn:
        warnings.warn(statsbomb_warning)
        
    df_dict = {}
    
    # read as dataframe
    df = pd.read_json(path_or_buf, encoding='utf-8')
    if df.empty:
        print(f'Skipping {path_or_buf}: empty json')
        return
    
    # timestamp defaults to today's date so store as integers in seperate columns
    df['timestamp_minute'] = df.timestamp.dt.minute
    df['timestamp_second'] = df.timestamp.dt.second
    df['timestamp_millisecond'] = (df.timestamp.dt.microsecond/1000).astype(np.int64)
    df.drop('timestamp', axis=1, inplace=True)
    
    # get match id and add to the event dataframe
    match_id = int(os.path.basename(path_or_buf)[:-5])
    df['match_id'] = match_id
    
    # loop through the columns that are still dictionary columns and add them as separate cols to the dataframe
    # these are nested dataframes in the docs - although dribbled_past/ pressure isn't needed here?
    # also some others are needed: type, possession_team, play_pattern, team, tactics, player, position
    dictionary_columns = ['pass', '50_50', 'bad_behaviour', 'ball_receipt', 'ball_recovery', 'block', 'carry',
                          'clearance', 'dribble', 'duel', 'foul_committed', 'foul_won', 'goalkeeper',
                          'half_end', 'half_start', 'injury_stoppage', 'interception',
                          'miscontrol', 'play_pattern', 'player', 'player_off', 'position',
                          'possession_team', 'shot', 'substitution', 'tactics', 'team', 'type']
    for col in dictionary_columns:
        if col in df.columns:
            df = _split_dict_col(df, col)
    
    # sort by time and reset index
    df.sort_values(['minute', 'second', 'timestamp_minute',
                    'timestamp_second', 'timestamp_millisecond', 'possession'], inplace=True)
    df.reset_index(inplace=True, drop=True)
    
    # split location info to x, y and (z for shot) columns and drop old columns
    _split_location_cols(df, 'location', ['x', 'y', 'z'])
    _split_location_cols(df, 'pass_end_location', ['pass_end_x', 'pass_end_y'])
    _split_location_cols(df, 'carry_end_location', ['carry_end_x', 'carry_end_y'])
    _split_location_cols(df, 'shot_end_location', ['shot_end_x', 'shot_end_y', 'shot_end_z'])
    _split_location_cols(df, 'goalkeeper_end_location', ['goalkeeper_end_x', 'goalkeeper_end_y'])
    
    # replace weird * character in the type_name for ball receipt
    df['type_name'] = df['type_name'].replace({'Ball Receipt*': 'Ball Receipt'})
    
    # because some columns were contained in dictionaries they have been split into separate columns
    # with different prefixes, e.g. clearance_aerial_won, pass_aerial_won, shot_aerial_won
    # this combines them into one column and drops the original columns
    df = _simplify_cols_and_drop(df, 'outcome_id')
    df = _simplify_cols_and_drop(df, 'outcome_name')
    df = _simplify_cols_and_drop(df, 'body_part_id')
    df = _simplify_cols_and_drop(df, 'body_part_name')
    df = _simplify_cols_and_drop(df, 'aerial_won')
    df = _simplify_cols_and_drop(df, 'end_x', ['pass_end_x', 'carry_end_x', 'shot_end_x', 'goalkeeper_end_x'])    
    df = _simplify_cols_and_drop(df, 'end_y', ['pass_end_y', 'carry_end_y', 'shot_end_y', 'goalkeeper_end_y'])
    df = _simplify_cols_and_drop(df, 'sub_type_id', ['pass_type_id', 'duel_type_id',
                                                     'goalkeeper_type_id', 'shot_type_id'])
    df = _simplify_cols_and_drop(df, 'sub_type_name', ['pass_type_name', 'duel_type_name',
                                                       'goalkeeper_type_name', 'shot_type_name'])
    # technique id/names are not always present so have to take this into account
    technique_id_cols = ['pass_technique_id', 'goalkeeper_technique_id', 'shot_technique_id']
    technique_id_cols = set(technique_id_cols).intersection(set(df.columns))
    technique_name_cols = ['pass_technique_name', 'goalkeeper_technique_name', 'shot_technique_name']
    technique_name_cols = set(technique_name_cols).intersection(set(df.columns))
    df = _simplify_cols_and_drop(df, 'technique_id', technique_id_cols)
    df = _simplify_cols_and_drop(df, 'technique_name', technique_name_cols)
    
    # create a related events dataframe
    if related_event_df:
        df_related_event = _list_dictionary_to_df(df, col='related_events',
                                                  value_name='related_event', var_name='event_related_id')
        # some carries don't have the corresponding events. This makes sure all events are linked both ways
        df_related_event.drop('event_related_id', axis=1, inplace=True)
        df_related_event_reverse = df_related_event.rename({'related_event': 'id', 'id': 'related_event'}, axis=1)
        df_related_event = pd.concat([df_related_event, df_related_event_reverse], sort=False)
        df_related_event.drop_duplicates(inplace=True)
        # and add on the type_names, index for easier lookups of how the events are related
        df_event_type = df[['id', 'type_name', 'index']].copy()
        df_related_event = df_related_event.merge(df_event_type, on='id', how='left', validate='m:1')
        df_event_type.rename({'id': 'related_event'}, axis=1, inplace=True)
        df_related_event = df_related_event.merge(df_event_type, on='related_event',
                                                  how='left', validate='m:1', suffixes=['', '_related'])
        df_related_event.rename({'related_event': 'id_related'}, axis=1, inplace=True)
        # add on match_id and add to dictionary
        df_related_event['match_id'] = match_id
        df_dict['related_event'] = df_related_event
    
    # create a shot freeze frame dataframe - also splits dictionary of player details into columns
    if shot_freeze_frame_df:
        df_shot_freeze = _list_dictionary_to_df(df, col='shot_freeze_frame',
                                                value_name='player', var_name='event_freeze_id')
        df_shot_freeze = _split_dict_col(df_shot_freeze, 'player')
        _split_location_cols(df_shot_freeze, 'player_location', ['x', 'y'])
        # add on match_id and add to dictionary
        df_shot_freeze['match_id'] = match_id
        df_dict['shot_freeze_frame'] = df_shot_freeze

    # create a tactics lineup frame dataframe - also splits dictionary of player details into columns
    if tactics_lineup_df:
        df_tactic_lineup = _list_dictionary_to_df(df, col='tactics_lineup',
                                                  value_name='player', var_name='event_tactics_id')
        df_tactic_lineup = _split_dict_col(df_tactic_lineup, 'player')
        # add on match_id and add to dictionary
        df_tactic_lineup['match_id'] = match_id
        df_dict['tactics_lineup'] = df_tactic_lineup
    
    # drop columns stored as a separate table
    df.drop(['related_events', 'shot_freeze_frame', 'tactics_lineup'], axis=1, inplace=True)
    
    # there are a few errors with through ball not always being marked in the technique name
    if 'pass_through_ball' in df.columns:
        df.loc[df.pass_through_ball.notnull(), 'technique_name'] = 'Through Ball'
    
    # drop cols that are covered by other columns (e.g. pass technique covers through, ball, inswinging etc.)
    cols_to_drop = ['pass_through_ball', 'pass_outswinging', 'pass_inswinging',  'clearance_head',
                    'clearance_left_foot', 'clearance_right_foot', 'pass_straight', 'clearance_other',
                    'goalkeeper_punched_out',  'goalkeeper_shot_saved_off_target', 'shot_saved_off_target',
                    'goalkeeper_shot_saved_to_post', 'shot_saved_to_post', 'goalkeeper_lost_out',
                    'goalkeeper_lost_in_play',  'goalkeeper_success_out', 'goalkeeper_success_in_play',
                    'goalkeeper_saved_to_post', 'shot_kick_off', 'goalkeeper_penalty_saved_to_post']
    df.drop(cols_to_drop, axis=1, errors='ignore', inplace=True)
    
    # rename end location
    df.rename({'shot_end_z': 'end_z'}, axis=1, inplace=True)
           
    # reorder columns so some of the most used ones are first
    cols = ['match_id', 'id', 'index', 'period', 'timestamp_minute', 'timestamp_second', 
            'timestamp_millisecond', 'minute', 'second', 'type_id', 'type_name', 'sub_type_id',
            'sub_type_name',  'outcome_id', 'outcome_name', 'play_pattern_id', 'play_pattern_name',
            'possession_team_id', 'possession',  'possession_team_name', 'team_id', 'team_name',
            'player_id', 'player_name', 'position_id',
            'position_name', 'duration', 'x', 'y', 'z', 'end_x', 'end_y', 'end_z',
            'body_part_id', 'body_part_name', 'technique_id', 'technique_name']  
    other_cols = df.columns[~df.columns.isin(cols)]
    cols.extend(other_cols)
    df = df[cols].copy()
    
    # add to dictionary
    df_dict['event'] = df
    
    return df_dict
#   ***********************************************************************************************
#         *********************************** END OF CRAP *************************************

#The API can be accessed by making a request to 
#https://data.statsbombservices.com/api/v3/competitions/?/seasons/?/matches.
#The question marks should be replaced with the competition and season IDs.


creds = {"user":"m.feigean@servettefc.ch", "passwd":"QzG3Kdlu"}
matches = sb.matches(competition_id=80, season_id=90, creds=creds)
match_files = [str(match)+'.json' for match in matches['match_id']]

#********************* NEW STUFF *********************
match = [str(match) for match in matches['match_id']]
#matches = sb.matches(competition_id=11, season_id=42)
#match_files = [str(match)+'.json' for match in matches['match_id']]

#I try with only first event
URL="https://data.statsbombservices.com/api/v5/events/3774885"
df=pd.DataFrame(get_resource(URL,creds))
#Now df is downloaded, the problem is that some column contains dictionaries and the path are different from
#the ones used in the code below
#for example column type has a dict with id,name. later is referred as type_name
df['type'].apply(pd.Series)
cd=pd.concat([df.drop(['type'],axis=1), df['type'].apply(pd.Series)],axis=1)
df=cd




#THIS IS CODE TO DOWNLOAD ALL EVENTS, it works but i had to check the reset_index part
#df = pd.DataFrame()
#for i in match:
#    URL="https://data.statsbombservices.com/api/v5/events/{}".format(i)
#    print(URL)
#    print(URL)
#    df=df.append(pd.DataFrame(get_resource(URL,creds)))
#    df.reset_index()
#
#df['type']


#SOME TRASH/NOTES

#URL="{HOSTNAME}/api/{VERSIONS['events']}/events/{match_id}"
#event_json=get_resource(URL,creds)
#read_event(event_json)
#we'll use mplsoccer to organise the data from each match file into a single dataframe
#kwargs = {'related_event_df': False, 'shot_freeze_frame_df': False, 'tactics_lineup_df': False, 'warn': False}
#df = pd.concat([read_event(f'{EVENT_SLUG}/{file}', **kwargs)['event'] for file in match_files])
#cc = pd.DataFrame(get_resource(URL,creds))
#df=df.append(cc)
#df = pd.concat([read_event((f'{https://data.statsbombservices.com/api/v3/events/{file}', **kwargs)['event'] for file in match_files]),creds)
#df = pd.concat([read_event(get_resource('https://data.statsbombservices.com/api/v3/competitions/80/seasons/90/matches/{}'.format(match_files[0]), creds))])
#x = read_event(event_json)

class Streamlines(object):
    """
    Copyright (c) 2011 Raymond Speth.
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
    See: http://web.mit.edu/speth/Public/streamlines.py
    """

    def __init__(self, X, Y, U, V, res=0.125,
                 spacing=1, maxLen=2500, detectLoops=False):
        """
        Compute a set of streamlines covering the given velocity field.
        X and Y - 1D or 2D (e.g. generated by np.meshgrid) arrays of the
                  grid points. The mesh spacing is assumed to be uniform
                  in each dimension.
        U and V - 2D arrays of the velocity field.
        res - Sets the distance between successive points in each
              streamline (same units as X and Y)
        spacing - Sets the minimum density of streamlines, in grid points.
        maxLen - The maximum length of an individual streamline segment.
        detectLoops - Determines whether an attempt is made to stop extending
                      a given streamline before reaching maxLen points if
                      it forms a closed loop or reaches a velocity node.
        Plots are generated with the 'plot' or 'plotArrows' methods.
        """

        self.spacing = spacing
        self.detectLoops = detectLoops
        self.maxLen = maxLen
        self.res = res

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        self.x = xa if xa.ndim == 1 else xa[0]
        self.y = ya if ya.ndim == 1 else ya[:,0]
        self.u = U
        self.v = V
        self.dx = (self.x[-1]-self.x[0])/(self.x.size-1) # assume a regular grid
        self.dy = (self.y[-1]-self.y[0])/(self.y.size-1) # assume a regular grid
        self.dr = self.res * np.sqrt(self.dx * self.dy)

        # marker for which regions have contours
        self.used = np.zeros(self.u.shape, dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:,0] = True
        self.used[:,-1] = True

        # Don't try to compute streamlines in regions where there is no velocity data
        for i in range(self.x.size):
            for j in range(self.y.size):
                if self.u[j,i] == 0.0 and self.v[j,i] == 0.0:
                    self.used[j,i] = True

        # Make the streamlines
        self.streamlines = []
        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            self.streamlines.append(self._makeStreamline(self.x[nz[0][1]],
                                                         self.y[nz[0][0]]))


    def _interp(self, x, y):
        """ Compute the velocity at point (x,y) """
        i = (x-self.x[0])/self.dx
        ai = i % 1

        j = (y-self.y[0])/self.dy
        aj = j % 1

        i, j = int(i), int(j)
        
        # Bilinear interpolation
        u = (self.u[j,i]*(1-ai)*(1-aj) +
             self.u[j,i+1]*ai*(1-aj) +
             self.u[j+1,i]*(1-ai)*aj +
             self.u[j+1,i+1]*ai*aj)

        v = (self.v[j,i]*(1-ai)*(1-aj) +
             self.v[j,i+1]*ai*(1-aj) +
             self.v[j+1,i]*(1-ai)*aj +
             self.v[j+1,i+1]*ai*aj)

        self.used[j:j+self.spacing,i:i+self.spacing] = True

        return u,v

    def _makeStreamline(self, x0, y0):
        """
        Compute a streamline extending in both directions from the given point.
        """

        sx, sy = self._makeHalfStreamline(x0, y0, 1) # forwards
        rx, ry = self._makeHalfStreamline(x0, y0, -1) # backwards

        rx.reverse()
        ry.reverse()

        return rx+[x0]+sx, ry+[y0]+sy

    def _makeHalfStreamline(self, x0, y0, sign):
        """
        Compute a streamline extending in one direction from the given point.
        """

        xmin = self.x[0]
        xmax = self.x[-1]
        ymin = self.y[0]
        ymax = self.y[-1]

        sx = []
        sy = []

        x = x0
        y = y0
        i = 0
        while xmin < x < xmax and ymin < y < ymax:
            u, v = self._interp(x, y)
            theta = np.arctan2(v,u)

            x += sign * self.dr * np.cos(theta)
            y += sign * self.dr * np.sin(theta)
            sx.append(x)
            sy.append(y)

            i += 1

            if self.detectLoops and i % 10 == 0 and self._detectLoop(sx, sy):
                break

            if i > self.maxLen / 2:
                break

        return sx, sy

    def _detectLoop(self, xVals, yVals):
        """ Detect closed loops and nodes in a streamline. """
        x = xVals[-1]
        y = yVals[-1]
        D = np.array([np.hypot(x-xj, y-yj)
                      for xj,yj in zip(xVals[:-1],yVals[:-1])])
        return (D < 0.9 * self.dr).any()

 #*************************** here there is the issue with the names. 
 #i.e. df[type_name] does not exists, so i switched to df['name']
 #i need to look to all the other parts
 #I think it will be better to work on the df and change columns names so that these below are correct
event_frame_passes = df[(df['name'] == 'Pass') & (df['outcome_name'] != 'Incomplete') ][['team_name', 'x', 'y', 'end_x', 'end_y']]

event_frame_passes = event_frame_passes[event_frame_passes['team_name'] == 'Servette']

#event_frame_passes = df.reset_index().pivot(columns='qual_name', index=['event_id', 'x', 'y'], values='value')

event_frame_passes.reset_index(inplace=True)
event_frame_passes['dist_x'] = event_frame_passes['end_x'] - event_frame_passes['x']
event_frame_passes['dist_y'] = event_frame_passes['end_y'] - event_frame_passes['y']

xbins = 16
ybins = 16

pitch_x = 120
pitch_y = 80

xgroups = pd.cut(event_frame_passes['x'], np.arange(0, pitch_x+(pitch_x/xbins), pitch_x/xbins))
ygroups = pd.cut(event_frame_passes['y'], np.arange(0, pitch_y+(pitch_y/ybins), pitch_y/ybins))
grouped = event_frame_passes.groupby([xgroups,ygroups]).mean()
grouped = grouped[['dist_x', 'dist_y']]


grouped_distx = grouped.reset_index().pivot(columns = 'x', values = 'dist_x', index = 'y')
grouped_disty = grouped.reset_index().pivot(columns = 'x', values = 'dist_y', index = 'y')
xarr = np.array(grouped_distx)
yarr = np.array(grouped_disty)


"""Copyright (c) 2018, Nicolas P. Rougier
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

xbinsj = 16j # by specifying nj we're telling mgrid to create n points between the start and stop value
ybinsj = 16j

#create grid points such that they are at the mid point of the bins we defined earlier
Y, X = np.mgrid[0+(pitch_y/(2*ybins)):pitch_y-(pitch_y/(2*ybins)):ybinsj, 0+(pitch_x/(2*xbins)):pitch_x-(pitch_x/(2*xbins)):xbinsj] # we want mid-point of the bins on the grid

U, V = xarr, yarr

##### PLOTTING #######
fig, ax = plt.subplots(1, 1, figsize=(12,8))

pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='white', linewidth=2, line_zorder=10)
pitch.draw(ax=ax)

#define the bins to be used for the heatmap overlay
heat_bins = (18, 12)

# plot the heatmap - darker colors = more passes originating from that square
bs_heatmap = pitch.bin_statistic(event_frame_passes.x.astype(float), event_frame_passes.y.astype(float), statistic='count', bins=heat_bins)

bs_heatmap['statistic'] = bs_heatmap['statistic'] / bs_heatmap['statistic'].max()

hm = pitch.heatmap(bs_heatmap, ax=ax, cmap='coolwarm', edgecolors = 'whitesmoke', linewidth = 0, antialiased = True)

cbar = plt.colorbar(hm,ax=ax, extend = 'both', fraction=0.04, pad=0.04, orientation = 'horizontal')
cbar.set_label('Pass Origin Relative Frequency', labelpad = 10, fontsize = 14)

plt.suptitle('Barcelona Completed Pass Flow', size = 20, x = 0.5, y = 0.925, fontweight = 'bold')
plt.title('La Liga | 2019/20', size = 16, pad = -10)

# load the StatsBomb logo
sb_logo = PIL.Image.open(urlopen(('https://github.com/statsbomb/open-data/blob/fb54bd7fe20dbd5299fafc64f1f6f0d919a5e40d/'
                              'stats-bomb-logo.png?raw=true')))

add_image(sb_logo, fig, left=0.625, bottom=0.175, width=0.2)
########################

lengths = []
colors = []
lines = []

# Streamline plotting and shading
s = Streamlines(X, Y, U, V)
for streamline in s.streamlines:
    x, y = streamline
    y = [pitch_y-i for i in y] # need to invert y axis for statsbomb as 0,0 is top-left
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    n = len(segments)
    
    D = np.sqrt(((points[1:] - points[:-1])**2).sum(axis=-1))
    L = D.cumsum().reshape(n,1) + np.random.uniform(0,1)
    C = np.zeros((n,3))
    C[:] = (L*1.5) % 1

    line = LineCollection((segments), color=C, linewidth=1)
    lengths.append(L)
    colors.append(C)
    lines.append(line)
    
    ax.add_collection(line)

# Update function for animation
def update(frame_no):
    for i in range(len(lines)):
        lengths[i] += 0.05
        colors[i][:] = (lengths[i]*1.5) % 1
        lines[i].set_color(colors[i])
    pbar.update()
    

n = 27 # This appears to be the magic number to get seamless looping

animation = FuncAnimation(fig, update, frames=n, interval=2)
pbar = tqdm.tqdm(total=n)

#animation.save('pass_flow.mp4', writer='ffmpeg', fps=10)
animation.save('pass_flow.gif', writer='imagemagick', fps=20)

pbar.close()
plt.show()

from PIL import Image, ImageSequence
im = Image.open('pass_flow.gif')
frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
frames.reverse()
frames[0].save('reversed_pass_flow.gif', save_all=True, append_images=frames[1:], loop=0)

from IPython.display import Image
Image(open('reversed_pass_flow.gif','rb').read())