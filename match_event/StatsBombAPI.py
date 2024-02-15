#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 15:32:32 2021

@author: mat
"""

import statsbombpy
from statsbombpy import sb
from statsbombpy import api_client

url = "https://data.statsbombservices.com/api/v3/competitions/?/seasons/?/matches"

creds = {"user":"m.feigean@servettefc.ch","passwd":"QzG3Kdlu"}

event_json = api_client.get_resource(url,creds)

matches = api_client.matches(competition_id=80,season_id=90,creds=creds)

events = api_client.events(match_id=3783522,creds=creds)
