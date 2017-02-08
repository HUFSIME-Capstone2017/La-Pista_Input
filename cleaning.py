import pandas as pd
from datetime import datetime

def get_preprocessed(code) :
    preprocess_dict = {
        "London (LHR)" : "LHR",
        "Paris (CDG)" : "CDG",
        "Seoul (ICN)" : "ICN"
    }
    for key, value in preprocess_dict.items():
        code = code.replace(key, value)

    return code

d = pd.read_csv('/Users/ERRERO/dohop/20170207.csv')
d['R_DEST'] = d['R_DEST'].apply(get_preprocessed)
d['R_ORIGIN'] = d['R_ORIGIN'].apply(get_preprocessed)
d = d[((d.R_DEST == 'LHR') & (d.R_ORIGIN == 'CDG')) |
      ((d.R_DEST == 'LHR') & (d.R_ORIGIN == 'ICN')) |
      ((d.R_DEST == 'CDG') & (d.R_ORIGIN == 'LHR')) |
      ((d.R_DEST == 'CDG') & (d.R_ORIGIN == 'ICN')) |
      ((d.R_DEST == 'ICN') & (d.R_ORIGIN == 'LHR')) |
      ((d.R_DEST == 'ICN') & (d.R_ORIGIN == 'CDG'))
      ]
d['ARR_T'] = pd.to_datetime(d['ARR_T']).dt.time
d['DEP_T'] = pd.to_datetime(d['DEP_T']).dt.time
d.to_csv("20170207pre.csv", index=False)