import bqplot as bqp
import pandas as pd
import ipywidgets as ipw

class Scatter():
    
    def __init__(self):
        '''The constructor of scatter class.'''
        
        self.widgets = dict()
        self.df = None
        self._build_cht_view()
    
    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        scale_x = bqp.LinearScale()
        scale_y = bqp.LinearScale()
        
        # Create the Mark
        self.widgets['tooltip'] = bqp.Tooltip(fields=['name','x', 'y'],formats=['','.2f', '.2f'])
        self.widgets['mark_scatter'] = bqp.Scatter(scales = {'x': scale_x, 'y': scale_y},
                                                   tooltip = self.widgets['tooltip'],
                                                   display_names = False,
                                                   interactions={'click': 'select','hover':'tooltip'},
                                                   selected_style={'opacity': 1.0, 'fill': '#F6980A', 'stroke': '#9C0303'},
                                                   unselected_style={'opacity': 0.1})

        # Create the Axis
        self.widgets['axis_x'] = bqp.Axis(scale=scale_x)
        self.widgets['axis_y'] = bqp.Axis(scale=scale_y,
                                          orientation='vertical',
                                          tick_format='0.0f')

        self.figure = bqp.Figure(marks=[self.widgets['mark_scatter']],
                            axes=[self.widgets['axis_x'], self.widgets['axis_y']],
                            animation_duration=500,
                            padding_x=0.05,
                            padding_y=0.05,
                            fig_margin={'top': 50, 'bottom': 60,
                                        'left': 50, 'right':30})

        # Create dropown widgets
        self.widgets['dropdown_x'] = ipw.Dropdown(description='X axis')
        self.widgets['dropdown_y'] = ipw.Dropdown(description='Y axis')
       
        # Bind callback to the dropdown widgets
        self.widgets['dropdown_x'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_y'].observe(self._update_plot, names=['value'])
        
        # Create Box containers
        widget_box = ipw.HBox([self.widgets['dropdown_x'], self.widgets['dropdown_y']])
        self.widgets['scatter_view'] = ipw.VBox([self.figure, widget_box], layout={'width':'100%'})
        self.show()
    
    
    def push(self,df):
        '''populate chart with data'''
        
        self.df = df
        options = list(df.columns)
        options.sort()
        self.widgets['dropdown_x'].options = options
        self.widgets['dropdown_x'].value = options[0]
        self.widgets['axis_x'].label = options[0]
        self.widgets['dropdown_y'].options = options
        self.widgets['dropdown_y'].value = options[1]
        self.widgets['axis_y'].label = options[1]
        self.widgets['mark_scatter'].x = df[options[0]]
        self.widgets['mark_scatter'].y = df[options[1]]
        self.widgets['mark_scatter'].names = df.index
        
    def _update_plot(self,evt):
        '''callback function for dropdown widgets'''
        
        if evt is not None and evt['new'] is not None:
            new_value = evt['new']
            if evt['owner'] == self.widgets['dropdown_x']:
                self.widgets['mark_scatter'].x = self.df[new_value]
                self.widgets['axis_x'].label = new_value
            elif evt['owner'] == self.widgets['dropdown_y']:
                self.widgets['mark_scatter'].y = self.df[new_value]
                self.widgets['axis_y'].label = new_value
            self.widgets['tooltip'].labels=['Company', 
                                            self.widgets['dropdown_x'].value,
                                            self.widgets['dropdown_y'].value]
    
    # Display the visualization
    def show(self):
        '''Display the initial app UI.'''
        
        return self.widgets['scatter_view']

class HeatMap():

    def __init__(self):

        '''The constructor of heatmap class.'''
        
        self.widgets = dict()
        self.df = None
        self._build_cht_view()
    
    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        self.widgets['x_sc'] = bqp.OrdinalScale()
        self.widgets['y_sc'] = bqp.OrdinalScale()
        self.widgets['col_sc'] = bqp.ColorScale(scheme='YlGn')
        self.widgets['x_lb'] = bqp.OrdinalScale()
        self.widgets['y_lb'] = bqp.OrdinalScale(reverse=True)

        # Create the Axis
        self.widgets['ax_x'] = bqp.Axis(scale=self.widgets['x_lb'],tick_style={'font-size': 10,'text-anchor': 'end'},tick_rotate=-45)
        self.widgets['ax_y'] = bqp.Axis(scale=self.widgets['y_lb'], orientation='vertical',tick_style={'font-size': 10,'text-anchor': 'end'})


        # Create the Fig
        self.widgets['fig'] = bqp.Figure(marks=[], axes=[self.widgets['ax_x'], self.widgets['ax_y']], padding_y=0.0,
                            layout={'min_width':'1000px','min_height':'600px'},fig_margin={'top':50,'right':0,'bottom':150,'left':150})
        
        # Create dropown widgets
        self.widgets['dropdown_x'] = ipw.Dropdown(description='X axis')
        self.widgets['dropdown_y'] = ipw.Dropdown(description='Y axis')
        self.widgets['dropdown_z'] = ipw.Dropdown(description='Type',options=['% Wgt (Port)','% Wgt (Index)','Active Wgt'])
       
        # Bind callback to the dropdown widgets
        self.widgets['dropdown_x'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_y'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_z'].observe(self._update_plot, names=['value'])
        
        # Create Box containers
        widget_box = ipw.HBox([self.widgets['dropdown_z'],self.widgets['dropdown_x'], self.widgets['dropdown_y']])
        self.widgets['heat_map_view'] = ipw.VBox([widget_box,self.widgets['fig'] ], layout={'width':'100%'})
        self.show()
        #title = 'Portfolio Weight HeatMap (%)')

    def create_new_grid(self,x,y,z):
        temp_df = self.get_grid_map_data_from_df(self.df,x,y,z)

        self.widgets['grid_map'] = bqp.GridHeatMap(color=temp_df,scales={'column': self.widgets['x_sc'], 'row': self.widgets['y_sc'], 'color': self.widgets['col_sc']},interactions={'click':'select'},
                                   anchor_style={'fill':'##F5EEF8'})
        self.widgets['x_lb'].domain = list(temp_df.columns)
        self.widgets['y_lb'].domain = list(temp_df.index)
        self.widgets['x_sc'].domain = [x for x in range(len(list(temp_df.columns)))]
        self.widgets['y_sc'].domain = [x for x in range(len([x for x in temp_df.index]))]

        marks = [self.widgets['grid_map']]

        for row in range(temp_df.shape[0]):
            for col in range(temp_df.shape[1]):
                marks.append(bqp.Label(x=[col],
                                y=[row],
                                scales={'x': self.widgets['x_sc'], 'y': self.widgets['y_sc']},
                                text=[str(round(temp_df.iloc[row, col], 2)) + '%'],
                                align='middle',
                                default_size=8,
                                font_weight='bolder',
                                colors=['black']))
        self.widgets['fig'].marks=marks

    def push(self,df,groups):
            
        self.df = df
        options = groups
        self.widgets['dropdown_x'].options = options
        self.widgets['dropdown_x'].value = options[0]
        self.widgets['ax_x'].label = options[0]
        self.widgets['dropdown_y'].options = options
        self.widgets['dropdown_y'].value = options[1]
        self.widgets['ax_y'].label = options[1]
        self.create_new_grid(self.widgets['dropdown_x'].value,
                             self.widgets['dropdown_y'].value,
                             self.widgets['dropdown_z'].value)

       

    def get_grid_map_data_from_df(self,df,group1,group2,weight_type):
        totals = df.groupby(by=[group1,group2]).sum().unstack().stack(dropna=False).fillna(0)
        totals['Active Wgt'] = totals['% Wgt (Port)'] - totals['% Wgt (Index)']
        return totals.reset_index().pivot(index=group1,columns=group2,values=weight_type)


    def _update_plot(self,evt):
        '''callback function for dropdown widgets'''
        
        if evt is not None and evt['new'] is not None and evt['old'] is not None:
            new_value = evt['new']
            self.widgets['fig'].layout.display = 'none'
            if evt['owner'] == self.widgets['dropdown_x']:
                self.create_new_grid(self.widgets['dropdown_x'].value,
                                     self.widgets['dropdown_y'].value,
                                     self.widgets['dropdown_z'].value)
                self.widgets['ax_x'].label = new_value
            elif evt['owner'] == self.widgets['dropdown_y']:
                self.create_new_grid(self.widgets['dropdown_x'].value,
                                     self.widgets['dropdown_y'].value,
                                     self.widgets['dropdown_z'].value)
                self.widgets['ax_y'].label = new_value
            else:
                self.create_new_grid(self.widgets['dropdown_x'].value,
                                     self.widgets['dropdown_y'].value,
                                     self.widgets['dropdown_z'].value)
            self.widgets['fig'].layout.display = ''

    # Display the visualization
    def show(self):
        '''Display the initial app UI.'''
        
        return self.widgets['heat_map_view']
             
