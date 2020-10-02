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
        
        
        self.widgets['tooltip'] = bqp.Tooltip(fields=['name','x', 'y'],formats=['','.2f', '.2f'])
        self.widgets['mark_scatter'] = bqp.Scatter(scales = {'x': scale_x, 'y': scale_y},
                                                   tooltip = self.widgets['tooltip'],
                                                   display_names = False) 
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
