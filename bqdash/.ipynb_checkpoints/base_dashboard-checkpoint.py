from abc import ABCMeta, abstractmethod, ABC
import pandas as pd
import numpy as np
import bqplot as bqp
from bqviz import BarPlot, HistPlot, LinePlot
from ipywidgets import HTML, Output, VBox, HBox, Button, Image,Tab, Dropdown, Layout, ToggleButtons
import bqdash.calc_functions
from bqdash.Spinners import *
from bqdash.custom_widgets import HeatMap, Scatter, ThirdPartyRatings, InternalRatings, Quartiles, DataGrid
from collections import OrderedDict


class BaseDashBoard(VBox):
    """Base class."""

    def __init__(self, df, colors=None, title=None, column_mappings=None):
        # Set initial state
        super().__init__()
        self._colors = colors
        self._data = df
        self._title = title
        self.column_mappings = column_mappings
        self.widgets = {}
        self.__build_title_box()
        self.__build_loading_indicator()

    def __build_all(self):
        '''To be implemented by concrete classes'''
        raise NotImplementedError

    def __read_col_mapping(self,col_mappings):
        '''To be implemented by concrete classes'''
        raise NotImplementedError

    def __build_title_box(self):
        # title
        if self._title:
            html_txt = """
            <h1  style=" font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    font-size: 24px; font-style: normal; font-variant: normal;
                    font-weight: 700; line-height: 26.4px;">{}</h1>
            """.format(self._title)
            title = HTML(html_txt)

            panel = HBox([title])
            panel.layout.overflow_x = "visible"
            panel.layout.overflow_y = "visible"
            panel.layout.display = "initial"
            panel.layout.width = "100%"
        else:
            panel = None

        self.widgets["title"] = panel

    def __build_loading_indicator(self):
        self.widgets['loading'] = CircleSpinner()
