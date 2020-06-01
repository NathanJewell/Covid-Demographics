import pandas as pd
from metadata import covid_data as meta
import numpy as np



data_path = "../data/"
data_fp = lambda fn : "{}{}".format(data_path, fn)

data=None
with open(data_fp("covid-counties-full.csv"), "r") as csvfile:
    data = pd.read_csv(csvfile)

data = data[data['county'] != "Unknown"]
state_county_fn = lambda d : "{}.{}".format(d[meta['state_col']], d[meta['county_col']])
data.insert(0, "covid_grouping", data.apply(state_county_fn, axis=1))
group_data = data.groupby('covid_grouping').agg(list)
group_data[meta['state_col']] = group_data[meta['state_col']].apply(lambda sarr : sarr[0])
group_data[meta['county_col']] = group_data[meta['county_col']].apply(lambda carr : carr[0])

import pdb
pdb.set_trace()

all_dates = data['date'].unique()
date_ids = np.array(range(len(all_dates)))
dates_df = pd.DataFrame(np.array([date_ids, all_dates]).T, columns=['date_id', 'date'] )
start_dates = group_data['date'].apply(lambda darr : np.where(all_dates == darr[0])[0][0])
group_data.insert(0, 'start_date', start_dates)
group_data.to_csv(data_fp("group-covid-counties.csv"))