from abc import ABCMeta, abstractmethod, ABC
import pandas as pd
import numpy as np
import bqplot as bqp
from bqdash.base_dashboard import BaseDashBoard
from ipywidgets import HTML, Output, VBox, HBox, Button, Image,Tab, Dropdown, Layout, ToggleButtons
import bqdash.calc_functions as calc_functions
from bqdash.custom_widgets import HeatMap, Scatter,BarPlot,LinePlot,HistPlot, ThirdPartyRatings, InternalRatings, Quartiles, DataGrid
from collections import OrderedDict

class ScoringDashboard(BaseDashBoard):

    def __init__(self,df=None,colors={'distribution':'#008616','median':'#E75480','scatter':'dodgerblue'}, title='Factor Scoring Dashboard', column_mappings=None):

        # Allow instantiation without dataframe
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame([0, 0], columns=['0'])

        super().__init__(df=df, colors=colors, title=title, column_mappings=column_mappings)

        self.__read_col_mapping(column_mappings)
        self.score_df = df.reset_index().set_index(self.id_field)
        self.score_df[self.date_field] = self.score_df[self.date_field].dt.strftime('%Y-%m-%d')
        self.selected_stocks = []
        self.dates = list(self.score_df[self.date_field].unique())
        self.date_count = len(self.dates)
        self.scores_on_each_date = OrderedDict([(name,group) for name,group in self.score_df.groupby(self.date_field,sort=False)])
        self.score_history_df = self.__compute_score_hist_df(self.score_df)
        self.score_latest_df = self.scores_on_each_date[max(self.dates)][[self.total_field]]
        self.score_sector_df = self.__compute_sector_df(max(self.dates))

        self.scatter_selected = []
        self.colors=colors
        self.__build_all()
        self.__update_grid()

    def __read_col_mapping(self,col_mappings):
        self.id_field = col_mappings['id_field']
        self.group_field = col_mappings['group_field']
        self.total_field = col_mappings['total_score_field']
        self.date_field = col_mappings['date_field']
        self.factor_fields = col_mappings['factor_score_fields']
        self.display_fields= [self.id_field,self.group_field,self.total_field]

    def __compute_sector_df(self,date):
        return self.scores_on_each_date[date][[self.group_field,self.total_field]].groupby(self.group_field).median().sort_values(self.total_field,ascending=False)[[self.total_field]]

    def __compute_score_hist_df(self,score_df):
        return score_df.reset_index().pivot_table(index=self.id_field,columns=self.date_field,values=self.total_field,aggfunc = max)

    def __build_all(self):
        chart_box = self.__build_charts()
        grid_box = self.__build_grid()

        self.children = [self.widgets['title'],
                         chart_box,
                         grid_box,
                         self.widgets['trend_chart_box']]

        self.layout=Layout(width='99%')

    def __build_charts(self):
        # Histogram for distribution of current composite score
        self.widgets['hist_plot'] = HistPlot(title='Distribution',bins=10,colors=[self.colors['distribution']], tick_format='0.0f')
        self.widgets['hist_plot'].push(self.score_latest_df)
        self.widgets['hist_plot'].widgets['mark_hist'].observe(self.__hist_plot_on_select, 'selected')
        # Sector median bar chart
        self.widgets['bar_plot'] = BarPlot(title='Median', orientation='horizontal', padding=0.3,colors=[self.colors['median']])
        self.widgets['bar_plot'].push(self.score_sector_df)
        self.widgets['bar_plot'].widgets['mark_bar'].observe(self.__bar_plot_on_select, 'selected')
        # Historical Trend Chart
        self.widgets['trend_chart'] = LinePlot(title='Composite Scores Trend')
        self.widgets['trend_chart_box'] = VBox([self.widgets['trend_chart'].show()],layout={'display':'none','height':'300px','width': '75%','overflow_y':'hidden', 'overflow_x':'hidden','margin':'0 0 0 200px'})
        #Scatter plot for historical dates
        self.widgets['scatter_plot'] = Scatter(title='History',colors=[self.colors['scatter']])
        self.widgets['scatter_plot'].widgets['mark_scatter'].on_element_click(self.__scatter_on_select)
        self.widgets['scatter_plot'].widgets['mark_scatter'].on_background_click(self.__background_callback)
        self.widgets['scatter_label'] = HTML('Click a point to generate a time series chart below the table',layout={'margin':'0 0 0 280px'})
        self.widgets['scatter_plot_box'] = VBox([self.widgets['scatter_label'],self.widgets['scatter_plot'].show()], layout={'width': '50%','overflow_x':'hidden'})
        self.__set_chart_configs()
        if self.date_count == 1:
            self.widgets['bar_plot_box'] = VBox([self.widgets['hist_plot'].show(), self.widgets['bar_plot'].show()], layout={'height':'50%','width': '100%', 'overflow_x':'hidden'})
            return HBox([self.widgets['bar_plot_box']])
        else:
            self.widgets['scatter_plot'].push(self.score_history_df)
            self.widgets['bar_plot_box'] = VBox([self.widgets['hist_plot'].show(), self.widgets['bar_plot'].show()], layout={'height':'50%','width': '50%', 'overflow_x':'hidden'})
            return HBox([self.widgets['bar_plot_box'],self.widgets['scatter_plot_box']])

    # Common configurations among histogram and sector median bar charts
    def __set_chart_configs(self):
        self.widgets['hist_plot'].figure.fig_margin = {'bottom': 20, 'left': 40, 'right': 20, 'top': 20}
        self.widgets['bar_plot'].figure.fig_margin = {'bottom': 20, 'left': 170, 'right': 20, 'top': 20}
        self.widgets['hist_plot'].widgets['mark_hist'].selected_style = self.widgets['bar_plot'].widgets['mark_bar'].selected_style =  {'opacity': 1.0}
        self.widgets['hist_plot'].widgets['mark_hist'].unselected_style = self.widgets['bar_plot'].widgets['mark_bar'].unselected_style = {'opacity': 0.3}
        self.widgets['hist_plot'].widgets['hist_view'].layout = self.widgets['bar_plot'].widgets['bar_view'].layout = Layout(overflow_x='hidden')
        self.widgets['hist_plot'].figure.layout = self.widgets['bar_plot'].figure.layout=self.widgets['trend_chart'].layout = {'height': '250px', 'width': '100%'}
        self.widgets['trend_chart'].figure.layout = {'height': '300px','overflow_y':'hidden'}
        self.widgets['hist_plot'].widgets['axis_y'].grid_lines = self.widgets['bar_plot'].widgets['axis_x'].grid_lines = 'none'
        self.widgets['hist_plot'].widgets['axis_x'].grid_lines = self.widgets['bar_plot'].widgets['axis_y'].grid_lines = 'dashed'
        self.widgets['hist_plot'].widgets['mark_hist'].interactions = self.widgets['bar_plot'].widgets['mark_bar'].interactions = {'click': 'select'}
        self.widgets['scatter_plot'].figure.height = '450px'
        self.widgets['scatter_plot'].figure.fig_margin = {'bottom': 40, 'left': 80, 'right': 40, 'top': 40}
        self.widgets['scatter_plot'].widgets['mark_scatter'].interactions={'click': 'select','hover':'tooltip'}
        self.widgets['scatter_plot'].widgets['mark_scatter'].selected_style={'opacity': 1.0, 'fill': 'DarkOrange', 'stroke': 'Red'}
        self.widgets['scatter_plot'].widgets['mark_scatter'].unselected_style={'opacity': 0.5}
        self.widgets['scatter_plot'].widgets['axis_x'].grid_lines  = 'dashed'
        self.widgets['scatter_plot'].widgets['axis_y'].grid_lines  = 'dashed'

    def update_colors(self,new_colors):
        '''pubic function'''
        self.widgets['hist_plot'].widgets['mark_hist'].colors = [new_colors['distribution']]
        self.widgets['bar_plot'].widgets['mark_bar'].colors = [new_colors['median']]
        self.widgets['scatter_plot'].widgets['mark_scatter'].colors = [new_colors['scatter']]

    def __build_grid(self):
        self.widgets['date_toggle'] = ToggleButtons(options=self.dates, description='As Of')
        self.widgets['date_toggle'].observe(lambda x: self.__date_toggle_callback(), 'value')

        # Detail grid
        company_cols = [{'headerName': f, 'field': f, 'width': 180,'pinned':'left'} for f in self.display_fields]
        score_cols = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 100,'cellStyle': calc_functions.highlight_positive()} for f in self.factor_fields]

        column_defs = [
            {'headerName': 'Company', 'children': company_cols},
            {'headerName': 'Factors', 'children': score_cols}
        ]

        self.widgets['grid'] = DataGrid(column_defs=column_defs)

        return VBox([self.widgets['date_toggle'],
                     self.widgets['grid']], layout={'width': '100%', 'margin': '20px 0px 0px 0px', 'overflow_x':'hidden'})

    def __date_toggle_callback(self):
        self.update_grid()
        date = self.widgets['date_toggle'].value
        self.widgets['hist_plot'].push(self.scores_on_each_date[date][[self.total_field]])
        self.widgets['bar_plot'].push(self.__compute_sector_df(date))
        #self.set_chart_configs()

    def __hist_plot_on_select(self,event):
        del self.selected_stocks[:]
        self.widgets['bar_plot'].widgets['mark_bar'].selected = None
        index_selected = self.widgets['hist_plot'].widgets['mark_hist'].selected

        if index_selected is not None:
            self.selected_stocks.extend(self.score_latest_df.iloc[index_selected].index.tolist())
        else:
            self.selected_stocks.extend(self.score_latest_df.index)

        self.update_grid()

    # Actions when user selects on sector median bar plot
    def __bar_plot_on_select(self,event):
        self.widgets['hist_plot'].widgets['mark_hist'].selected= None
        index_selected = self.widgets['bar_plot'].widgets['mark_bar'].selected

        if index_selected is not None:
            selected_sectors = self.score_sector_df.index[index_selected]
        else:
            selected_sectors = self.score_sector_df.index

        del self.selected_stocks[:]
        self.selected_stocks.extend(self.score_df[self.score_df.Sector.isin(selected_sectors)].index.values)

        self.__update_grid()

    # Actions when user selects on scatter plot
    def __scatter_on_select(self,mark,event):
        new_select = (event['data']['index'])
        if new_select not in self.scatter_selected:
           self.scatter_selected.append(event['data']['index'])
        self.__update_trend_chart()

    def __update_trend_chart(self):
       score_trend_df  = self.score_history_df.loc[list(self.score_history_df.iloc[self.scatter_selected].index)]
       self.widgets['trend_chart'].push(score_trend_df.T)
       self.widgets['trend_chart'].widgets['axis_x'].grid_lines = 'dashed'
       self.widgets['trend_chart'].widgets['axis_y'].grid_lines = 'none'
       self.widgets['trend_chart_box'].layout.display = ''

    def __background_callback(self,mark,target):
        self.scatter_selected = []
        self.__update_trend_chart()
        self.widgets['trend_chart_box'].layout.display = 'none'

    def __update_grid(self):
        date = self.widgets['date_toggle'].value
        # Filter by as of date
        score_asof_df_temp = self.scores_on_each_date[date]
        score_asof_df = score_asof_df_temp.copy(deep=True)

        # Filter by selected stocks
        # If no selection, then show everything
        if self.selected_stocks:
            score_asof_df = score_asof_df[score_asof_df.index.isin(self.selected_stocks)]

        #score_asof_df['ID'] = score_asof_df.index
        self.widgets['grid'].update_grid_data(score_asof_df.reset_index())

class PortfolioDashboard(BaseDashBoard):

    def __init__(self,df=None,colors='RdPu', title='Portfolio Dashboard', column_mappings=None):

        self.__read_col_mapping(column_mappings)
        # Allow instantiation without dataframe
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame([0, 0], columns=['0'])

        super().__init__(df=df, colors=colors, title=title, column_mappings=column_mappings)
        self.data = df
        self.data['Active (%)'] = self.data[self.port_field] - self.data[self.index_field]
        self.colors = colors
        self.__build_all()
        self.update_heatmap()

    def __read_col_mapping(self,col_mappings):
        self.id_field = col_mappings['id_field']
        self.groups = col_mappings['group_field']
        self.port_field = col_mappings['port_field']
        self.index_field = col_mappings['index_field']

    def __build_all(self):

        # HeatMap
        # Create dropown widgets
        self.widgets['dropdown_x'] = Dropdown(description='X axis',options=self.groups)
        self.widgets['dropdown_x'].value = self.groups[0]
        self.widgets['dropdown_y'] = Dropdown(description='Y axis',options=self.groups)
        self.widgets['dropdown_y'].value = self.groups[1]
        self.widgets['dropdown_z'] = Dropdown(description='Type',options=[self.port_field,self.index_field,'Active (%)'])

        # Bind callback to the dropdown widgets
        self.widgets['dropdown_x'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_y'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_z'].observe(self._update_plot, names=['value'])

        # Create Box containers
        self.widgets['settings'] = HBox([self.widgets['dropdown_z'],self.widgets['dropdown_x'], self.widgets['dropdown_y']],
                                        layout={'margin':'0 0 0 130px'})
        self.widgets['Heatmap'] = HeatMap(color_scale=self.colors,callback=self.__update_transparency_table)
        self.widgets['transparency_lbl'] = HTML('<p style="color: #F2F3F4;font-size:30px">Portfolio Holdings</p>',layout={'overflow_x':'visible','overflow_y':'visible','display':'none'})
        self.widgets['portfolio_grid_error'] = HTML('<p style="color: #F7DC6F;font-size:20px">Error: Same Grouping Selected</p>')
        self.widgets['portfolio_table_error'] = HTML('<p style="color: #F7DC6F;font-size:20px">Portfolio Contains No Stocks in this Allocation</p>')
        self.widgets['portfolio_table'] = DataGrid()#HTML()
        self.widgets['port_table_box'] = VBox([self.widgets['portfolio_table']],layout={'min_height':'250px','display':'none'})
        # Summary tables
        self.widgets['g1_summary'] = HTML(layout={'overflow_x':'visible','overflow_y':'auto','min_width':'450px','max_height':'500px','margin':'0 15px 0 0'})
        self.widgets['g2_summary'] = HTML(layout={'overflow_x':'visible','overflow_y':'auto','min_width':'450px','max_height':'500px','margin':'0 0 0 0'})

        # create the tab view
        form_summary = HBox([self.widgets['g1_summary'],
                             self.widgets['g2_summary']],
                          layout={'overflow_x':'visible','overflow_y':'visible','max_height':'500px','margin':'0 0 2px 5px'})

        self.widgets['form_heatmap'] = VBox([self.widgets['settings'],
                                             self.widgets['Heatmap'].show(),
                                             self.widgets['transparency_lbl'],
                                             self.widgets['port_table_box']])

        self.widgets['tab'] = Tab(layout={'margin':'0 0 5px 0'})
        self.widgets['tab'].children = [self.widgets['form_heatmap']]
        self.widgets['tab'].set_title(0, 'Heatmap')
        #self.widgets['tab'].set_title(1, 'Summary')

        self.children = [
            self.widgets['title'],
            self.widgets['form_heatmap']
        ]

    def update_heatmap(self):
        self.__toggle_loading()
        self.widgets['Heatmap'].push(self.data,
                                     self.widgets['dropdown_x'].value,
                                     self.widgets['dropdown_y'].value,
                                     self.widgets['dropdown_z'].value)
        self.__toggle_ready()

    def _update_plot(self,evt):
        '''callback function for dropdown widgets'''
        try:
            if evt is not None and evt['new'] is not None and evt['old'] is not None:
                new_value = evt['new']
                self.widgets['Heatmap'].widgets['fig'].layout.display = 'none'
                self.widgets['transparency_lbl'].layout.display = 'none'
                self.widgets['port_table_box'].layout.display = 'none'
                self.widgets['portfolio_table'] = None
                self.update_heatmap()
        except ValueError:
            self.__toggle_error()

        self.widgets['Heatmap'].widgets['fig'].layout.display = ''

    def __update_transparency_table(self,chart,target):
        self.widgets['transparency_lbl'].layout.display = ''
        self.widgets['port_table_box'].layout.display = ''
        group1 = self.widgets['dropdown_x'].value
        group2 = self.widgets['dropdown_y'].value
        grid_data = self.data.groupby(by=[group1,group2]).sum().unstack().stack(dropna=False).fillna(0)
        grid_data = grid_data.reset_index().pivot(index=group2,columns=group1,values=self.port_field)
        try:
            columns = list(grid_data.columns)[target['data']['column']]
            rows = list(grid_data.index)[target['data']['row']]
            transparency_df = self.__get_table_data(group1,group2)
            column_defs = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150} for f in transparency_df[columns,rows].columns]
            self.widgets['portfolio_table'] = DataGrid(df =transparency_df[columns,rows].round(2), column_defs=column_defs)
            self.widgets['port_table_box'].children = [self.widgets['portfolio_table']]
        except:
            self.widgets['port_table_box'].children = [self.widgets['portfolio_table_error']]

    def __get_table_data(self,group1,group2):
        portfolio = self.data.copy(deep=True)
        portfolio = portfolio[pd.notnull(portfolio[self.port_field])]
        portfolio[[self.port_field, self.index_field,'Active (%)']] = portfolio[[self.port_field, self.index_field,'Active (%)']].fillna(value=0)
        portfolio = portfolio.reset_index()
        portfolio= portfolio[[self.id_field,group1,group2,self.port_field, self.index_field,'Active (%)']]
        region_list = {key:val for key,val in portfolio.groupby(by=[group1,group2])}
        return region_list

    def __toggle_loading(self):
        # loading indicator
        self.widgets['form_heatmap'].children=[self.widgets['settings'],
                                                self.widgets['loading']]

    def __toggle_error(self):
        # loading indicator
        self.widgets['form_heatmap'].children=[self.widgets['settings'],
                                               self.widgets['portfolio_grid_error']]

    def __toggle_ready(self):
        self.widgets['form_heatmap'].children=[self.widgets['settings'],
                                                self.widgets['Heatmap'].show(),
                                                self.widgets['transparency_lbl'],
                                                self.widgets['port_table_box']]

class EsgDashboard(BaseDashBoard):

    def __init__(self,df=None,colors=[], title='ESG Dashboard',ratings_scale=None,column_mappings=None):

        # Allow instantiation without dataframe
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame([0, 0], columns=['0'])

        super().__init__(df=df, colors=colors, title=title, column_mappings=column_mappings)
        self.__read_col_mapping(column_mappings)
        if df.index.is_numeric():
            self.data = df.set_index(self.id_field)
        else:
            self.data = df.reset_index().set_index(self.id_field)
        self.securities = list(self.data.index.values)
        self.ratings_scale = ratings_scale
        self.__build_all()

    def __read_col_mapping(self,col_mappings):
        self.id_field = col_mappings['id_field']
        self.description_field = col_mappings['description_field']
        self.sector_field = col_mappings['sector_field']
        self.internal_score = col_mappings['internal_score']
        self.third_party_score = col_mappings['third_party_score']
        self.third_party_score_date = col_mappings['third_party_score_date']
        self.factors = col_mappings['factor_score_fields']

    def __build_all(self):

        # ticker input
        self.widgets['ticker_and_btn'] = self.__build_ticker_and_btn()
        # name and des
        name_and_des = self.__build_name_and_des()
        #company info
        third_party_rating = self.__build_third_party_rating()
        self.widgets['des_box'] = HBox([name_and_des, third_party_rating])

        column_defs_single = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150,'cellStyle': calc_functions.highlight_scores()} for f in self.factors]
        column_defs_peers = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 150,'cellStyle': calc_functions.highlight_scores()} for f in [self.id_field] + self.factors]

        self.widgets['tbl'] = DataGrid(column_defs=column_defs_single)
        self.widgets['peer_tbl'] = DataGrid(column_defs=column_defs_peers)
        self.widgets['Tab'] = Tab()

        self.children = [
            self.widgets['title'],
            self.widgets['ticker_and_btn']
        ]

    def __build_ticker_and_btn(self):
        self.widgets['ticker_input'] = Dropdown(options=self.securities)
        self.widgets['btn'] = Button(description = "Run Report")
        self.widgets['btn'].on_click(self.__run_btn_call_back)
        panel = HBox([self.widgets['ticker_input'],
                      self.widgets['btn']])
        return panel

    def __build_name_and_des(self):
        self.widgets['name'] = HTML()
        self.widgets['des'] = HTML()
        self.widgets['industry'] = HTML()
        self.widgets['internal_score'] = InternalRatings()
        self.widgets['internal_score'].layout = {'margin':'30px 0 0 0'}
        panel = VBox([self.widgets['name'],
                      self.widgets['industry'],
                      self.widgets['des'],
                      self.widgets['internal_score']
                      ])
        # layout
        panel.layout.width = "50%"
        return panel

    def __build_third_party_rating(self):

        self.widgets['thirdparty'] = ThirdPartyRatings(self.ratings_scale)
        self.widgets['thirdparty'].layout.max_height = "300px"
        self.widgets['thirdparty'].layout.width = "100%"
        self.widgets['thirdparty'].layout.margin = '0 0 0 20px'
        panel = VBox([self.widgets['thirdparty']])
        panel.layout.width = "50%"
        panel.layout.overflow_x = "hidden"
        return panel

    def __update(self, data):
        self.__update_name_and_des(data)
        self.__update_third_party_rating(data)
        self.__update_tables(data)

    def __update_name_and_des(self, data):
        self.widgets['name'].value = '<h1  style="color: #F6980A">' +  str(data['name']) + "</h1>"
        self.widgets['des'].value = "<font color=#CFB010>" + str(data['des']) + "</font>"
        self.widgets['industry'].value = '<p style="color: #fffff;font-size:20px">Industry: ' + str(data['industry']) + "</p>"
        self.widgets['internal_score'].update(data['internal_score'])

    def __update_tables(self, data):
        self.widgets['tbl'].update_grid_data(data['tbl_data'])
        self.widgets['peer_tbl'].update_grid_data(data['peer_data'])
        self.widgets['Tab'].children = [self.widgets['tbl'],self.widgets['peer_tbl']]
        self.widgets['Tab'].set_title(0,'Security')
        self.widgets['Tab'].set_title(1,'Peers')

    def __update_third_party_rating(self, data):
        self.widgets['thirdparty'].update(data["third_party_score"],data['third_party_score_date'])

    def __run_btn_call_back(self, caller = None):

        self.__toggle_loading()
        ticker = self.widgets['ticker_input'].value
        field_mapping = {'Name':self.id_field,
                         'Des':self.description_field,
                         'Sector':self.sector_field,
                         'internal_score':self.internal_score,
                         'third_party_score':self.third_party_score,
                         'third_party_score_date':self.third_party_score_date,
                         'factors':self.factors}

        sec_data = calc_functions.arrange_data_for_gui(ticker,self.data,field_mapping)
        self.__update(sec_data)
        self.__toggle_ready()

    def __toggle_loading(self):
        # loading indicator
        self.children = [
            self.widgets["title"],
            self.widgets['ticker_and_btn'],
            self.widgets['loading']
        ]

    def __toggle_ready(self):
        self.children = [
            self.widgets["title"],
            self.widgets['ticker_and_btn'],
            self.widgets['des_box'],
            self.widgets['Tab']
        ]
