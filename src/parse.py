#load and organize data for visualization


import pandas as pd
import numpy as np
import fuzzywuzzy as fwp
from metadata import *

data_path = "../data/"
data_fp = lambda fn : "{}{}".format(data_path, fn)

def load_data(metadata):
    loaded = []
            
    for meta in metadata:
        data = pd.read_csv(data_fp(meta["fn"]))
        loaded.append(data)

    return loaded

def clean_data(data, metadata):
    #removes columns not contained in "load_cols"
    #applies tolower for headers
    for d, m in zip(data, metadata): 
        use_cols = m["load_cols"] + [m["state_col"], m["county_col"]]
        state_rows = []
        for row, county in enumerate(d[m["county_col"]]):
            if not county:
                state_rows.append(row)
        d.drop(rows=state_rows, inplace=True) #drop all rows without county
        remove_cols = [col_name
                for col_name in list(d.columns) 
                if col_name.lower() not in use_cols]
        d.drop(columns=remove_cols, inplace=True)
        #first word + lowercase to county
        d.columns = [c.lower() for c in d.columns]
        d[m["county_col"]].apply(lambda x: x.split(' ')[0].lower())

    return data


def aggregate_counties(data, metadata):
    cols = []
    num_unique = 0
    num_filled = 0
    county_unique = {}

    col_labels = []
    data_py = []

    for d, m in zip(data, metadata):
        county_col = m["county_col"]
        state_col = m["state_col"]

        #find indices for all counties in this dataset
        county_indices = []
        for state, county in zip(d[state_col], d[county_col]):
            unique = "{}.{}".format(
                state,
                county 
            )
            if unique not in county_unique:
                county_unique[unique] = num_unique
                num_unique += 1
            county_indices.append(county_unique[unique])
        
        #increase number of rows for any new counties
        for x in range(num_unique - len(data_py)):
            data_py.append([])

        all_idx = set(range(len(data_py)))

        data_unique = d.drop(columns=[county_col, state_col]) 
        col_labels += list(data_unique.columns)
        for cidx, county_data in zip(county_indices, data_unique):
            if cidx < len(data_py):
                data_py[cidx] += county_data
                all_idx.remove(cidx)
            else:
                print("ERROR aggregating data, result array missized")

        filler = [None] * len(d)
        num_filled += len(all_idx)
        for remaining in all_idx:
            data_py[remaining] += filler
        
        print("agreggated dataset with {} counties".format(len(county_indices)))
        print("missed {} existing entries".format(num_filled))

    return np.asarray(data_py, dtype=float), col_labels

def aggregate_counties_pandas(data, metadata):
    county_label = "county"
    state_label = "state"

    first = True
    final = None
    for d, m in zip(data, metadata):
        state_col = m["state_col"]
        county_col = m["county_col"]
        new_columns = list(d.columns)
        new_columns[new_columns.index(state_col)] = state_label
        new_columns[new_columns.index(county_col)] = county_label 
        d.columns = new_columns
        if first:
            final = d
            first = False
        else:
            final = final.merge(d, 'inner', [county_label, state_label])
    
    return final


    
def entry():
    #setup metadata
    metadata = [
        gis_demo_data,
        covid_data
    ]

    #load data
    data = load_data(metadata)

    data = clean_data(data, metadata)

    data = aggregate_counties_pandas(data, metadata)
    #data_np, labels = aggregate_counties(data, metadata)


if __name__ == "__main__":
    entry()