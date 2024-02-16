#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:47:23 2021

@author: peter
"""
import os,re
import requests
import json
import pandas as pd
import glob
from datetime import datetime,timedelta
import datetime
from functools import reduce
import math
import numpy as np

def GetCoordStadium(home_team):
    if(home_team=="Servette"):
        Lat_0 = 46.178318
        Lon_0 = 6.127000
        rot_angle = -0.02959
        return Lat_0,Lon_0,rot_angle
    if(home_team=="Zurich"):
        Lat_0 = 47.38329613588504 #The corner should be the (0,0) of Statsbomb (not sure if it's the best solutioon )  , 8.50385923251749
        Lon_0 = 8.50385923251749
        rot_angle = -0.899 #CALCULATE AGAIN THE ANGLE!
        return Lat_0,Lon_0,rot_angle
#Function to download the GPS data
def Download(date):

    folder = re.sub('\D', '', date)
    username = 'm.feigean@servettefc.ch'
    password = 'Florence3007'
    if not os.path.isdir(folder):
        os.mkdir(folder)
    r = requests.get('https://stats.integratedbionics.com/api/gpssessions_export',
                     auth=(username, password),
                     data={
                            'date':date,
                            'org':1762
                        },
                        )
    print(r.status_code)
    sessions = r.json()
    for session in sessions:
        rawurl = session['s3rawe']
        print('Downloading ' + session['user']['name'] + ' from ' + rawurl)
        r = requests.get(rawurl)
        outfile = folder+'/'+session['user']['name']+'.json'.replace(' ','_')
        print('Saving to '+outfile)
        #print(r.content)
        with open(outfile, 'w') as f:
            #f.write(r.json())
            json.dump(r.json(), f)
    return


def JSONtoCSV(date):
    path = re.sub('\D', '', date)
    file_list = glob.glob(path+"/*.json")
    
    for f in file_list:

        longitude = []
        latitude = []
        stamp = []
        speed = []
        #loop on json files aand store longitude,latitude,timestamp,speed and save it in a csv file
        with open(f) as json_file:
        
            data = json.load(json_file)
            #print(data)
            for i in data['gpss']:
                longitude.append(i['lon'])
                latitude.append(i['lat'])
                stamp.append(datetime.datetime.fromtimestamp(i['stamp']))
                #stamp.append(datetime.datetime.fromtimestamp(i['stamp'])- timedelta(hours=2))
    
                #print(datetime.datetime.utcfromtimestamp(i['stamp']).strftime('%Y-%m-%dT%H:%M:%SZ'))
    
                speed.append(i['speed'])
        
        output = pd.DataFrame()
        output['stamp'] = stamp
        output['lon'] = longitude
        output['lat'] = latitude
        output['speed'] = speed
        
        output.to_csv(f.replace('json','csv'))

        os.remove(f) #removing json file
        
###Rotate the field given the origin of the pitch        
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

    
#function that takes the latitude and longitude of the initial and final position and calculates the distance along the x and y axis and also the angle of the movement -> it considers all different cases to correctly store the angle value
def GetMovementVector(Lambda1,Lambda2,Phi1,Phi2):
    #print('{0} * {1} * {2} * {3}'.format(Lambda1,Lambda2,Phi1,Phi2))
    R = 6370000 #m -> earth radius
    #If the point is the same, the player is not moving
    if(Lambda1==Lambda2 and Phi1==Phi2):
            return 0, 0, 0, 0
    #If he is moving on the lambda.axis    
    if(Lambda1!=Lambda2):
        x = math.sin(Lambda1*np.pi/180.)*math.sin(Lambda2*np.pi/180.) + math.cos(Lambda1*np.pi/180.)*math.cos(Lambda2*np.pi/180.)
        #x is the angle of the direction
        if x>1:
            x = 1.0
        DeltaLambda = ((Lambda2-Lambda1)/abs(Lambda2-Lambda1))*R*math.acos(x)
    else:
        DeltaLambda = 0
    #doing the same thing for Phi   
    if(Phi1!=Phi2):
        DeltaPhi = ((Phi2-Phi1)/abs(Phi2-Phi1))*R*math.acos(1+math.pow(math.cos(Lambda1*np.pi/180.),2)*(math.cos((Phi2-Phi1)*np.pi/180.)-1))
    else:
        DeltaPhi = 0
     
    #we have to multiply by -1 due to trigonometrical calculations
    DeltaLambda = DeltaLambda*(-1)
    
    #euclidean distance
    TotDist = math.sqrt(math.pow(DeltaLambda,2)+math.pow(DeltaPhi,2))
    
    #Calculating the angle
    Direction = -999
    #if he is moving along the Phi-axis
    if(DeltaLambda==0):
        if(DeltaPhi==0):
            Direction = 0
        else:
            Direction = (1-0.5*(DeltaPhi/abs(DeltaPhi)))*180.
    #if he is moving along Delta-axis
    else:
        #check which quadrant it is
        #1st quadrant
        if(DeltaLambda>0 and DeltaPhi>=0):
            Direction = math.atan(DeltaPhi/DeltaLambda)*180./np.pi
        #2nd and 3rd quadrant
        if(DeltaLambda<0):
            Direction = 180.+math.atan(DeltaPhi/DeltaLambda)*180./np.pi
        #4th quadrant
        if(DeltaLambda>0 and DeltaPhi<=0):
            Direction = 360.+math.atan(DeltaPhi/DeltaLambda)*180./np.pi
        
    return DeltaLambda, DeltaPhi, TotDist, Direction

def CSVtoXY(date,time_list,home_team):
    #take path to the files
    path = re.sub('\D', '', date)
    
    BeginMatch = time_list[0]
    EndFirstHalf = time_list[1]
    BeginSecondHalf = time_list[2]
    EndMatch = time_list[3]
    
    Lat_0,Lon_0,rot_angle = GetCoordStadium(home_team)

    #take all CSV file converted for the players
    file_list = glob.glob(path+"/*.csv")
    print(file_list)
    dict_df = {}
    #looping on list of players to get the X,Y position in the field and the direction of the movement
    for f in file_list:
        if('_XY' in f):
            continue
        print(f)
        df = pd.read_csv(f)
        df = df.dropna() #dropping events where we don't have data
        #storing only the data from exact second (ms==0)
        df['Condition'] = df['stamp'].apply(lambda x: 'True' if  x.split('.')[1]=='000' else 'False')         
        df = df[df['Condition']=='True']
        #Clean-up dataframe
        df = df.drop(['Condition'],axis=1)
        df = df.reset_index()
        df = df.drop(['index','Unnamed: 0'],axis=1)
        
        #Taking the Latitude and longitude
        Lat = df['lat']
        Lon = df['lon']
    
        if len(Lat)==0:
            continue
        #Width and length of Servette's field
        #Width = 65.0614919794312
        #Length = 101.44454040621274
        
        dLambda = []
        dPhi = []
        dist = []
        direct = []
            
        for i in range(0,len(Lat)-1):       
            Lambda1 = Lat[i]
            Lambda2 = Lat[i+1]
            Phi1 = Lon[i]
            Phi2 = Lon[i+1]
            
            DeltaLambda, DeltaPhi, TotDist, Direction = GetMovementVector(Lambda1,Lambda2,Phi1,Phi2)
            
            dLambda.append(DeltaLambda)
            dPhi.append(DeltaPhi)
            dist.append(TotDist)
            direct.append(Direction)
    
        #arrays where we store distance, direction, X, Y position in each second    
        dist.append(0)      
        direct.append(0)
         
        X = []
        Y = []
        X_rot = []
        Y_rot = []
        
        X.append(0)
        Y.append(0)
        X_rot.append(0)
        Y_rot.append(0)
        
        #First we take the X,Y withoutany rotation of the field
        for i in range(0,len(dLambda)):
            #adding the deltaX and deltaY at each step to have the X,Y position in each second
            X.append(X[i]+dLambda[i])
            Y.append(Y[i]+dPhi[i])
                    
        dLambda.append(0) 
        dPhi.append(0)
    
        #calculating distance between point (0,0) for the GPS and the corner kick
        DeltaLambda, DeltaPhi, TotDist, Direction = GetMovementVector(Lat[0],Lat_0,Lon[0],Lon_0)
        #applying translation to X,Y data to have the corner kick as (0,0)
        X = [x - DeltaLambda for x in X]
        Y = [y - DeltaPhi for y in Y]
        Speed = []
    
        #Calculate the rotated X,Y position
        for i in range(0,len(X)-1):

            qx,qy = rotate((0,0), (X[i],Y[i]), rot_angle)
            X_rot.append(qx)
            Y_rot.append(qy)
            speed = math.sqrt(pow(Y[i]-Y[i+1],2) + pow(X[i]-X[i+1],2))
            Speed.append(speed)
            
        Speed.append(0)
        #X_rot = [x - DeltaLambda for x in X_rot]
        #Y_rot = [y - DeltaPhi for y in Y_rot]
        #Storing in the DataFrame
        df['X_rot'] = X_rot
        df['Y_rot'] = Y_rot
        df['New Speed'] = Speed
        df['Direction'] = direct
        df['dLambda'] = dLambda
        df['dPhi'] = dPhi
        #plotting the X,Y position of each player to check that the data makes sense
        print(f)
        print(len(df.index))
        
        df['stamp']= df['stamp'].str.replace('.000','')
        #Converting timestamp from string to datetime object
        df['stamp'] = df['stamp'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
        #Dropping all data which is not part of the match
        df = df[ ((df['stamp'] > BeginMatch) & (df['stamp'] < EndFirstHalf)) | ((df['stamp'] > BeginSecondHalf) & (df['stamp'] < EndMatch))]
    
        #Saving the files in a new DF
        output = pd.DataFrame()        
            
        output['Time'] = df['stamp']
        output['X'] = df['X_rot']
        output['Y'] = df['Y_rot']
        output['Speed'] = df['speed']
        output['New speed'] = df['New Speed']
        output['Latitude'] = df['lat']
        output['Longitude'] = df['lon']
        output['Direction'] = df['Direction']
        output['dLambda'] = df['dLambda']
        output['dPhi'] = df['dPhi']
        #store all info in a csv file
        output.to_csv(f.replace('.csv','_XY.csv'))
        
        dict_df[f.split('.')[0].split(' ')[1]] = output
        
    return dict_df

#Function to merge all GPS data players based on the timestamp
def MergeAllPlayers(dict_df):
    for k in dict_df.keys():
        print(k)
        dict_df[k]['Y'] = -1*dict_df[k]['Y'] #TO BE CANCELED AFTER FIXING THE ANGLE! -> STATSBOMB!
        dict_df[k].loc[(dict_df[k]['Y'] > 10000) | (dict_df[k]['Y'] < -2), 'Y'] = np.nan
        dict_df[k].rename(columns={'X':'X_'+k,'Y':'Y_'+k,'Speed':'Speed_'+k,'Direction':'Direction_'+k},inplace=True)
        dict_df[k].drop(columns=['New speed','Latitude','Longitude','dLambda','dPhi'],inplace=True)
        print(k)
    
    list_df = list(dict_df.values())    
    
    tot_df = reduce(lambda x, y: pd.merge(x, y, on = 'Time',how='outer'), list_df)
    tot_df.sort_values(by=['Time'],inplace=True)
    
    tot_df.reset_index(inplace=True)
    tot_df.drop(columns=['index'],inplace=True)
    return tot_df
    
#Function to merge GPS data with event data
def MergeEvtGps(event_file,tot_df,time_list):
    
    #col_list = ['event_type_name','timestamp','team_name','possession_team_name','player_name','location_x','location_y','end_location_x','end_location_y','substituted_player_name','speedball_x','speedball_y','speedball']
    
    #List of columns we are storing
    col_list = ['event_type_name','timestamp','team_name','possession_team_name','player_name','substituted_player_name','location_x','location_y']
    
    BeginMatch = time_list[0]
    EndFirstHalf = time_list[1]
    BeginSecondHalf = time_list[2]
    
    #Splitting into 1st and 2nd half, because StatsBomb timestamp starts from 0 in the second half
    df_1sthalf = event_file[event_file.period==1]   
    #dropping milliseconds
    df_1sthalf['timestamp'] = df_1sthalf['timestamp'].apply(lambda x: x.split('.')[0])
    
    #Taking 1st half data from the GPS DF
    tot_df_1sthalf = tot_df[tot_df['Time']<EndFirstHalf]
    
    #Calculating the difference between Timestamp and Kick-off to match the Statsbomb time format
    tot_df_1sthalf['Time'] = tot_df_1sthalf['Time'].apply(lambda x: str(x-BeginMatch).split('days ')[1])    
    tot_df_1sthalf.rename(columns={'Time':'timestamp'},inplace=True)    
    tot_df_1sthalf['period'] = 1
    
    #Merging with event data, if more than 1 event in 1 second, then it creates a list of the events
    ###NEED TO ADD OTHER VARIABLES!
    df_aslist = df_1sthalf.groupby('timestamp').aggregate(lambda x: list(x)).reset_index()    
    df_event_gps_1st = pd.merge(tot_df_1sthalf,df_aslist[col_list], on='timestamp',how='outer')
    
    ###SECOND HALF###
    df_2ndhalf = event_file[event_file.period==2]   
    #dropping milliseconds
    df_2ndhalf['timestamp'] = df_2ndhalf['timestamp'].apply(lambda x: x.split('.')[0])
    
    #Taking 1st half data from the GPS DF
    tot_df_2ndhalf = tot_df[tot_df['Time']>BeginSecondHalf]
    #Calculating the difference between Timestamp and Kick-off to match the Statsbomb time format
    tot_df_2ndhalf['Time'] = tot_df_2ndhalf['Time'].apply(lambda x: str(x-BeginSecondHalf).split('days ')[1])    
    tot_df_2ndhalf.rename(columns={'Time':'timestamp'},inplace=True)    
    tot_df_2ndhalf['period'] = 2
    
    #Merging with event data, if more than 1 event in 1 second, then it creates a list of the events
    ###NEED TO ADD OTHER VARIABLES!
    df_aslist = df_2ndhalf.groupby('timestamp').aggregate(lambda x: list(x)).reset_index()    
    df_event_gps_2nd = pd.merge(tot_df_2ndhalf,df_aslist[col_list], on='timestamp',how='outer')
    
    df_event = pd.concat([df_event_gps_1st,df_event_gps_2nd], ignore_index=True)
    return df_event
        