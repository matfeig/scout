#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:01:30 2023

@author: matfeig
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
from matplotlib import cm
from highlight_text import fig_text, ax_text

import seaborn as sns

from PIL import Image
import urllib
import os


plt.rcParams['font.family'] = 'Karla'

df = pd.read_csv('data/02122023_passes.csv', index_col=0)
df['date'] = pd.to_datetime(df['date'])


df_new = df[df['date'] >= '2022-08-01'].reset_index(drop=True)
df_new = df_new[df_new['position'] != 'GK'].reset_index(drop=True)
df_teams = (
    df_new
    .groupby(['team_id', 'team_name', 'match_id', 'date'])
    [['total_passes', 'accurate_passes']].sum()
    .assign(pass_accuracy = lambda x: x.accurate_passes/x.total_passes)
    .reset_index()
    .sort_values(by=['team_name', 'date'])
    .reset_index(drop=True)
)



# -- Compute rolling average
df_teams['rolling_pass'] = (
    df_teams
    .groupby(['team_name'])
    .rolling(window=3, min_periods=0)['pass_accuracy']
    .mean()
    .reset_index(drop=True)
)

df_new = df_new.assign(pass_accuracy = lambda x: x.accurate_passes/x.total_passes)
df_all = df_new[df_new['minutes_played'] >= 30].reset_index(drop=True)

df_spurs = df_teams[df_teams['team_name'] == 'Brighton & Hove Albion'].reset_index(drop=True)
df_scatter = pd.DataFrame()
for index, match in enumerate(df_spurs['match_id']):
    df_aux = df_new[df_new['team_name'] == 'Brighton & Hove Albion']
    df_aux = df_aux[df_aux['minutes_played'] >= 30]
    df_aux = df_aux[df_aux['match_id'] == match]
    df_aux = df_aux.assign(x_pos = index)
    df_scatter = pd.concat([df_scatter, df_aux])
    df_scatter.reset_index(drop=True, inplace=True)
    
fig = plt.figure(figsize=(7,4), dpi=200)
axs = fig.subplot_mosaic(
    'DS', gridspec_kw={
        "width_ratios":[.15,.5]
    }, sharey=True
)


axs['D'].set_ylim(.4,1.05)

main_color = '#0057B8'
second_color = 'grey'

axs['S'].grid(ls='dashed', lw=.5, color='lightgrey')
axs['S'].plot(df_spurs.index, df_spurs.rolling_pass, color=main_color,
        zorder=5, marker='o', markevery=[-1],
        markersize=8, mfc=axs['S'].get_facecolor(), lw=2.5, mew=2, label='5-game moving average')

axs['S'].legend(markerscale=0.75, loc='upper center', bbox_to_anchor = [0.5, 1.06], fontsize='x-small')

sns.scatterplot(data=df_scatter, x='x_pos', y='pass_accuracy', size='total_passes', alpha=0.25, color=second_color, zorder=3,
                legend=False, sizes=(5,100), ax=axs['S'], ec=second_color)

axs['S'].set_xlabel('Match index')

axs['D'].grid(ls='dashed', lw=.5, color='lightgrey')
sns.histplot(data=df_scatter, y='pass_accuracy', ax=axs["D"], 
            element='step', zorder=2, color=second_color, alpha=0.5, stat='density')
axs['D'].invert_xaxis()
axs['D'].spines['left'].set_visible(False)
axs['D'].spines['right'].set_visible(True)
axs['D'].spines['bottom'].set_visible(False)
axs['D'].yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0%}'))
axs['D'].set_xticks([])
axs['D'].yaxis.tick_right()
# -- Turn of labels
axs['D'].set_ylabel('')
axs['D'].set_xlabel('')

fig_text(
    x=0.17, y=1.11, s='<Brighton & Hove Albion\'s> passing accuracy in the EPL', family='DM Sans',
    ha='left', va='center', weight='normal', size='large',
    highlight_textprops = [{'weight':'bold', 'size':'x-large'}] 
)
fig_text(
    x=0.12, y=1.01, s='<5-game moving average> pass accuracy in the 2022/2023 Premier League.\n<Bubbles> denote passing accuracy of <individual players> (exc. GK) with at least 30 minutes played, for each match.\n<Bubble size> denotes the number of passes attempted. Viz by @sonofacorner.', 
    family='Karla',
    ha='left', va='center', size='x-small',
    highlight_textprops = [{'weight':'bold', 'color':main_color}, {'weight':'bold', 'color':second_color}, {'weight':'bold', 'color':second_color}, {'weight':'bold', 'color':second_color}] 
)


ax_size = 0.075
image_ax = fig.add_axes(
    [0.1, 1.08, ax_size, ax_size],
    fc='None'
)
fotmob_url = 'https://images.fotmob.com/image_resources/logo/teamlogo/'
club_icon = Image.open(urllib.request.urlopen(f'{fotmob_url}{df_spurs["team_id"].iloc[0]:.0f}.png'))
image_ax.imshow(club_icon)
image_ax.axis('off')

plt.savefig(
	"figures/0122023_pass_rolling.png",
	dpi = 500,
	facecolor = "#EFE9E6",
	bbox_inches="tight",
    edgecolor="none",
	transparent = False
)

plt.savefig(
	"figures/0122023_pass_rolling_tr.png",
	dpi = 500,
	facecolor = "none",
	bbox_inches="tight",
    edgecolor="none",
	transparent = True
)