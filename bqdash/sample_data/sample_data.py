import pandas as pd
import numpy as np
import os

esg_path = os.path.join(os.path.dirname(__file__), 'esg_data.xlsx')
esg_sample_data = pd.read_excel(esg_path)

port_path = os.path.join(os.path.dirname(__file__), 'port_sample_data.xlsx')
port_sample_data = pd.read_excel(port_path)

score_path = os.path.join(os.path.dirname(__file__), 'scoring_sample.xlsx')
scoring_sample_data = pd.read_excel(score_path)
