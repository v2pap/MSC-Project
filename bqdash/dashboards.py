from abc import ABCMeta, abstractmethod, ABC
import pandas as pd
import numpy as np
from ipywidgets import HTML, VBox, HBox, Button,Tab, Dropdown, Layout, ToggleButtons
from bqdash.base_dashboard import BaseDashBoard
import bqdash.calc_functions as calc_functions
from bqdash.custom_widgets import HeatMap, Scatter,BarPlot,LinePlot,HistPlot, ThirdPartyRatings, InternalRatings, Quartiles, DataGrid
from collections import OrderedDict

class ScoringDashboard(BaseDashBoard):
    """Creates a Scorecard dashboard from a dataframe of input data. For best
    results, make sure to map your columns so bqdash knows which elements are important.
    A title for the dashboard can be optionally passed as a parameter.

    Parameters
    ----------
    df: Pandas dataframe
        The dataframe containing the data
    title: string (default='Factor Scoring Dashboard')
        An optional title to be displayed on the figure.
    colors:  dictionary of strings (default={'distribution':'#008616','median':'#E75480','scatter':'dodgerblue'})
        Required keys - 'distribution','median','scatter'
        For best results provide colors in hex format
    column_mappings: dictionary
        A dictionary to map the columns in your Dataframe to bqdash ids.
        Required keys - 'id_field','group_field','total_score_field','date_field',factor_score_fields
        Example:{'id_field':'Name',
                 'group_field':'Sector',
                 'total_score_field':'Total Score',
                 'date_field':'DATE',
                 'factor_score_fields':['Factor 1','Factor 2','Factor 3','Factor 4','Factor 5','Factor 6','Factor 7','Factor 8','Factor 9','Factor 10']}

    Attributes
    ----------

    """
    def __init__(self,df,column_mappings,colors={'distribution':'#008616','median':'#E75480','scatter':'dodgerblue'}, title='Factor Scoring Dashboard'):

        try:
            super().__init__(df=df, colors=colors, title=title, column_mappings=column_mappings)
            self.verify_user_input()
            self._read_col_mapping()
            self.score_df = self.data.reset_index().set_index(self.id_field)
            self.score_df[self.date_field] = self.score_df[self.date_field].dt.strftime('%Y-%m-%d')
            self.charts_selected = []
            self.dates = list(self.score_df[self.date_field].unique())
            self.date_count = len(self.dates)
            self.scores_on_each_date = OrderedDict([(name,group) for name,group in self.score_df.groupby(self.date_field,sort=False)])
            self.score_history_df = calc_functions.compute_score_hist_df(self.score_df,self.column_mappings)
            self.score_latest_df = self.scores_on_each_date[max(self.dates)][[self.total_field]]
            self.score_sector_df = calc_functions.compute_sector_df(self.scores_on_each_date,max(self.dates),self.column_mappings)

            self.scatter_selected = []
            self._build_all()
            self.__update_grid()
        except ValueError as e:
            raise ValueError(e) from None

    def _read_col_mapping(self):
        verify_fields = self.check_required_fields(['id_field','group_field','total_score_field','date_field','factor_score_fields'])
        if len(verify_fields) == 0:
            self.id_field = self.column_mappings['id_field']
            self.group_field = self.column_mappings['group_field']
            self.total_field = self.column_mappings['total_score_field']
            self.date_field = self.column_mappings['date_field']
            self.factor_fields = self.column_mappings['factor_score_fields']
            self.display_fields= [self.id_field,self.group_field,self.total_field]
        else:
            error_msg = 'Missing Fields in column_mapping: ' + ','.join(verify_fields)
            raise ValueError(error_msg)

    def _build_all(self):
        chart_box = self.__build_charts()
        grid_box = self.__build_grid()

        self._toggle_children([self._widgets['title'],
                         chart_box,
                         grid_box,
                         self._widgets['trend_chart_box']])

        self.layout=Layout(width='99%')

    def __build_charts(self):
        # Histogram for distribution of current composite score
        self._widgets['hist_plot'] = HistPlot(title='Distribution',bins=10,colors=[self.colors['distribution']], tick_format='0.0f')
        self._widgets['hist_plot'].push(self.score_latest_df)
        self._widgets['hist_plot'].widgets['mark_hist'].observe(self.__hist_plot_on_select, 'selected')
        # Sector median bar chart
        self._widgets['bar_plot'] = BarPlot(title='Median', orientation='horizontal', padding=0.3,colors=[self.colors['median']])
        self._widgets['bar_plot'].push(self.score_sector_df)
        self._widgets['bar_plot'].widgets['mark_bar'].observe(self.__bar_plot_on_select, 'selected')
        # Historical Trend Chart
        self._widgets['trend_chart'] = LinePlot(title='Composite Scores Trend')
        self._widgets['trend_chart_box'] = VBox([self._widgets['trend_chart'].show()],layout={'display':'none','height':'300px','width': '75%','overflow_y':'hidden', 'overflow_x':'hidden','margin':'0 0 0 200px'})
        #Scatter plot for historical dates
        self._widgets['scatter_plot'] = Scatter(title='History',colors=[self.colors['scatter']])
        self._widgets['scatter_plot'].widgets['mark_scatter'].on_element_click(self.__scatter_on_select)
        self._widgets['scatter_plot'].widgets['mark_scatter'].on_background_click(self.__background_callback)
        self._widgets['scatter_label'] = HTML('Click a point to generate a time series chart below the table',layout={'margin':'0 0 0 280px'})
        self._widgets['scatter_plot_box'] = VBox([self._widgets['scatter_label'],self._widgets['scatter_plot'].show()], layout={'width': '50%','overflow_x':'hidden'})
        self.__set_chart_configs()
        if self.date_count == 1:
            self._widgets['bar_plot_box'] = VBox([self._widgets['hist_plot'].show(), self._widgets['bar_plot'].show()], layout={'height':'50%','width': '100%', 'overflow_x':'hidden'})
            return HBox([self._widgets['bar_plot_box']])
        else:
            self._widgets['scatter_plot'].push(self.score_history_df)
            self._widgets['bar_plot_box'] = VBox([self._widgets['hist_plot'].show(), self._widgets['bar_plot'].show()], layout={'height':'50%','width': '50%', 'overflow_x':'hidden'})
            return HBox([self._widgets['bar_plot_box'],self._widgets['scatter_plot_box']])

    # Common configurations among histogram and sector median bar charts
    def __set_chart_configs(self):
        self._widgets['hist_plot'].figure.fig_margin = {'bottom': 20, 'left': 40, 'right': 20, 'top': 20}
        self._widgets['bar_plot'].figure.fig_margin = {'bottom': 20, 'left': 170, 'right': 20, 'top': 20}
        self._widgets['hist_plot'].widgets['mark_hist'].selected_style = self._widgets['bar_plot'].widgets['mark_bar'].selected_style =  {'opacity': 1.0}
        self._widgets['hist_plot'].widgets['mark_hist'].unselected_style = self._widgets['bar_plot'].widgets['mark_bar'].unselected_style = {'opacity': 0.3}
        self._widgets['hist_plot'].widgets['hist_view'].layout = self._widgets['bar_plot'].widgets['bar_view'].layout = Layout(overflow_x='hidden')
        self._widgets['hist_plot'].figure.layout = self._widgets['bar_plot'].figure.layout=self._widgets['trend_chart'].layout = {'height': '250px', 'width': '100%'}
        self._widgets['trend_chart'].figure.layout = {'height': '300px','overflow_y':'hidden'}
        self._widgets['hist_plot'].widgets['axis_y'].grid_lines = self._widgets['bar_plot'].widgets['axis_x'].grid_lines = 'none'
        self._widgets['hist_plot'].widgets['axis_x'].grid_lines = self._widgets['bar_plot'].widgets['axis_y'].grid_lines = 'dashed'
        self._widgets['hist_plot'].widgets['mark_hist'].interactions = self._widgets['bar_plot'].widgets['mark_bar'].interactions = {'click': 'select'}
        self._widgets['scatter_plot'].figure.height = '450px'
        self._widgets['scatter_plot'].figure.fig_margin = {'bottom': 40, 'left': 80, 'right': 40, 'top': 40}
        self._widgets['scatter_plot'].widgets['mark_scatter'].interactions={'click': 'select','hover':'tooltip'}
        self._widgets['scatter_plot'].widgets['mark_scatter'].selected_style={'opacity': 1.0, 'fill': 'DarkOrange', 'stroke': 'Red'}
        self._widgets['scatter_plot'].widgets['mark_scatter'].unselected_style={'opacity': 0.5}
        self._widgets['scatter_plot'].widgets['axis_x'].grid_lines  = 'dashed'
        self._widgets['scatter_plot'].widgets['axis_y'].grid_lines  = 'dashed'

    def update_colors(self,new_colors):
        '''Public Function'''
        self._widgets['hist_plot'].widgets['mark_hist'].colors = new_colors['distribution'] if isinstance(new_colors['distribution'],list) else [new_colors['distribution']]
        self._widgets['bar_plot'].widgets['mark_bar'].colors = new_colors['median'] if isinstance(new_colors['median'],list) else [new_colors['median']]
        self._widgets['scatter_plot'].widgets['mark_scatter'].colors = [new_colors['scatter']]

    def __build_grid(self):
        self._widgets['date_toggle'] = ToggleButtons(options=self.dates, description='As Of')
        self._widgets['date_toggle'].observe(lambda x: self.__date_toggle_callback(), 'value')

        # Detail grid
        company_cols = [{'headerName': f, 'field': f, 'width': 180,'pinned':'left'} for f in self.display_fields]
        score_cols = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 100,'cellStyle': calc_functions.highlight_positive()} for f in self.factor_fields]

        column_defs = [
            {'headerName': 'Company', 'children': company_cols},
            {'headerName': 'Factors', 'children': score_cols}
        ]

        self._widgets['grid'] = DataGrid(column_defs=column_defs)

        return VBox([self._widgets['date_toggle'],
                     self._widgets['grid']], layout={'width': '100%', 'margin': '20px 0px 0px 0px', 'overflow_x':'hidden'})

    def __date_toggle_callback(self):
        self.__update_grid()
        date = self._widgets['date_toggle'].value
        self._widgets['hist_plot'].push(self.scores_on_each_date[date][[self.total_field]])
        self._widgets['bar_plot'].push(calc_functions.compute_sector_df(self.scores_on_each_date,date,self.column_mappings))

    def __hist_plot_on_select(self,event):
        del self.charts_selected[:]
        self._widgets['bar_plot'].widgets['mark_bar'].selected = None
        index_selected = self._widgets['hist_plot'].widgets['mark_hist'].selected

        if index_selected is not None:
            self.charts_selected.extend(self.score_latest_df.iloc[index_selected].index.tolist())
        else:
            self.charts_selected.extend(self.score_latest_df.index)

        self.__update_grid()

    # Actions when user selects on sector median bar plot
    def __bar_plot_on_select(self,event):
        self._widgets['hist_plot'].widgets['mark_hist'].selected= None
        index_selected = self._widgets['bar_plot'].widgets['mark_bar'].selected

        if index_selected is not None:
            selected_sectors = self.score_sector_df.index[index_selected]
        else:
            selected_sectors = self.score_sector_df.index

        del self.charts_selected[:]
        self.charts_selected.extend(self.score_df[self.score_df.Sector.isin(selected_sectors)].index.values)

        self.__update_grid()

    # Actions when user selects on scatter plot
    def __scatter_on_select(self,mark,event):
        new_select = (event['data']['index'])
        if new_select not in self.scatter_selected:
           self.scatter_selected.append(event['data']['index'])
        self.__update_trend_chart()

    def __update_trend_chart(self):
       score_trend_df  = self.score_history_df.loc[list(self.score_history_df.iloc[self.scatter_selected].index)]
       self._widgets['trend_chart'].push(score_trend_df.T)
       self._widgets['trend_chart'].widgets['axis_x'].grid_lines = 'dashed'
       self._widgets['trend_chart'].widgets['axis_y'].grid_lines = 'none'
       self._widgets['trend_chart_box'].layout.display = ''

    def __background_callback(self,mark,target):
        self.scatter_selected = []
        self.__update_trend_chart()
        self._widgets['trend_chart_box'].layout.display = 'none'

    def __update_grid(self):
        date = self._widgets['date_toggle'].value
        # Filter by as of date
        score_asof_df_temp = self.scores_on_each_date[date]
        score_asof_df = score_asof_df_temp.copy(deep=True)

        # Filter by selected stocks
        # If no selection, then show everything
        if self.charts_selected:
            score_asof_df = score_asof_df[score_asof_df.index.isin(self.charts_selected)]

        self._widgets['grid'].update_grid_data(score_asof_df.reset_index())

class PortfolioDashboard(BaseDashBoard):
    """Creates a Portfolio exposure dashboard from a dataframe of input data. For best
    results, make sure to map your columns so bqdash knows which elements are important.
    A title for the dashboard can be optionally passed as a parameter.

    Parameters
    ----------
    df: Pandas dataframe
        The dataframe containing the data
    title: string (default='Portfolio Dashboard')
        An optional title to be displayed on the figure.
    colors:  dictionary of strings (default={'heat_map':'RdPu'})
        Color to define the heatmap colorscale.
        Colors either be a valid colorscale or a list of colors to represent the scale - Matplot lib and Seabor ncolor scales can be used in this way
        For best results provide colors in hex format
    column_mappings: dictionary
        A dictionary to map the columns in your Dataframe to bqdash ids.
        Required keys - 'id_field','group_field','port_field','index_field'
        Example: {'id_field':'Name',
                  'group_field':['Sector','Region','Currency','Credit Rating'],
                  'port_field':'Fund (%)',
                  'index_field':'Index (%)'}

    Attributes
    ----------

    """
    def __init__(self,df,column_mappings,colors={'heat_map':'RdPu'}, title='Portfolio Dashboard'):

        try:
            super().__init__(df=df, title=title, colors=colors, column_mappings=column_mappings)
            self.verify_user_input()
            self._read_col_mapping()
            self.data['Active (%)'] = self.data[self.port_field] - self.data[self.index_field]
            self._build_all()
            self.update_heatmap()
        except ValueError as e:
            raise ValueError(e) from None

    def _read_col_mapping(self):
        verify_fields = self.check_required_fields(['id_field','group_field','port_field','index_field'])
        if len(verify_fields) == 0:
            self.id_field = self.column_mappings['id_field']
            self.groups = self.column_mappings['group_field']
            self.port_field = self.column_mappings['port_field']
            self.index_field = self.column_mappings['index_field']
        else:
            error_msg = 'Missing Fields in column_mapping: ' + ','.join(verify_fields)
            raise ValueError(error_msg)

    def _build_all(self):

        # HeatMap
        # Create dropown _widgets
        self._widgets['dropdown_x'] = Dropdown(description='X axis',options=self.groups)
        self._widgets['dropdown_x'].value = self.groups[0]
        self._widgets['dropdown_y'] = Dropdown(description='Y axis',options=self.groups)
        self._widgets['dropdown_y'].value = self.groups[1]
        self._widgets['dropdown_z'] = Dropdown(description='Type',options=[self.port_field,self.index_field,'Active (%)'])

        # Bind callback to the dropdown _widgets
        self._widgets['dropdown_x'].observe(self._update_plot, names=['value'])
        self._widgets['dropdown_y'].observe(self._update_plot, names=['value'])
        self._widgets['dropdown_z'].observe(self._update_plot, names=['value'])

        # Create Box containers
        self._widgets['settings'] = HBox([self._widgets['dropdown_z'],self._widgets['dropdown_x'], self._widgets['dropdown_y']],
                                        layout={'width':'65%','margin':'0 0 0 130px'})
        self._widgets['Heatmap'] = HeatMap(color_scale=self.colors['heat_map'],callback=self.__update_transparency_table)
        self._widgets['transparency_lbl'] = HTML('<p style="color: #F2F3F4;font-size:30px">Portfolio Holdings</p>',layout={'margin':'0 0 0 130px','overflow_x':'visible','overflow_y':'visible','display':'none'})
        self._widgets['portfolio_grid_error'] = HTML('<p style="color: #F7DC6F;font-size:20px">Error: Same Grouping Selected</p>')
        self._widgets['portfolio_table_error'] = HTML('<p style="color: #F7DC6F;font-size:20px">Portfolio Contains No Stocks in this Allocation</p>')
        self._widgets['portfolio_table'] = DataGrid()
        self._widgets['port_table_box'] = VBox([self._widgets['portfolio_table']],layout={'width':'70%','height':'250px','margin':'5px 0 0 130px','display':'none'})


        self._toggle_children([
            self._widgets['title'],
            self._widgets['settings'],
             self._widgets['Heatmap'].show(),
             self._widgets['transparency_lbl'],
             self._widgets['port_table_box']

        ])


    def update_colors(self,new_colors):
        '''Public Function'''
        if type(new_colors['heat_map']) == list:
            self._widgets['Heatmap'].widgets['col_sc'].colors = new_colors['heat_map']
        else:
            self._widgets['Heatmap'].widgets['col_sc'].scheme = new_colors['heat_map']

    def update_heatmap(self):
        self._toggle_children([self._widgets['title'],
                              self._widgets['settings'],
                              self._widgets['loading']])
        self._widgets['Heatmap'].push(self.data,
                                     self._widgets['dropdown_x'].value,
                                     self._widgets['dropdown_y'].value,
                                     self._widgets['dropdown_z'].value)
        self._toggle_children([self._widgets['title'],
                               self._widgets['settings'],
                               self._widgets['Heatmap'].show(),
                               self._widgets['transparency_lbl'],
                               self._widgets['port_table_box']])

    def _update_plot(self,evt):
        '''callback function for dropdown _widgets'''
        try:
            if evt is not None and evt['new'] is not None and evt['old'] is not None:
                new_value = evt['new']
                self._widgets['Heatmap'].widgets['fig'].layout.display = 'none'
                self._widgets['transparency_lbl'].layout.display = 'none'
                self._widgets['port_table_box'].layout.display = 'none'
                self._widgets['portfolio_table'] = None
                self.update_heatmap()
        except ValueError:
            self._toggle_children([self._widgets['settings'],
                                                   self._widgets['portfolio_grid_error']])

        self._widgets['Heatmap'].widgets['fig'].layout.display = ''

    def __update_transparency_table(self,chart,target):
        self._widgets['transparency_lbl'].layout.display = ''
        self._widgets['port_table_box'].layout.display = ''
        group1 = self._widgets['dropdown_x'].value
        group2 = self._widgets['dropdown_y'].value
        grid_data =calc_functions.get_grid_map_data_from_df(self.data,group1,group2,self.port_field)
        try:
            columns = list(grid_data.columns)[target['data']['column']]
            rows = list(grid_data.index)[target['data']['row']]
            transparency_df = self.__get_table_data(group1,group2)
            column_defs = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150} for f in transparency_df[columns,rows].columns]
            self._widgets['portfolio_table'] = DataGrid(df =transparency_df[columns,rows].round(2), column_defs=column_defs)
            self._widgets['port_table_box'].children = [self._widgets['portfolio_table']]
        except:
            self._widgets['port_table_box'].children = [self._widgets['portfolio_table_error']]

    def __get_table_data(self,group1,group2):
        portfolio = self.data.copy(deep=True)
        portfolio = portfolio[pd.notnull(portfolio[self.port_field])]
        portfolio[[self.port_field, self.index_field,'Active (%)']] = portfolio[[self.port_field, self.index_field,'Active (%)']].fillna(value=0)
        portfolio = portfolio.reset_index()
        portfolio= portfolio[[self.id_field,group1,group2,self.port_field, self.index_field,'Active (%)']]
        region_list = {key:val for key,val in portfolio.groupby(by=[group1,group2])}
        return region_list


class EsgDashboard(BaseDashBoard):
    """Creates am ESG dashboard from a dataframe of input data. For best
    results, make sure to map your columns so bqdash knows which elements are important.
    A title for the dashboard can be optionally passed as a parameter.

    Parameters
    ----------
    df: Pandas dataframe
        The dataframe containing the data
    title: string (default='ESG Dashboard')
        An optional title to be displayed on the figure.
    colors:  dictionary of strings (default={'name':'#F6980A','industry':'#fffff','des':'#CFB010','third_party':'#F6980A'})
        Required keys - 'name','industry','des','third_party'
        For best results provide colors in hex format
    ratings_scale: list of strings (default=None)
        A rating scale for the third party score. If none is provided then it will be inferred from the data
    column_mappings: dictionary
        A dictionary to map the columns in your Dataframe to bqdash ids.
        Required keys - 'id_field','description_field','sector_field','internal_score',third_party_score,third_party_score_date,factor_score_fields
        Example:{'id_field':'NAME',
                 'description_field':'DES',
                 'sector_field':'GICS_SUB_INDUSTRY_NAME',
                 'internal_score':'INTERNAL RATING',
                 'third_party_score':'THIRD PARTY RATING',
                 'third_party_score_date':'RATING DATE',
                 'factor_score_fields':['ISSUE ONE SCORE','ISSUE TWO SCORE','ISSUE THREE SCORE',
                                        'ISSUE FOUR SCORE','ISSUE FIVE SCORE','ISSUE SIX SCORE',
                                        'ISSUE SEVEN SCORE','ISSUE EIGHT SCORE']}
    Attributes
    ----------

    """
    def __init__(self,column_mappings,df=None,colors={'name':'#F6980A','industry':'#fffff','des':'#CFB010','third_party':'#F6980A'},
                 title='ESG Dashboard',ratings_scale=None):

        try:
            super().__init__(df=df, colors=colors, title=title, column_mappings=column_mappings)
            self.verify_user_input()

            self._read_col_mapping()
            if df.index.is_numeric():
                self.data = self.data.set_index(self.id_field)
            else:
                self.data = self.data.reset_index().set_index(self.id_field)
            self.securities = list(self.data.index.dropna().values)
            self.sec_data = None
            self.ratings_scale = ratings_scale
            self._build_all()
        except ValueError as e:
            raise ValueError(e) from None

    def _read_col_mapping(self):
        verify_fields = self.check_required_fields(['id_field','description_field','sector_field','internal_score','third_party_score','third_party_score_date','factor_score_fields'])
        if len(verify_fields) == 0:
            self.id_field = self.column_mappings['id_field']
            self.description_field = self.column_mappings['description_field']
            self.sector_field = self.column_mappings['sector_field']
            self.internal_score = self.column_mappings['internal_score']
            self.third_party_score = self.column_mappings['third_party_score']
            self.third_party_score_date = self.column_mappings['third_party_score_date']
            self.factors = self.column_mappings['factor_score_fields']
        else:
            error_msg = 'Missing Fields in column_mapping: ' + ','.join(verify_fields)
            raise ValueError(error_msg)

    def _build_all(self):

        # ticker input
        self._widgets['ticker_and_btn'] = self.__build_ticker_and_btn()
        # name and des
        name_and_des = self.__build_name_and_des()
        #company info
        third_party_rating = self.__build_third_party_rating()
        self._widgets['des_box'] = HBox([name_and_des, third_party_rating])

        column_defs_single = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150,'cellStyle': calc_functions.highlight_scores()} for f in self.factors]
        column_defs_peers = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150,'cellStyle': calc_functions.highlight_scores()} for f in [self.id_field] + self.factors]

        self._widgets['tbl'] = DataGrid(column_defs=column_defs_single)
        self._widgets['tbl'].layout={'width':'100%','height':'250px'}
        self._widgets['peer_tbl'] = DataGrid(column_defs=column_defs_peers)
        self._widgets['peer_tbl'].layout={'width':'100%','height':'250px'}
        self._widgets['Tab'] = Tab(layout={'width':'90%'})

        self._toggle_children ([
            self._widgets['title'],
            self._widgets['ticker_and_btn']
        ])

    def __build_ticker_and_btn(self):
        self._widgets['ticker_input'] = Dropdown(options=self.securities)
        self._widgets['btn'] = Button(description = "Run Report")
        self._widgets['btn'].on_click(self.__run_btn_call_back)
        panel = HBox([self._widgets['ticker_input'],
                      self._widgets['btn']])
        return panel

    def __build_name_and_des(self):
        self._widgets['name'] = HTML()
        self._widgets['des'] = HTML()
        self._widgets['industry'] = HTML()
        self._widgets['internal_score'] = InternalRatings(self.internal_score)
        self._widgets['internal_score'].layout = {'margin':'30px 0 0 0','width':'500px'}
        panel = VBox([self._widgets['name'],
                      self._widgets['industry'],
                      self._widgets['des'],
                      self._widgets['internal_score']
                      ])
        # layout
        panel.layout.width = "50%"
        return panel

    def __build_third_party_rating(self):

        self._widgets['thirdparty'] = self.__build_tp_rating__widgets()
        self._widgets['thirdparty'].layout.max_height = "300px"
        self._widgets['thirdparty'].layout.width = "500px"
        self._widgets['thirdparty'].layout.margin = '0 0 0 20px'
        panel = VBox([self._widgets['thirdparty']])
        panel.layout.width = "50%"
        panel.layout.overflow_x = "hidden"
        return panel

    def __build_tp_rating__widgets(self):
        if self.ratings_scale:
            return ThirdPartyRatings(self.third_party_score,self.ratings_scale,self.colors['third_party'])
        else:
            ratings = list(self.data[self.column_mappings['third_party_score']].dropna().sort_values().unique())
            return ThirdPartyRatings(self.third_party_score,ratings,self.colors['third_party'])

    def __update(self, data):
        self.__update_name_and_des(data)
        self.__update_third_party_rating(data)
        self.__update_tables(data)

    def __update_name_and_des(self, data):
        self._widgets['name'].value = '<h1  style="color: {}">'.format(self.colors['name']) +  str(data['name']) + "</h1>"
        self._widgets['des'].value = "<font color={}>".format(self.colors['des']) + str(data['des']) + "</font>"
        self._widgets['industry'].value = '<p style="color: {};font-size:20px">Industry: '.format(self.colors['industry']) + str(data['industry']) + "</p>"
        self._widgets['internal_score'].update(data['internal_score'])

    def __update_tables(self, data):
        self._widgets['tbl'].update_grid_data(data['tbl_data'])
        self._widgets['peer_tbl'].update_grid_data(data['peer_data'])
        self._widgets['Tab'].children = [self._widgets['tbl'],self._widgets['peer_tbl']]
        self._widgets['Tab'].set_title(0,'Security')
        self._widgets['Tab'].set_title(1,'Peers')

    def __update_third_party_rating(self, data):
        self._widgets['thirdparty'].update(data["third_party_score"],data['third_party_score_date'],self.colors['third_party'])

    def update_colors(self,new_colors):
        '''Public Function'''
        try:
            self._widgets['name'].value = '<h1  style="color: {}">'.format(new_colors['name']) +  str(self.sec_data['name']) + "</h1>"
            self._widgets['des'].value = "<font color={}>".format(new_colors['des']) + str(self.sec_data['des']) + "</font>"
            self._widgets['industry'].value = '<p style="color: {};font-size:20px">Industry: '.format(new_colors['industry']) + str(self.sec_data['industry']) + "</p>"
            self._widgets['thirdparty'].update(self._widgets['thirdparty'].score,self._widgets['thirdparty'].date,new_colors['third_party'])
        except TypeError:
            print("Need to Run Report First!")

    def __run_btn_call_back(self, caller = None):

        self._toggle_children([
            self._widgets["title"],
            self._widgets['ticker_and_btn'],
            self._widgets['loading']
        ])
        ticker = self._widgets['ticker_input'].value
        self.sec_data = calc_functions.arrange_data_for_gui(ticker,self.data,self.column_mappings)
        self.__update(self.sec_data)
        self._toggle_children([
            self._widgets["title"],
            self._widgets['ticker_and_btn'],
            self._widgets['des_box'],
            self._widgets['Tab']
        ])
