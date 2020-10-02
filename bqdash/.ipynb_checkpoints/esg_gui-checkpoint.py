from ipywidgets import HTML, Output, VBox, HBox, Button, Image,Tab
from gui.esg_flags import thirdpartyratings, internalratings,Quartiles
import functions.functions
import warnings
import pandas as pd



class EsgDashboardGui(VBox):
    """ Main gui """
    def __init__(self):
        super().__init__()
        self.widgets = {}
        self.__build_all()
        self.overflow_y = "visible"

    # *****************************************************************
    #
    #    Building the widget
    #
    # *****************************************************************
    def __build_all(self):

        #title and logo
        title_logo = self.__build_title_and_logo()

        # ticker input
        self.widgets['ticker_and_btn'] = self.__build_ticker_and_btn()

        # name and des
        name_and_des = self.__build_name_and_des()

        # rating, chart and co2
        third_party_rating = self.__build_third_party_rating()

        #row 2
        self.widgets['row_2'] = HBox([name_and_des, third_party_rating])
#         # flex table
        self.widgets['flex_tbl'] = HTML(layout={'margin':'30px 0 0 0'})
        self.widgets['peer_tbl'] = HTML(layout={'margin':'30px 0 0 0'})
        self.widgets['Tab'] = Tab()
#         self.widgets['flex_tbl'].bottom_panel_height = "700px"


        # busy indicator
        self.widgets['busy'] = HTML("""<h2 style="color:white;">Downloading data ...
        .</h><i class="fa fa-spinner fa-spin fa-2x fa-fw" style="color:white;"></i>""")

        self.children = [
            title_logo,
            self.widgets['ticker_and_btn']
        ]

    def __build_title_and_logo(self):
        # title
        html_txt = """
        <div style=\"background-color:#007683; height:60px; text-align:left; line-height: 1.5\">
            <font size=6 color=white ">
                <b>ESG Dashboard</b>
            </font>
        </div>
        """
        title = HTML(html_txt)
#         \style=\"margin-right: 5%;\
        # pack
        panel = HBox([title])
        self.widgets["title_and_logo"] = panel

        # layouts
        #title.layout.width = "100%"

        panel.layout.overflow_x = "visible"
        panel.layout.overflow_y = "visible"
        panel.layout.display = "initial"
        #title_panel.layout.width = "80%"
        panel.layout.width = "100%"
        #panel.layout.overflow_x = "hidden"


        return panel

    def __build_ticker_and_btn(self):
        self.widgets['ticker_input'] = AutoComplete(data = pd.read_excel("sample_data/esg_data.xlsx",sheetname='Data')["Name"].tolist())
        self.widgets['btn'] = Button(description = "get data")
        self.widgets['btn'].on_click(self.__run_btn_call_back)
        panel = HBox([self.widgets['ticker_input'],
                      self.widgets['btn']])
        return panel

    def __build_name_and_des(self):
        self.widgets['name'] = HTML()
        self.widgets['des'] = HTML()
        self.widgets['industry'] = HTML()
        self.widgets['internal_score'] = internalratings()
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

        self.widgets['thirdparty'] = thirdpartyratings()


        third_party_rating = VBox([
                             self.widgets['thirdparty'],

                                 ])
        # layout
        #rating_panel.layout.justify_content = "space-between"

        self.widgets['thirdparty'].layout.max_height = "300px"
        self.widgets['thirdparty'].layout.width = "100%"
        self.widgets['thirdparty'].layout.margin = '0 0 0 20px'


        third_party_rating.layout.width = "50%"
        third_party_rating.layout.overflow_x = "hidden"


        return third_party_rating

    def color_percentiles_hi(self,column,background=True):

        if not background:
            return ['' if val =='-' else 'color: red' if val > 3 else  'color: #ff6600'
                if val == 3 else 'color: #93C02D'
                if val == 1 else 'color: DarkOrange' for val in column]
        else:
            return ['' if val =='-' else 'background-color: red' if val > 3 else  'background-color: #ff6600'
                if val == 3 else 'background-color: #93C02D'
                if val == 1 else 'background-color: DarkOrange' for val in column]

    def format_frame(self,dataframe,subset,font_size,background_color):
        formatted_frame = (dataframe.replace(0,'-').style
                        #.format(dataframe_formats)
                        .set_table_attributes('class="table"')
                        .set_table_styles([{'selector': '.row_heading','props': [('display', 'none')]},{'selector': '.blank.level0','props': [('display', 'none')]},
                                          dict(selector='th',props=[('text-align','center'),('overflow-wrap','break-word'),('background-color', '#B4B3B2'),('color', '#1a1a1a')])])
                        .set_properties(**{'text-align':'center','overflow-wrap':'break-word','color':'white','font-size':font_size})#'white-space': 'nowrap'
                        .apply(self.color_percentiles_hi,subset=subset,background=background_color))
        return formatted_frame.render()

    # *****************************************************************
    #
    #    Update the widgets data
    #
    # *****************************************************************

    def __update(self, data):

        self.__update_name_and_des(data)
        self.__update_third_party_rating(data)
        self.widgets['flex_tbl'].value =  '' if data['tbl_data'].empty else self.format_frame(data['tbl_data'],['Quartile'],'15px',background_color=True)
        self.widgets['peer_tbl'].value =  '' if data['peer_data'].empty else self.format_frame(data['peer_data'],list(set(data['peer_data'].columns)- set(['Name'])),'12px',background_color=False)
        self.widgets['Tab'].children = [self.widgets['flex_tbl'],self.widgets['peer_tbl']]
        self.widgets['Tab'].set_title(0,'Security')
        self.widgets['Tab'].set_title(1,'Peers')

    def __update_name_and_des(self, data):

        self.widgets['name'].value = "<h1>" +  str(data['name']) + "</h1>"
        self.widgets['des'].value = "<font color=#CFB010>" + str(data['des']) + "</font>"
        self.widgets['industry'].value = '<p style="color: #ffffff;font-size:20px">Industry: ' + str(data['industry']) + "</p>"
        self.widgets['internal_score'].update(data['score_flag'])

    def traffic_colors(self,data):
        if data >= 3:
            return 'red'
        elif data ==1:
            return '#93C02D'
        else:
            return 'DarkOrange'

    def __update_third_party_rating(self, data):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")


            # thirdparty ratings
            self.widgets['thirdparty'].update(data["third_party_rating"],data['rating_date'],data['score_flag'])


    # *****************************************************************
    #
    #    button call back
    #
    # *****************************************************************

    def __run_btn_call_back(self, caller = None):
        #with self.widgets['err_display']:
        self.__toggle_busy()
            #try:
        ticker = self.widgets['ticker_input'].value
        new_data = functions.functions.get_data(ticker)
        self.__update(new_data)
        self.__toggle_ready()
            #except:
        #self.__toggle_ready()
            #raise

    # *****************************************************************
    #
    #    toggle busy
    #
    # *****************************************************************

    def __toggle_busy(self):
        # busy indicator
        self.children = [
            self.widgets["title_and_logo"],
            self.widgets['ticker_and_btn'],
            self.widgets['busy']
        ]


    def __toggle_ready(self):
        self.children = [
            self.widgets["title_and_logo"],
            self.widgets['ticker_and_btn'],
            self.widgets['row_2'],
            self.widgets['Tab']
        ]
