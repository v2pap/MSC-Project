def get_totals(all_data,group1,group2):

    benchmark = all_data.copy(deep=True).drop(['% Wgt (Port)'],axis=1)
    portfolio = all_data.copy(deep=True).drop(['% Wgt (Index)'],axis=1).dropna()

    portfolio_totals = portfolio.groupby(by=[group1,group2]).sum()
    benchmark_totals = benchmark.groupby(by=[group1,group2]).sum()

    groupings = {group1 : list(all_data[group1].dropna().unique()),
                 group2 : list(all_data[group2].dropna().unique())}

#     print(groupings)
#     for key,str_list in groupings.items():
#         str_list = list(filter(None,str_list))

    for x in groupings[group1]:
            for y in groupings[group2]:
                if not (x,y) in portfolio_totals.index:
                    portfolio_totals.loc[(x,y),:] = 0

    for x in groupings[group1]:
        for y in groupings[group2]:
            if not (x,y) in benchmark_totals.index:
                benchmark_totals.loc[(x,y),:] = 0

    return {'port_totals':portfolio_totals,
            'bench_totals':benchmark_totals}

def get_table_data(all_data,group1,group2):
    portfolio = all_data.copy(deep=True)
    portfolio = portfolio[pd.notnull(portfolio['% Wgt (Port)'])]
    portfolio[['% Wgt (Port)', '% Wgt (Index)']] = portfolio[['% Wgt (Port)', '% Wgt (Index)']].fillna(value=0)
    portfolio['+/-'] = portfolio['% Wgt (Port)'] - portfolio['% Wgt (Index)']
    portfolio = portfolio.reset_index()
    portfolio = portfolio.rename(columns={'% Wgt (Port)':'Fund (%)','% Wgt (Index)':'Index (%)','ID':'Ticker'})
    portfolio= portfolio[['Ticker','Name',group1,group2,'Fund (%)','Index (%)','+/-']]
    region_list = {key:val for key,val in portfolio.groupby(by=[group1,group2])}
    return region_list

def get_grid_map_data(all_data,group1,group2):
    totals = get_totals(all_data,group1,group2)
    final_totals = totals['port_totals'].join(totals['bench_totals']).fillna(0)
    final_totals['+/-'] = final_totals['% Wgt (Port)'] - final_totals['% Wgt (Index)']
    final_totals = final_totals.reset_index()
    final_pivot = final_totals.pivot(index=group1,columns=group2,values='% Wgt (Port)')
    return final_pivot

def overall_totals(all_data,group1,group2):
    benchmark = all_data.copy(deep=True).drop(['% Wgt (Port)'],axis=1)
    portfolio = all_data.copy(deep=True).drop(['% Wgt (Index)'],axis=1).dropna()

    portfolio_g1_totals = portfolio.groupby(by=[group1]).sum()[['% Wgt (Port)']]
    portfolio_g2_totals = portfolio.groupby(by=[group2]).sum()[['% Wgt (Port)']]

    benchmark_g1_totals = benchmark.groupby(by=[group1]).sum()[['% Wgt (Index)']]
    benchmark_g2_totals = benchmark.groupby(by=[group2]).sum()[['% Wgt (Index)']]

    portfolio_g1_count = portfolio.groupby(by=[group1]).count()[['Name']]
    portfolio_g2_count = portfolio.groupby(by=[group2]).count()[['Name']]
    #.drop([0],axis=0)
    g1_total = pd.concat([portfolio_g1_totals,benchmark_g1_totals,portfolio_g1_count],axis=1)
    g2_total = pd.concat([portfolio_g2_totals,benchmark_g2_totals,portfolio_g2_count],axis=1)
    g1_total['+/-'] = g1_total['% Wgt (Port)'] - g1_total['% Wgt (Index)']
    g2_total['+/-'] = g2_total['% Wgt (Port)'] - g2_total['% Wgt (Index)']

    g1_total = g1_total.rename(columns={'% Wgt (Port)':'Fund (%)','% Wgt (Index)':'Index (%)','Name':'# Stocks'}).sort_values('+/-')
    g2_total = g2_total.rename(columns={'% Wgt (Port)':'Fund (%)','% Wgt (Index)':'Index (%)','Name':'# Stocks'}).sort_values('+/-')


    return {'g1_totals':g1_total,
            'g2_totals':g2_total}

def format_portfolio_frame(dataframe):
    formatted_frame = (dataframe.round(2).replace(0,'-').style
                    #.format(dataframe_formats)
                    .set_table_attributes('class="table"')
                    .set_table_styles([{'selector': '.row_heading','props': [('display', 'none')]},{'selector': '.blank.level0','props': [('display', 'none')]},
                                      dict(selector='th',props=[('text-align','center'),('white-space', 'nowrap'),('background-color', '#f2f2f2'),('width','200px'),('font-size', '12px'),('color', '#1a1a1a')])])
                    .set_properties(**{'text-align':'center','white-space': 'nowrap','color':'white','font-size':'12px'}))

    return formatted_frame.render()

def format_summary_frame(dataframe):
    formatted_frame = (dataframe.round(2).replace(0,'-').style
                    .set_table_attributes('class="table"')
                    .set_table_styles([{'selector': '.row_heading','props': [('display', 'none')]},{'selector': '.blank.level0','props': [('display', 'none')]},
                                      dict(selector='th',props=[('text-align','center'),('white-space', 'nowrap'),('background-color', '#f2f2f2'),('width','200px'),('font-size', '10px'),('color', '#1a1a1a')])])
                    .set_properties(**{'text-align':'center','white-space': 'nowrap','color':'white','font-size':'10px'})
                    .apply(highlight_positives,subset=['+/-']))

    return formatted_frame.render()

def highlight_positives(column):
        return ['' if val =='-' else 'background-color: #ff8080' if val < 0 else 'background-color: #80ff80' if val > 0 else 'background-color: #ffb366' for val in column]

def update_table(self,target):
    lbl.layout.display = ''
    #print(target['new'])
    try:
        first = list(grid_data.columns)[target['data']['column']]
        second = list(grid_data.index)[target['data']['row']]
        portfolio_table.value = format_portfolio_frame(group_data[first,second])
    except:
        portfolio_table.value = '<p style="color: #F7DC6F;font-size:20px">Portfolio Contains No Stocks in this Allocation</p>'

def update_table_two(target):
    if target['old'] == None or target['old'] == {} or target['old'] == {'hovered_point': None} or target['old'] == 0 or target['old'] == 'traitlets.Undefined':
        pass
    else:
        try:
            first = list(grid_data.columns)[target['owner'].x[0]]
            second = list(grid_data.index)[target['owner'].y[0]]
            portfolio_table.value = format_portfolio_frame(group_data[first,second])
        except:
            portfolio_table.value = '<p style="color: #F7DC6F;font-size:20px">Portfolio Contains No Stocks in this Allocation</p>'

def update_summary_tables(data):
    g1_summary.value = format_summary_frame(data['g1_totals'].fillna(0).reset_index())
    g2_summary.value = format_summary_frame(data['g2_totals'].fillna(0).reset_index())

def update_chart(df):

    grid_map = GridHeatMap(color=df,scales={'column': x_sc, 'row': y_sc, 'color': col_sc},interactions={'click':'select'},
                           anchor_style={'fill':'##F5EEF8'})

    x_lb.domain = list(df.columns)
    y_lb.domain = list(df.index)
    x_sc.domain = [x for x in range(len(list(df.columns)))]
    y_sc.domain = [x for x in range(len([x for x in df.index]))]

    marks = [grid_map]

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            marks.append(
                Label(x=[col],
                      y=[row],
                      scales={'x': x_sc, 'y': y_sc},
                      text=[str(round(df.iloc[row, col], 2)) + '%'],
                      align='middle',
                      default_size=8,
                      font_weight='bolder',
                      colors=['black']))
    fig.marks=marks
    ax_x.label = grouping_one.value
    ax_y.label = grouping_two.value

    fig.layout.display = ''

#     for mark in fig.marks:
#         mark.observe(update_table_two)

    grid_map.on_element_click(update_table)

def run_app(btn):
    global grid_data
    global group_data
    fig.layout.display = 'None'
    tab.layout.display ='None'
    loading_html.layout.display = ''
    matrix = get_data('x',benchmark_picker.value,grouping_one.value,grouping_two.value)

    if grouping_one.value == 'Region' or grouping_two.value == 'Region':
        matrix['Region'] = matrix['Region'].map(region_mapping)

    group_data = get_table_data(matrix,grouping_one.value,grouping_two.value)
    summary_data = overall_totals(matrix,grouping_one.value,grouping_two.value)
    grid_data = get_grid_map_data(matrix,grouping_two.value,grouping_one.value)
    update_summary_tables(summary_data)
    update_chart(grid_data)
    tab.layout.display =''
    loading_html.layout.display = 'None'

# Define Interactive Dropdowns
universe_picker = Dropdown(options=['Portfolio 1'],layout={'overflow_x':'visible','overflow_y':'visible','max_width':'200px'})
benchmark_picker = Dropdown(value='MSCI World',options=benchmarks.keys(),layout={'overflow_x':'visible','overflow_y':'visible','max_width':'200px'})
grouping_one = Dropdown(value='Sector',options=group_mapping.keys(),layout={'overflow_x':'visible','overflow_y':'visible','max_width':'200px'})
grouping_two = Dropdown(value='Region',options=group_mapping.keys(),layout={'overflow_x':'visible','overflow_y':'visible','max_width':'200px'})
run_button = Button(description='GO',button_style='success',layout={'margin':'34px 0 0 2px'})
run_button.on_click(run_app)

# Define the various Table Objects
portfolio_table = HTML()
g1_summary = HTML(layout={'overflow_x':'visible','overflow_y':'auto','min_width':'450px','max_height':'500px','margin':'0 15px 0 0'})
g2_summary = HTML(layout={'overflow_x':'visible','overflow_y':'auto','min_width':'450px','max_height':'500px','margin':'0 0 0 0'})
lbl = HTML('<p style="color: #F2F3F4;font-size:30px">Portfolio Holdings</p>',layout={'overflow_x':'visible','overflow_y':'visible','display':'none'})

loading_html = HTML("""
    <div style="font-size:14px; color:lightskyblue;">
        <i class="fa fa-circle-o-notch fa-spin"></i><span>&nbsp;Loading...</span>
    </div>""",layout={'margin':'34px 0 0 2px','display':'none'})

load_box = HBox([loading_html])

# Define the bqplot Objects
x_sc = OrdinalScale()
y_sc = OrdinalScale()
col_sc = ColorScale(scheme='YlGn')
x_lb = OrdinalScale()
y_lb = OrdinalScale(reverse=True)
ax_x = Axis(scale=x_lb,tick_style={'font-size': 10,'text-anchor': 'end'},tick_rotate=-45)
ax_y = Axis(scale=y_lb, orientation='vertical',tick_style={'font-size': 10,'text-anchor': 'end'})
fig = Figure(marks=[], axes=[ax_x, ax_y], padding_y=0.0,
     layout={'min_width':'1000px','min_height':'600px'},fig_margin={'top':50,'right':0,'bottom':150,'left':150},
     title = 'Portfolio Weight HeatMap (%)')

# create the tab view
form_summary = HBox([g1_summary,g2_summary],
                  layout={'overflow_x':'visible','overflow_y':'visible','max_height':'500px','margin':'0 0 2px 5px'})

form_heatmap = VBox([fig,lbl,VBox([portfolio_table],layout={'min_height':'300px'})])

tab = Tab(layout={'margin':'0 0 5px 0'})
tab.layout.display ='None'
tab.children = [form_heatmap,form_summary]
tab.set_title(0, 'Heatmap')
tab.set_title(1, 'Summary')


controls = VBox([HBox([VBox([HTML(value='Choose Portfolio'),universe_picker]),VBox([HTML(value='Choose Benchmark'),benchmark_picker]),run_button,load_box],
                layout={'margin':'0 0 20px 0'}),
                HBox([VBox([HTML(value='Choose Grouping (x)'),grouping_one]),VBox([HTML(value='Choose Grouping (y)'),grouping_two])],
                layout={'margin':'0 0 20px 0'})
                ])

form = VBox([

            controls,
            tab
            ])

display(form)
