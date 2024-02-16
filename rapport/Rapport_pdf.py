from fpdf import FPDF

import API
import xg
import defense_territory_v2
import xThreat
import last_third_of_the_field
import duel
import match_sonars_v2
import ball_speed
import pressure
import indices

id_match = API.n_dernier_match(1,["Servette"])

for id in id_match :
    teams = API.teams_in_match(id)
    df_matches = API.df_matches
    df_events = API.df_events(id)
    match_info = df_matches[(df_matches.match_id == id)]
    match_info.reset_index(drop=True, inplace=True)
    home_team_name = match_info["home_team_name"][0]
    away_team_name = match_info["away_team_name"][0]
    home_score = match_info["home_score"][0]
    away_score = match_info["away_score"][0]
    fig1_1 = xg.xg(id,df_events)
    fig1_1.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xg.png')
    print("1_1")
    fig1_2 = last_third_of_the_field.passes_in_the_last_third(id,df_events)
    fig1_2.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/passes_in_the_last_third.png')
    print("1_2")
    fig1_3 = ball_speed.ball_speed(id,df_events)
    fig1_3.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/ball_speed.png')
    print("1_3")
    fig2_1 = xThreat.xT_diff(id)
    fig2_1.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xT_diff.png')
    print("2_1")
    for team in teams :
        print(id,team)
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font(family='Times', style='', size=7)
        pdf.set_text_color(0, 0, 0)
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xg.png', x=4, y=30, w=90, h=56)
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/passes_in_the_last_third.png', x=4, y=92, w=90, h=56)
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/ball_speed.png', x=4, y=153, w=90, h=56)
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xT_diff.png', x=105, y=30, w=90, h=56)
        fig2_2 = xThreat.xT_joueur(id,team,df_events)
        fig2_2.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xT_joueur.png')
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/xT_joueur.png', x=105, y=92, w=90, h=56)
        print("2_2")
        fig2_3 = match_sonars_v2.match_sonars(id,team,df_events)
        fig2_3.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/match_sonars.png')
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/match_sonars.png', x=105, y=153, w=90, h=56)
        print("2_3")
        fig3_1 = duel.duel(team,id,df_events)
        fig3_1.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/duel.png')
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/duel.png', x=206, y=30, w=90, h=56)
        print("3_1")
        fig3_2 = defense_territory_v2.defense_territory(id,team,df_events)
        fig3_2.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/defense_territory.png')
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/defense_territory.png', x=206, y=92, w=90, h=56)
        print("3_2")
        fig3_3 = pressure.pressure(id,team,df_events)
        fig3_3.savefig('/Users/matfeig/Dropbox/SFC/Code/rapport/image/pressure.png')
        pdf.image('/Users/matfeig/Dropbox/SFC/Code/rapport/image/pressure.png', x=206, y=153, w=90, h=56)
        print("3_3")
        ind1,ind2,ind3,ind4 = indices.indices_possessions(id,team,df_events)
        ind5,ind6 = indices.indices_tirs(id,team,df_events)
        ind7,ind8,ind9,ind10 = indices.indices_def(id,team,df_events)
        pdf.set_xy(0, 0)
        pdf.cell(140, 25, border=1)
        pdf.set_xy(0, 0)
        pdf.cell(70, 5, txt="Possession time : " + str(ind1), ln=0.01, align="C")
        pdf.set_xy(0, 5)
        pdf.cell(70, 5, txt="Number of possessions for a shot : " + str(ind2), ln=0.01, align="C")
        pdf.set_xy(0, 10)
        pdf.cell(70, 5, txt="Pass by possession : " + str(ind3), ln=0.01, align="C")
        pdf.set_xy(0, 15)
        pdf.cell(70, 5, txt="Last third possession time : " + str(ind4), ln=0.01, align="C")
        pdf.set_xy(0, 20)
        pdf.cell(70, 5, txt="Number of passes before a shot : " + str(ind5), ln=0.01, align="C")
        pdf.set_xy(70, 0)
        pdf.cell(70, 5, txt="Possession time before a shot : " + str(ind6), ln=0.01, align="C")
        pdf.set_xy(70, 5)
        pdf.cell(70, 5, txt="PPDA : " + str(ind7), ln=0.01, align="C")
        pdf.set_xy(70, 10)
        pdf.cell(70, 5, txt="Challenge intensity index : " + str(ind8), ln=0.01, align="C")
        pdf.set_xy(70, 15)
        pdf.cell(70, 5, txt="Average height of defensive actions : " + str(ind9), ln=0.01, align="C")
        pdf.set_xy(70, 20)
        pdf.cell(70, 5, txt="Average height of defensive actions of center backs : " + str(ind10), ln=0.01, align="C")
        title = home_team_name + '  ' + str(int(home_score)) + ' - ' + str(int(away_score)) + '  ' + away_team_name
        pdf.set_font(family='Times', style='', size=30)
        pdf.set_xy(140, 0)
        pdf.cell(157, 25, txt=title, border=1, align="C")
        file_name = str(id) + '_' + team + '.pdf'
        pdf.output(file_name)
