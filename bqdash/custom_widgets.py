import bqplot as bqp
import pandas as pd
from ipywidgets import HTML, VBox, HBox, Button,Dropdown
from ipyaggrid import Grid
import bqdash.calc_functions as calc_functions
import six

class BarPlot():

    def __init__(self,title='',orientation='horizontal',colors=['#E75480'],padding=0.3):
        '''The constructor of the BarPlot class.'''
        self.widgets = dict()
        self.df = None
        self.title = title
        self.colors=colors
        self.orientation = orientation
        self.padding = padding
        self._build_cht_view()
        self.show()

    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        scale_x = bqp.OrdinalScale()
        scale_y = bqp.LinearScale()

        # Create the Mark
        self.widgets['tooltip'] = bqp.Tooltip(fields=['x', 'y'],formats=['', '.2f'])
        self.widgets['mark_bar'] = bqp.Bars(scales = {'x': scale_x, 'y': scale_y},
                                                   tooltip = self.widgets['tooltip'],
                                                   orientation=self.orientation,colors=self.colors,
                                                   padding=self.padding)

        if self.orientation == 'horizontal':
            x_orientation = 'vertical'
            y_orientation = 'horizontal'
        else:
            x_orientation='horizontal'
            y_orientation = 'vertical'
        # Create the Axis
        self.widgets['axis_x'] = bqp.Axis(scale=scale_x,orientation=x_orientation)
        self.widgets['axis_y'] = bqp.Axis(scale=scale_y,orientation=y_orientation,tick_format='0.0f')

        self.figure = bqp.Figure(title=self.title,marks=[self.widgets['mark_bar']],
                                axes=[self.widgets['axis_x'], self.widgets['axis_y']],
                                animation_duration=500,
                                padding_x=0.05,
                                padding_y=0.05)

        # Create Box containers
        self.widgets['bar_view'] = VBox([self.figure])


    def push(self,df):
        '''populate chart with data'''
        self.df = df
        self.widgets['mark_bar'].x = self.df.index
        self.widgets['mark_bar'].y = self.df.iloc[:,-1]

    # Display the visualization
    def show(self):
        '''Display the initial app UI.'''
        return self.widgets['bar_view']

class HistPlot():

    def __init__(self,title='',bins=10,colors=['#E75480'], tick_format='0.0',normalized=False):
        '''The constructor of the HistPlot class.'''
        self.widgets = dict()
        self.df = None
        self.title = title
        self.colors=colors
        self.bins = bins
        self.tick_format = tick_format
        self.normalized = normalized
        self._build_cht_view()
        self.show()

    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        scale_x = bqp.LinearScale()
        scale_y = bqp.LinearScale(min=0, allow_padding=False)

        # Create the Mark
        self.widgets['tooltip'] = bqp.Tooltip(fields=['x', 'y'],formats=['', '.2f'])
        self.widgets['mark_hist'] = bqp.Hist(scales = {'sample': scale_x, 'count': scale_y},
                                                   tooltip = self.widgets['tooltip'],
                                                   bins=self.bins,colors=self.colors,
                                                   normalized=self.normalized)

        # Create the Axis
        self.widgets['axis_x'] = bqp.Axis(scale=scale_x)
        self.widgets['axis_y'] = bqp.Axis(scale=scale_y,tick_format=self.tick_format,orientation='vertical')

        self.figure = bqp.Figure(title=self.title,marks=[self.widgets['mark_hist']],
                                axes=[self.widgets['axis_x'], self.widgets['axis_y']],
                                animation_duration=500)

        # Create Box containers
        self.widgets['hist_view'] = VBox([self.figure])


    def push(self,df):
        '''populate chart with data'''
        self.df = df
        self.widgets['mark_hist'].sample = self.df[self.df.columns[0]]

    # Display the visualization
    def show(self):
        '''Display the initial app UI.'''
        return self.widgets['hist_view']

class LinePlot():

    def __init__(self,title='',legend=True):
        '''The constructor of the LinePlot class.'''
        self.widgets = dict()
        self.df = None
        self.title = title
        self.legend = legend
        self._build_cht_view()
        self.show()

    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        scale_x = bqp.OrdinalScale()
        scale_y = bqp.LinearScale()

        # Create the Mark
        self.widgets['mark_line'] = bqp.Lines(scales = {'x': scale_x, 'y': scale_y},display_legend=self.legend)

        self.widgets['axis_x'] = bqp.Axis(scale=scale_x)
        self.widgets['axis_y'] = bqp.Axis(scale=scale_y,tick_format='0.2f',orientation='vertical')

        self.figure = bqp.Figure(title=self.title,marks=[self.widgets['mark_line']],
                                axes=[self.widgets['axis_x'], self.widgets['axis_y']],
                                animation_duration=500)

        # Create Box containers
        self.widgets['line_view'] = VBox([self.figure])


    def _get_x_scale(self, val):
        """Returns the appropriate Scale type for the index data type"""

        if isinstance(val, six.string_types):
            return bqp.OrdinalScale

        elif isinstance(val, dt.date):
            return bqp.DateScale

        elif isinstance(val, dt.datetime):
            return bqp.DateScale

        elif isinstance(val, np.datetime64):
            return bqp.DateScale

        elif isinstance(val, pd.Timestamp):
            return bqp.DateScale

        elif isinstance(val, (int, float, complex)):
            return bqp.LinearScale

        elif np.issubdtype(val, np.number):
            return bqp.LinearScale

        else:
            raise ValueError("'{}' is not a valid axis data type.".format(val))

    def push(self,df):
        '''populate chart with data'''
        self.df = df
        self.widgets['mark_line'].x = self.df.index.to_list()
        self.widgets['mark_line'].y = [self.df[col] for col in self.df]
        self.widgets['mark_line'].labels = self.df.columns.to_list()

    # Display the visualization
    def show(self):
        '''Display the initial app UI.'''
        return self.widgets['line_view']

class Scatter():

    def __init__(self,title='Scatter',colors=['dodgerblue']):
        '''The constructor of scatter class.'''

        self.widgets = dict()
        self.df = None
        self.title = title
        self.colors = colors
        self._build_cht_view()
        self.show()

    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        scale_x = bqp.LinearScale()
        scale_y = bqp.LinearScale()

        # Create the Mark
        self.widgets['tooltip'] = bqp.Tooltip(fields=['name','x', 'y'],formats=['','.2f', '.2f'])
        self.widgets['mark_scatter'] = bqp.Scatter(scales = {'x': scale_x, 'y': scale_y},
                                                   tooltip = self.widgets['tooltip'],
                                                   stroke='white',
                                                   display_names=False,colors=self.colors)

        # Create the Axis
        self.widgets['axis_x'] = bqp.Axis(scale=scale_x)
        self.widgets['axis_y'] = bqp.Axis(scale=scale_y,
                                          orientation='vertical',
                                          tick_format='0.0f')

        self.figure = bqp.Figure(title=self.title,marks=[self.widgets['mark_scatter']],
                                axes=[self.widgets['axis_x'], self.widgets['axis_y']],
                                animation_duration=500,
                                padding_x=0.05,
                                padding_y=0.05)

        # Create dropown widgets
        self.widgets['dropdown_x'] = Dropdown(description='X axis')
        self.widgets['dropdown_y'] = Dropdown(description='Y axis')

        # Bind callback to the dropdown widgets
        self.widgets['dropdown_x'].observe(self._update_plot, names=['value'])
        self.widgets['dropdown_y'].observe(self._update_plot, names=['value'])

        # Create Box containers
        widget_box = HBox([self.widgets['dropdown_x'], self.widgets['dropdown_y']])
        self.widgets['scatter_view'] = VBox([self.figure, widget_box])



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
        self.widgets['mark_scatter'].x = self.df[options[0]]
        self.widgets['mark_scatter'].y = self.df[options[1]]
        self.widgets['mark_scatter'].names = self.df.index

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

    def __init__(self,color_scale='YlGn',callback=None):

        '''The constructor of heatmap class.'''
        self.widgets = dict()
        self.df = None
        self.callback = callback
        self.color_scale = color_scale
        self._build_cht_view()
        self.show()

    def _build_cht_view(self):
        '''function to build chart gui'''
        # Create scales
        self.widgets['x_sc'] = bqp.OrdinalScale()
        self.widgets['y_sc'] = bqp.OrdinalScale()
        self.widgets['col_sc'] = bqp.ColorScale(scheme=self.color_scale)
        self.widgets['x_lb'] = bqp.OrdinalScale()
        self.widgets['y_lb'] = bqp.OrdinalScale(reverse=True)
        # Create the Axis
        self.widgets['ax_x'] = bqp.Axis(scale=self.widgets['x_lb'],tick_style={'font-size': 10,'text-anchor': 'end'},tick_rotate=-45,label_offset='60px')
        self.widgets['ax_y'] = bqp.Axis(scale=self.widgets['y_lb'], orientation='vertical',tick_style={'font-size': 10,'text-anchor': 'end'},label_offset='80px')
        # Create the Fig
        self.widgets['fig'] = bqp.Figure(marks=[], axes=[self.widgets['ax_x'], self.widgets['ax_y']], padding_y=0.0,
                            layout={'width':'100%','height':'400px','overflow_x':'hidden'},fig_margin={'top':20,'right':0,'bottom':130,'left':130})
        self.widgets['heat_map_view'] = VBox([self.widgets['fig'] ], layout={'width':'80%','overflow_x':'hidden'})

    def create_new_grid(self,df):

        self.widgets['grid_map'] = bqp.GridHeatMap(color=df,scales={'column': self.widgets['x_sc'], 'row': self.widgets['y_sc'], 'color': self.widgets['col_sc']},
                                                   interactions={'click':'select'},anchor_style={'fill':'##F5EEF8'})#stroke='white',
        self.widgets['x_lb'].domain = list(df.columns)
        self.widgets['y_lb'].domain = list(df.index)
        self.widgets['x_sc'].domain = [x for x in range(len(list(df.columns)))]
        self.widgets['y_sc'].domain = [x for x in range(len([x for x in df.index]))]
        marks = [self.widgets['grid_map']]

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                marks.append(bqp.Label(x=[col],
                                y=[row],
                                scales={'x': self.widgets['x_sc'], 'y': self.widgets['y_sc']},
                                text=[str(round(df.iloc[row, col], 2)) + '%'],
                                align='middle',
                                default_size=8,
                                font_weight='bolder',
                                colors=['black']))
        self.widgets['fig'].marks=marks
        self.widgets['grid_map'].on_element_click(self.callback)

    def push(self,df,group1,group2,weight_type):
        self.df = df
        self.widgets['ax_x'].label = group1
        self.widgets['ax_y'].label = group2
        grid_df = calc_functions.get_grid_map_data_from_df(self.df,group1,group2,weight_type)
        self.create_new_grid(grid_df)

    # Display the visualization
    def show(self):
        return self.widgets['heat_map_view']


class ThirdPartyRatings(VBox):

    def __init__(self,text,ratings_scale,color='#F6980A'):
        self.ratings = ratings_scale
        self._color = color
        self._score = ''
        self._date = ''
        self._text = text
        self.upper = self._build_banner()
        self.lower = self._build_rating_buttons()
        self.date_widget = HTML()
        super().__init__(children = [self.upper,self.lower,self.date_widget])

    def _build_banner(self):
        html_label_text = '<p style="color: {};font-size:30px;line-height: 95px;">{}</p>'.format(self._color,self._text)

        html_score_text = '''<html>
              <head>
                <style>
                  .circle {
                          width: 100px;
                          height: 100px;
                          border-radius: 50%;
                          font-size: 40px;
                          color: #fffff;
                          line-height: 90px;
                          text-align: center;
                          background:  color
                        }
                </style>
              </head>
              <body>
                <div class="circle">thescore</div>
              </body>
            </html>'''.replace('thescore',self._score).replace('color',self._color)

        label = HTML(html_label_text)
        score_circle = HTML(html_score_text)

        score_box = [label,score_circle]
        return HBox(score_box)

    def _build_rating_buttons(self):
        children = [Button(description=rating,disabled=False,layout={'width':'50px'},style={'button_color' : self._color})  if rating == self._score else
                    Button(description=rating,disabled=False,layout={'width':'50px'},style={'button_color' : '#808080'}) for rating in self.ratings]
        return HBox(children)

    def update(self,score,date,color):
        self._color = color
        self._date = date
        self._score = score
        self.date_widget.value = '<p style="color: {};font-size:20px;">Last Updated: {}</p>'.format(self._color,self._date)
        self.upper = self._build_banner()
        self.lower = self._build_rating_buttons()
        self.children = [self.upper,self.lower,self.date_widget]

    @property
    def date(self):
        return self._date

    @property
    def score(self):
        return self._score

class InternalRatings(VBox):

    def __init__(self,text):

        self._text = text
        self.upper = self._build_banner('default')
        super().__init__(children = [self.upper])


    def _build_banner(self,score):

        html_label_text = '<p style="color: #fffff;font-size:25px;line-height: 45px;">{}</p>'.format(self._text)
        if score =='default' or score == '':
            colorone = '#808080'
            colortwo = '#808080'
            colorthree = '#808080'
        elif score ==1:
            colorone = '#93C02D'
            colortwo = '#808080'
            colorthree = '#808080'
        elif score ==2:
            colorone = '#808080'
            colortwo = '#ff751a'
            colorthree = '#808080'
        elif score ==3:
            colorone = '#808080'
            colortwo = '#808080'
            colorthree = '#ff1a1a'

        html_score_text = '''<html>
              <head>
                <style>
                  .circle0 {
                          width: 55px;
                          height: 55px;
                          border-radius: 50%;
                          font-size: 20px;
                          color: #fff;
                          line-height: 95px;
                          text-align: center;
                          display: inline-block;
                          background:  colorone
                        }
                    .circle1 {
                          width: 55px;
                          height: 55px;
                          border-radius: 50%;
                          font-size: 20px;
                          color: #fff;
                          line-height: 95px;
                          text-align: center;
                          display: inline-block;
                          background:  colortwo
                        }
                    .circle2 {
                          width: 55px;
                          height: 55px;
                          border-radius: 50%;
                          font-size: 20px;
                          color: #fff;
                          line-height: 95px;
                          text-align: center;
                          display: inline-block;
                          background:  colorthree
                        }
                </style>
              </head>
              <body>
                <span class="circle0"></span>
                <span class="circle1"></span>
                <span class="circle2"></span>
              </body>
            </html>'''.replace('colorone',colorone).replace('colortwo',colortwo).replace('colorthree',colorthree)
        label = HTML(html_label_text)
        score_circle = HTML(html_score_text)

        score_box = [label,score_circle]
        return HBox(score_box)

    def update(self,score):
        self.upper = self._build_banner(score)
        self.children = [self.upper]


class Quartiles(HBox):

    def __init__(self,score):
        if score == '':
            super().__init__(children = [])
        else:
            self.upper = self._build_banner(int(score))
            super().__init__(children = [self.upper])
            self.layout.margin = '13px 0 0 0'

    def _build_banner(self,score):
        if score ==4:
            color = 'red'
        elif score == 3:
            color= '#ff6600'
        elif score ==1:
            color= '#93C02D'
        else:
            color= 'DarkOrange'

        quartile_view = [Button(layout={'width':'10px','height':'10px'},style={'button_color' : color}) for x in range(score)]

        quartile_box = quartile_view
        return HBox(quartile_view)

class TableHTML():
    def format_frame(self,dataframe,subset,font_size,background_color):
        formatted_frame = (dataframe.replace(0,'-').style
                        #.format(dataframe_formats)
                        .set_table_attributes('class="table"')
                        .set_table_styles([{'selector': '.row_heading','props': [('display', 'none')]},
                                           {'selector': '.blank.level0','props': [('display', 'none')]},
                                           {'selector':'th','props' :[('text-align','center'),('overflow-wrap','break-word'),('background-color', '#B4B3B2'),('color', '#1a1a1a')]}])
                        .set_properties(**{'text-align':'center','overflow-wrap':'break-word','color':'black','font-size':font_size})#'white-space': 'nowrap'
                        .apply(self.color_percentiles_hi,subset=subset,background=background_color))
        return formatted_frame.render()

    def format_portfolio_frame(self,df):
        formatted_frame = (df.round(2).replace(0,'-').style
                        .set_table_attributes('class="table"')
                        .set_table_styles([{'selector': '.row_heading','props': [('display', 'none')]},
                                           {'selector': '.blank.level0','props': [('display', 'none')]},
                                           {'selector':'th','props' :[('text-align','center'),('white-space', 'nowrap'),('background-color', '#f2f2f2'),('width','200px'),('font-size', '12px'),('color', '#1a1a1a')]}])
                        .set_properties(**{'text-align':'center','white-space': 'nowrap','color':'white','font-size':'12px'}))

        return formatted_frame.render()

    def color_percentiles_hi(self,column,background=True):
        if not background:
            return ['' if val =='-' else 'color: red' if val > 3 else  'color: #ff6600'
                if val == 3 else 'color: #93C02D'
                if val == 1 else 'color: DarkOrange' for val in column]
        else:
            return ['' if val =='-' else 'background-color: red' if val > 3 else  'background-color: #ff6600'
                if val == 3 else 'background-color: #93C02D'
                if val == 1 else 'background-color: DarkOrange' for val in column]

class DataGrid(Grid):
    def __init__(self,column_defs={},df=pd.DataFrame([0, 0], columns=['0'])):
        super().__init__(grid_data=df,grid_options = {'columnDefs' : column_defs,
                                                      'enableSorting': True,
                                                      'enableFilter': True,
                                                      'enableColResize': True,
                                                      'enableRangeSelection': True,
                                                      'rowSelection':'multiple'},
                        theme='ag-theme-balham-dark')
