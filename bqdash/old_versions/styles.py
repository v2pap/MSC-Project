BB_CLRS_DARK = ['#FFFFFF', '#1B84ED', '#CF7DFF', '#FF5A00', '#00D3D6',
                '#008616', '#B31D83', '#FF1E3E', '#FF9E24', '#63B2FF',
                '#30C030', '#9B016A', '#FD5D5D', '#AAAAAA', '#FBE360',
                '#00A5E3', '#35B56C', '#AC1BE8', '#007575', '#D20000',
                '#1E6AB4', '#89A4C5', '#626262']

BB_CLRS_LIGHT = ['#000000', '#0073ff', '#fa5a28', '#c873ff', '#d7be00',
                 '#00c2d7', '#db8922', '#f328bb', '#50f06e', '#8f52b6',
                 '#b09b00', '#009eb0', '#c31834', '#fdac93', '#ae1d86',
                 '#00a223', '#66abff', '#ffc070', '#787878', '#e61e3c']

# Keeping this in the namespace to not break existing notebooks
BB_CLRS = BB_CLRS_DARK

BB_CLRS_AVG = ['#FFFFFF', '#FF1A93', '#78FF8F', '#FFDE2B']

BQV_STYLES = {'title': {'baseline-shift': '12', 'font-size': '18px',
                        'font-family': 'Arial Narrow, Arial, Helvetica, sans-serif'}}

BB_PLOT_CLR_SETS = {'dark':  {'grid_lines': 'dashed',
                              'line_color': 'white',
                              'grid_color': '#3c3c3c',
                              'background': {'fill': '#222222',
                                             'stroke': '#3c3c3c',
                                             'stroke-width': 1},
                              'plot_colors': BB_CLRS_DARK},
                    'light': {'grid_lines': 'solid',
                              'line_color': 'black',
                              'grid_color': '#ffffff',
                              'background': {'fill': '#f7f7f7',
                                             'stroke': '#ffffff',
                                             'stroke-width': 1},
                              'plot_colors': BB_CLRS_LIGHT}}

BQV_WIDTH = '99%'
BQV_LEFT_PADDING = '20px'

BQV_FIGSTYLE = {
    'general': {'legend_location': 'top-right',
                'padding_y': 0.16,
                'fig_margin': {'top': 20, 'bottom': 35,
                               'left': 55, 'right': 30},
                'layout': {'width': '99%', 'height': '300px', 'grid_area': 'plot'},
                'animation_duration': 500},
    'multicompare': {'padding_y': 0.25,
                     'fig_margin': {'top': 20, 'bottom': 35,
                                    'left': 55, 'right': 30},
                     'layout': {'width': '99%', 'height': '200px', 'grid_area': 'plot'},
                     'animation_duration': 500,
                     'min_aspect_ratio': 0.01,
                     'max_aspect_ratio': 100},
    'narrow': {'padding_y': 0.25,
               'fig_margin': {'top': 20, 'bottom': 35,
                              'left': 55, 'right': 30},
               'layout': {'width': '99%', 'height': '180px', 'grid_area': 'plot'},
               'animation_duration': 500},
    'cal_leftview': {'padding_y': 0.25,
                     'fig_margin': {'top': 20, 'bottom': 35,
                                    'left': 45, 'right': 30},
                     'layout': {'width': '99%', 'height': '150px', 'grid_area': 'plot'}},
    'cal_rightview': {'padding_y': 0.25,
                      'fig_margin': {'top': 20, 'bottom': 35,
                                     'left': 30, 'right': 30},
                      'layout': {'width': '99%', 'height': '99%', 'grid_area': 'plot'}},
    'int_scatter': {'fig_margin': {'top': 40, 'bottom': 40,
                                   'left': 80, 'right': 150},
                    'layout': {'width': '620px', 'height': '470px', 'grid_area': 'plot'}},
    'pie': {'legend_location': 'top-right',
            'padding_y': 0.16,
            'fig_margin': {'top': 0, 'bottom': 0,
                           'left': 30, 'right': 30},
            'layout': {'width': '350px', 'height': '300px'},
            'animation_duration': 500},
}

# ipywidgets Layout settings
BQV_GRIDBOX = {'width': '99%',
               'grid_template_rows': 'auto',
               'grid_template_columns': 'auto',
               'grid_template_areas': '''"plot"''',
               'overflow': 'hidden',
               'overflow_y': 'hidden',
               'overflow_x': 'hidden'}

BQV_GRIDBOX_BBG_STYLE = {'width': '99%',
                         'grid_template_rows': 'auto auto auto',
                         'grid_template_columns': 'auto min-content',
                         'grid_template_areas': '''"title title" "legend toolbar" "plot plot"''',
                         'overflow': 'hidden',
                         'overflow_y': 'hidden',
                         'overflow_x': 'hidden'}

BQV_GRIDBOX_EXTERNAL_LEGEND = {'width': '99%',
                               'grid_template_rows': 'auto',
                               'grid_template_columns': 'auto min-content',
                               'grid_template_areas': '''"plot legend"''',
                               'overflow': 'hidden',
                               'overflow_y': 'hidden',
                               'overflow_x': 'hidden'}
