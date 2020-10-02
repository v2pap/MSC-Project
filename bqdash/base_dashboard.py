from abc import ABCMeta, abstractmethod, ABC
import pandas as pd
import numpy as np
import bqdash.calc_functions
from ipywidgets import HTML, VBox, HBox, Button
from bqdash.Spinners import *

class MyAbstractMetaClass(ABCMeta,type(VBox)):pass

class BaseDashBoard(VBox,metaclass=MyAbstractMetaClass):
    """
    Base class
    """

    def __init__(self, df,column_mappings, colors, title=None):
        # Set initial state
        super().__init__()
        self.colors = colors
        self.data = df
        self.title = title
        self.column_mappings = column_mappings

        #Placeholder for widgets
        self._widgets = {}
        self.__build_title_box()
        self.__build_loading_indicator()

    def __build_title_box(self):
        '''
        Builds and sets the title widget for all dashboards
        '''
        if self.title:
            html_txt = """
            <h1  style=" font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    font-size: 24px; font-style: normal; font-variant: normal;
                    font-weight: 700; line-height: 26.4px;">{}</h1>
            """.format(self.title)
            title = HTML(html_txt)

            panel = HBox([title])
            panel.layout.overflow_x = "visible"
            panel.layout.overflow_y = "visible"
            panel.layout.display = "initial"
            panel.layout.width = "100%"
        else:
            panel = None

        #store title in widget dictionary
        self._widgets["title"] = panel

    def __build_loading_indicator(self):
        '''
        Creates and sets a loading spinner from Spinners module
        '''
        self._widgets['loading'] = CircleSpinner()

    def _toggle_children(self,children):
        '''Takes a list of widgets and sets them into the
           UI via the inherited VBox attribute
        '''
        self.children = children

    def verify_user_input(self):
        wrong_type_dict = {}

        if not isinstance(self.column_mappings, dict):
            wrong_type_dict['column_mappings'] = type(self.column_mappings)

        if not isinstance(self.data, pd.DataFrame):
            wrong_type_dict['df'] = type(self.data)

        if not isinstance(self.colors, dict):
            wrong_type_dict['colors'] = type(self.colors)

        if not isinstance(self.title, str):
            wrong_type_dict['title'] = type(self.title)

        if len(wrong_type_dict) != 0:
            error_msg = 'There is a problem with the input: ' + ' & '.join(['Incorrect type: ' + str(error) + ' for argument: ' + param for param,error in wrong_type_dict.items()])
            raise ValueError(error_msg)

    def check_required_fields(self,fields):
        missing_fields = []
        for field in  fields:
            if field not in self.column_mappings.keys():
                missing_fields.append(field)
        return missing_fields

    @abstractmethod
    def _build_all(self):
        '''AbstractMethod to be implemented by concrete classes'''
        raise NotImplementedError

    @abstractmethod
    def _read_col_mapping(self):
        '''AbstractMethod to be implemented by concrete classes'''
        raise NotImplementedError

    @property
    def widgets(self):
        return self._widgets
