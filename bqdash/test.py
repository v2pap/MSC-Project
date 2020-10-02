import pandas as pd
import numpy as np
from .calc_functions import *
from .custom_widgets import *
import bqplot as bqp

mock_esg_data_set = pd.DataFrame(columns=['ID','NAME','INDUSTRY','DES','COUNTRY','RATING DATE','EXTERNAL RATING','INTERNAL RATING','ISSUE ONE','ISSUE TWO'],
             data=[['BA UN Equity','Boeing Co/The','Aerospace & Defense','The Boeing Company, together with its subsidia...','US',pd.Timestamp('2019-08-05 00:00:00'),'A',1,3,4],
                  ['CAT UN Equity','Caterpillar Inc','Aerospace & Defense','Caterpillar Inc. designs, manufactures, and ma...','US',pd.Timestamp('2019-08-05 00:00:00'),'BBB',1,4,3],
                  ['AXP UN Equity','American Express Co','Consumer Finance',"American Express Company is a global payment and travel company",'US',pd.Timestamp('2019-08-05 00:00:00'),'A',1,4,1],
                  ['JPM UN Equity','JPMorgan Chase & Co','Consumer Finance','JPMorgan Chase & Co. provides global financial services and retail banking.','US', pd.Timestamp('2019-08-05 00:00:00'),'AAA', 2, 3, 4],
                  ['VZ UN Equity','Verizon Communications Inc','Integrated Telecommunication Services','Verizon Communications Inc. is an integrated telecommunications company that provides wire line voice and data services...','US',pd.Timestamp('2019-08-05 00:00:00'),'AA',2,2,2,]])

mock_esg_data_set_two =pd.DataFrame(columns=['ID','NAME','INDUSTRY','DES','COUNTRY','RATING DATE','EXTERNAL RATING','INTERNAL RATING','ISSUE ONE','ISSUE TWO'],
             data=[['BA UN Equity','Boeing Co/The','Aerospace & Defense','The Boeing Company, together with its subsidia...','US',np.NaN,'A',1,3,4],
                  ['CAT UN Equity','Caterpillar Inc','Aerospace & Defense','Caterpillar Inc. designs, manufactures, and ma...','US',pd.Timestamp('2019-08-05 00:00:00'),'BBB',1,4,np.NaN],
                  ['JPM UN Equity','JPMorgan Chase & Co','Consumer Finance','JPMorgan Chase & Co. provides global financial services and retail banking.','US', pd.Timestamp('2019-08-05 00:00:00'),'AAA', 2, 3, 4],
                  [np.NaN,'Verizon Communications Inc','Integrated Telecommunication Services','Verizon Communications Inc. is an integrated telecommunications...','US',pd.Timestamp('2019-08-05 00:00:00'),'AA',2,2,2,]])

def test_get_securities_in_sector():
    sector_one = 'Aerospace & Defense'
    sector_two = 'Consumer Finance'
    sector_three = 'Integrated Telecommunication Services'
    sector_mapping_column = 'INDUSTRY'
    result_one = get_securities_in_sector(sector_one,mock_esg_data_set,sector_mapping_column)
    result_two = get_securities_in_sector(sector_two,mock_esg_data_set,sector_mapping_column)
    result_three = get_securities_in_sector(sector_three,mock_esg_data_set,sector_mapping_column)
    assert result_one == [0,1]
    assert result_two == [2,3]
    assert result_three == [4]

def test_get_peer_data():
    sector_one = 'Aerospace & Defense'
    sector_two = 'Consumer Finance'
    sector_mapping_column = 'INDUSTRY'
    result_one = get_peer_data(sector_one,mock_esg_data_set,sector_mapping_column)
    result_two = get_peer_data(sector_two,mock_esg_data_set,sector_mapping_column)
    assert type(result_one) == pd.core.frame.DataFrame
    assert list(result_one.columns)==['ID','NAME','INDUSTRY','DES','COUNTRY','RATING DATE','EXTERNAL RATING','INTERNAL RATING','ISSUE ONE','ISSUE TWO']
    assert list(result_one[['ID']].values) == ['BA UN Equity','CAT UN Equity']
    assert type(result_two) == pd.core.frame.DataFrame
    assert list(result_two.columns)==['ID','NAME','INDUSTRY','DES','COUNTRY','RATING DATE','EXTERNAL RATING','INTERNAL RATING','ISSUE ONE','ISSUE TWO']
    assert list(result_two[['ID']].values) == ['AXP UN Equity','JPM UN Equity']

def test_arrange_data_for_gui():
    security = 'JPM UN Equity'
    security_two = 'BA UN Equity'
    security_three = 'CAT UN Equity'
    security_four = np.NaN
    field_mapping = {'id_field':'ID',
                     'description_field':'DES',
                     'sector_field':'INDUSTRY',
                     'internal_score':'INTERNAL RATING',
                     'third_party_score':'EXTERNAL RATING',
                     'third_party_score_date':'RATING DATE',
                     'factor_score_fields':['ISSUE ONE','ISSUE TWO']}

    result = arrange_data_for_gui(security,mock_esg_data_set.set_index(field_mapping['id_field']),field_mapping)
    result_two = arrange_data_for_gui(security_two,mock_esg_data_set_two.set_index(field_mapping['id_field']),field_mapping)
    assert len(result.keys()) == 8
    assert result['third_party_score'] == 'AAA'
    assert list(result['peer_data'][field_mapping['factor_score_fields'][0]]) ==[4,3]
    assert result_two['third_party_score_date'] == 'Unknown'

def test_get_grid_map_data_from_df():
    pass

def test_compute_sector_df():
    pass

def test_compute_score_hist_df():
    pass

def test_get_table_data():
    pass

def test_bar_plot():
    chart = BarPlot(title='test', orientation='horizontal', padding=0.3)
    assert isinstance(chart.figure,bqp.Figure)
    assert isinstance(chart.widgets['mark_bar'] ,bqp.Bars)

def test_bar_plot_push():
    chart = BarPlot(title='test', orientation='horizontal', padding=0.3)
    pass

def test_hist_plot():
    chart = HistPlot(title='Distribution',bins=10, tick_format='0.0f')
    assert isinstance(chart.figure,bqp.Figure)
    assert isinstance(chart.widgets['mark_hist'] ,bqp.Hist)

def test_hist_plot_push():
    chart = HistPlot(title='Distribution',bins=10, tick_format='0.0f')
    pass

def test_line_plot():
    chart =LinePlot(title='Composite Scores Trend')
    assert isinstance(chart.figure,bqp.Figure)
    assert isinstance(chart.widgets['mark_line'] ,bqp.Lines)

def test_line_plot_push():
    chart = LinePlot(title='Composite Scores Trend')
    pass

def test_scatter_plot():
    chart = Scatter(title='History')
    assert isinstance(chart.figure,bqp.Figure)
    assert isinstance(chart.widgets['mark_scatter'] ,bqp.Scatter)

def test_scatter_plot_push():
    chart = Scatter(title='History')
    pass
