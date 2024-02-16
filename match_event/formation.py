#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:26:04 2021

@author: matfeig
"""

from scipy.spatial import ConvexHull
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_color='lightgrey', line_color='white', stripe=False, axis=False, label=False, tick=False)
fig, ax = pitch.draw()


data = pd.read_csv("zur_stgbomb.csv")
data.head()
#defdata.dropna(subset=['location_x'], inplace = True)



def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`

    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    Returns
    -------
    matplotlib.patches.Ellipse

    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimenLausannel dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse), mean_x, mean_y

def ellipse(team, deb=0, fin=max(data.Index)//60):
    players = data[data.Team_name == team].player_name.unique()
    fig, ax_nstd = plt.subplots(figsize=(15,9.5))
    draw_pitch("lightgrey", "black", "h", "full", ax=ax_nstd)
    for player in players[:11] :
        action = data[(data.player_name == player) & (data.start >= deb*60) & (data.start <= fin*60 )]
        ax_nstd.scatter(action.location_x, action.location_y, s=0.5, color='lightgrey')
        p, x, y = confidence_ellipse(action.location_x, action.location_y, ax_nstd, n_std=0.5, label=r'$1\sigma$', edgecolor='gold', linewidth=3, fill=True, facecolor='orange', alpha=0.2)
        plt.text(x, y, player.split()[0][:-1], ha="center", va="center",fontsize = 15, family = 'monospace', fontweight = 'bold')
        plt.title(team, fontsize = 30, color='firebrick', family = 'monospace', fontweight = 'bold' )
    plt.show()
ellipse("FC Zürich")
