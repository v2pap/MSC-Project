import numpy as np
import pandas as pd

from collections import OrderedDict
from ipyaggrid import Grid as DataGrid
from bqviz import BarPlot, HistPlot, LinePlot
from ipywidgets import *
from bqplot import Tooltip
from bqplot.interacts import (
    FastIntervalSelector, IndexSelector, BrushIntervalSelector,
    BrushSelector, MultiSelector, LassoSelector, PanZoom, HandDraw)
from charts import Scatter

class scoring_model(VBox):
    
    def __init__(self,score_df):
        
        super().__init__()
        score_df['DATE'] = score_df['DATE'].dt.strftime('%Y-%m-%d')
        self.display_fields=['Name','Sector','Total Score']
        self.selected_stocks = []
        self.dates = list(score_df['DATE'].unique())
        self.score_df = score_df
        self.score_sector_df = score_df[score_df.DATE == score_df.DATE.max()][['Sector','Total Score']].groupby('Sector').median().sort_values('Total Score',ascending=False)[['Total Score']]
        names = [df[['Name']] for name,df in score_df.groupby('DATE')][0]
        temp_hist = score_df.reset_index().pivot(index='ID',columns='DATE',values='Total Score')
        self.score_history_df = temp_hist.join(names,how='left').reset_index().set_index('Name').drop(['ID'],axis=1)

        self.score_latest_df = score_df[score_df.DATE == score_df.DATE.max()][['Total Score']]
        self.scores_on_each_date = OrderedDict([(name,group) for name,group in self.score_df.groupby('DATE',sort=False)])
        
        
        # Histogram for distribution of current composite score
        self.hist_plot = HistPlot(df=self.score_latest_df, bins=10,colors=['#008616'], tick_format='0.0', layout={'width': '100%'})
        self.hist_plot._figure.fig_margin = {'bottom': 20, 'left': 30, 'right': 20, 'top': 20}

        # Sector median bar chart
        self.bar_plot = BarPlot(self.score_sector_df, title='Median', orientation='horizontal', legend=False, padding=0.3,colors=['#E75480'])
        self.bar_plot._figure.fig_margin = {'bottom': 20, 'left': 170, 'right': 20, 'top': 20}
        self.bar_plot._mark_main.selected_style = {'opacity': 1.0}
        self.bar_plot._mark_main.unselected_style = {'opacity': 0.3}
        self.bar_plot._container.layout = Layout(overflow_x='hidden')
        self.bar_plot._mark_main.observe(self.bar_plot_on_select, 'selected')
        
        # Common configurations among histogram and sector median bar charts
        self.hist_plot._figure.layout = self.bar_plot._figure.layout = {'height': '250px', 'width': '100%'}
        self.hist_plot._axis_x.grid_lines = self.bar_plot._axis_x.grid_lines = 'none'
        self.hist_plot._axis_y.grid_lines = self.bar_plot._axis_y.grid_lines = 'dashed'
        self.hist_plot._mark_main.interactions = self.bar_plot._mark_main.interactions = {'click': 'select'}
        self.bar_plot_box = VBox([self.hist_plot.show(), self.bar_plot.show()], layout={'width': '50%', 'overflow_x':'hidden'})
        self.hist_plot._mark_main.observe(self.hist_plot_on_select, 'selected')
        
        self.trend_chart = LinePlot(title='Composite Scores Trend',colors=['#008616'])#.set_style()
        self.trend_chart_box = HBox([self.trend_chart.show()],layout={'display':'none'})
        
        #Scatter plot for historical dates
        self.scatter_plot = Scatter()
        self.scatter_plot.widgets['mark_scatter'].on_element_click(self.scatter_on_select)
        self.scatter_plot.figure.title='History'
        self.scatter_plot.figure.height = '450px'
        self.scatter_plot.figure.fig_margin = {'bottom': 40, 'left': 80, 'right': 40, 'top': 40}
        self.scatter_plot.widgets['mark_scatter'].selected_style = {'opacity': 1.0}
        self.scatter_plot.widgets['mark_scatter'].unselected_style = {'opacity': 0.8}
        self.scatter_plot.push(self.score_history_df)
        self.scatter_plot_box = HBox([self.scatter_plot.show()], layout={'width': '50%','overflow_x':'hidden'})
        
        self.chart_box = HBox([self.bar_plot_box,self.scatter_plot_box]) 
        self.date_toggle = ToggleButtons(options=self.dates, description='As Of')
        self.date_toggle.observe(lambda x: self.update_grid(), 'value')
       

        # Detail grid
        company_cols = [{'headerName': 'ID', 'field':'ID', 'width': 130,'pinned':'left'}] \
                     + [{'headerName': f, 'field': f, 'width': 130,'pinned':'left'} for f in self.display_fields]
        
        score_cols = [{'headerName': f, 'field':f, 'type': 'numericColumn', 'width': 125} for f in self.score_df if f not in self.display_fields + ['Total Score','DATE']]
        
        column_defs = [
            {'headerName': 'Company', 'children': company_cols},
            {'headerName': 'Factors', 'children': score_cols}
        ]
        self.grid = DataGrid(grid_options = {
                                'columnDefs' : column_defs,
                                'enableSorting': True,
                                'enableFilter': True,
                                'enableColResize': True,
                                'enableRangeSelection': True,
                                'rowSelection':'multiple',
                                 
                            },theme='ag-theme-bootstrap')
        self.grid_box = VBox([self.date_toggle,self.grid], layout={'width': '100%', 'margin': '20px 0px 0px 0px', 'overflow_x':'hidden'})
    
       
        self.update_grid()
           
        self.children = [self.chart_box, self.grid_box,self.trend_chart_box]
        self.layout=Layout(width='99%')
        
        
    def hist_plot_on_select(self,event):
        del self.selected_stocks[:]
        self.bar_plot._mark_main.selected = None
        index_selected = self.hist_plot._mark_main.selected
        
        if index_selected is not None:
            self.selected_stocks.extend(self.score_latest_df.iloc[index_selected].index.tolist())
            
        else:
            self.selected_stocks.extend(self.score_latest_df.index)
            
        
        #self.selected_stocks.extend(self.score_df[self.score_df.Sector.isin(selected_sectors)].index.values)

        self.update_grid()

    # Actions when user selects on sector median bar plot
    def bar_plot_on_select(self,event):
        self.hist_plot._mark_main.selected= None
        index_selected = self.bar_plot._mark_main.selected
        
        if index_selected is not None:
            selected_sectors = self.score_sector_df.index[index_selected]
            
        else:
            selected_sectors = self.score_sector_df.index
            
        #self.selected_stocks.clear()
        del self.selected_stocks[:]
        self.selected_stocks.extend(self.score_df[self.score_df.Sector.isin(selected_sectors)].index.values)

        self.update_grid()
        
        # Actions when user selects on sector median bar plot
    def scatter_on_select(self,mark,event):
        if len(self.scatter_plot.widgets['mark_scatter'].selected):
            
           score_trend_df  = self.score_history_df.loc[list(self.score_history_df.iloc[self.scatter_plot.widgets['mark_scatter'].selected].index)]
           
           self.trend_chart.push(score_trend_df.T)
           self.trend_chart_box.layout.display = ''


    def to_excel(self):
        try:
            writer = pd.ExcelWriter('Data.xlsx')
            for key in self.scores_on_each_date:
                 self.scores_on_each_date[key].to_excel(writer, key)

            writer.save()
        except:
            raise ValueError('Please Close Excel Sheet called Data.xlsx.')

    
    def update_grid(self):
        date = self.date_toggle.value
        # Filter by as of date
        score_asof_df_temp = self.scores_on_each_date[date]
        score_asof_df = score_asof_df_temp.copy(deep=True)
        
        # Filter by selected stocks
        # If no selection, then show everything
        if self.selected_stocks:
            score_asof_df = score_asof_df[score_asof_df.index.isin(self.selected_stocks)]
            

        score_asof_df['ID'] = score_asof_df.index
     
        self.grid.update_grid_data(score_asof_df)
    