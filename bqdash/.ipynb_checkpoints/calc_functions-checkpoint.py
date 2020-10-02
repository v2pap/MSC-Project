from collections import OrderedDict
import pandas as pd
import numpy as np

def get_securities_in_sector(sector,df,sector_mapping):
    secs = list(df[df[sector_mapping] == sector].index.values)
    return [i for n, i in enumerate(secs) if i not in secs[:n]]

def get_peer_data(sector,df,sector_mapping):

    peer_univ =  get_securities_in_sector(sector,df,sector_mapping)
    peer_tbl = df.loc[peer_univ,:]
    return peer_tbl

def arrange_data_for_gui(security,tbl,mappings):
    # df to dictionary for easier access
    sec_tbl = tbl.loc[[security],:].reset_index()
    tbl_dict = {c:sec_tbl[c].tolist()[0] for c in sec_tbl.columns}

    gui_data = {}
    gui_data["name"] = tbl_dict[mappings['id_field']]
    gui_data["des"] = tbl_dict[mappings['description_field']]
    gui_data["industry"] = tbl_dict[mappings['sector_field']] if tbl_dict[mappings['id_field']] != 0 else 'Not Covered'

    gui_data["internal_score"] = tbl_dict[mappings['internal_score']]
    gui_data["third_party_score"] = tbl_dict[mappings['third_party_score']]
    gui_data["third_party_score_date"] = tbl_dict[mappings['third_party_score_date']].strftime('%Y-%m-%d')
    gui_data["tbl_data"] = sec_tbl.loc[:,mappings['factor_score_fields']]
    gui_data["peer_data"] = get_peer_data(gui_data["industry"],tbl,mappings['sector_field']).loc[:,mappings['factor_score_fields']].reset_index()
    return gui_data

def get_grid_map_data_from_df(df,group1,group2,weight_type):
    totals = df.groupby(by=[group1,group2]).sum().unstack().stack(dropna=False).fillna(0)
    return totals.reset_index().pivot(index=group2,columns=group1,values=weight_type)

def compute_sector_df(dictionary,date,mappings):
    return dictionary[date][[mappings['group_field'],mappings['total_score_field']]].groupby(mappings['group_field']).median().sort_values(mappings['total_score_field'],ascending=False)[[mappings['total_score_field']]]

def compute_score_hist_df(score_df,mappings):
    return score_df.reset_index().pivot_table(index=mappings['id_field'],columns=mappings['date_field'],values=mappings['total_score_field'],aggfunc = max)

def highlight_positive():
    return '''function(params){
                                if (params.value < 0) {
                                  return {color: 'red'};
                                } else {
                                  return {color: 'forestgreen'};
                                }
                               }
            '''

def highlight_scores():
    return '''function(params){
                                if (params.value > 3) {
                                  return {color: 'red'};
                                } else if (params.value===3){
                                  return {color: '#ff6600'};
                                } else if (params.value === 1){
                                  return {color:'#93C02D'};
                                }
                                  else{
                                  return{color: 'DarkOrange'};
                                }
                            }'''
