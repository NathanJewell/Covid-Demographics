#load and organize data for visualization


import pandas as pd
import numpy as np
import fuzzywuzzy.process as fwp
from metadata import *
from convert_state import asState
import sys

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
    print("CLEANING")
    for d, m in zip(data, metadata): 
        remove_col_labels = [m["state_col"], m["county_col"]]
        if "filter_col" in m:
            remove_col_labels.append(m["filter_col"])
        use_cols = m["load_cols"] + remove_col_labels
        #if m["fn"] == "Unemployment.csv":
            #import pdb
            #pdb.set_trace()
        remove_cols = [col_name
                for col_name in list(d.columns) 
                if col_name.lower() not in use_cols]
        d.drop(columns=remove_cols, inplace=True)
        #first word + lowercase to county
        d.columns = [c.lower() for c in d.columns]

        remove_rows = []

        for label in remove_col_labels:
            for row, val in enumerate(d[label]):
                if pd.isnull(val):
                    remove_rows.append(row)
        d.drop(index=remove_rows, inplace=True) #drop all rows without value in metadata->"filter_col"
        print("\tDropped {} incomplete rows from {}".format(len(remove_rows),m["fn"]))

        d[m["county_col"]].apply(lambda x: x.lower())#x.split(' ')[0].lower())
        if (m["state_fmt"] == "abv"):
            d[m["state_col"]] = d[m["state_col"]].apply(lambda state_abv: asState(state_abv))

    return data

#UNUSED before I realized pd.merge exists
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
    #setup some variables
    county_label = "county"
    state_label = "state"
    unique_label = "unique"
    unique = lambda d : "{}.{}".format(d[county_label], d[state_label])

    first = True
    final = None
    for d, m in zip(data, metadata):
    #iterate over all the datasets we need to combine
        state_col = m["state_col"]
        county_col = m["county_col"]

        #swap standardized key column names into df
        # ? should this be moved to clean ?
        new_columns = list(d.columns)
        new_columns[new_columns.index(state_col)] = state_label
        new_columns[new_columns.index(county_col)] = county_label 
        d.columns = new_columns
        d.insert(0, unique_label, d[[state_label, county_label]].apply(unique, axis=1))
        
        #there was an error when I tried to compare pd.Series obj to None
        #thus the extra variable
        if first:
            final = d
            first = False
            continue

        #https://stackoverflow.com/questions/35380933/how-to-merge-two-pandas-dataframes-based-on-a-similarity-function
        state_choices = {}
        complete = 0
        dropped = 0
        def ldist(row):
            nonlocal complete
            nonlocal dropped
            progress_interval = int(len(d) / 100)
            minscore = 85
            complete += 1
            choices = None
            if row[state_label] in state_choices:
                choices = state_choices[row[state_label]]
            else:
                choices = set(final[final[state_label] == row[state_label]][unique_label])
                state_choices[row[state_label]] = choices
            
            choices = [""] if not choices else choices
            choice, score = fwp.extractOne(row[unique_label],choices)

            if ((len(d) - complete) % progress_interval) == 0:
                #print("{}%".format(int((complete/len(d)) * 100)))
                sys.stdout.write("\r\t\t{}%".format(int((complete/len(d)) * 100)))
                sys.stdout.flush()
            #print("Choice: {} Score: {}".format(choice, score))
            if score < minscore or len(choices) < 1:
                dropped += 1
                return None
                #print(score)

            state_choices[row[state_label]].remove(choice)
            return choice

        print("MERGING")
        print("\tcomputing levenshtein distances")
        d[unique_label] = d.apply(ldist, axis=1)
        print("\n\tdid not match {} entries".format(dropped))
        print("\tfinished computing distances")
        d = d[pd.notnull(d[unique_label])]
        d.drop(columns=[state_label, county_label], inplace=True)
        
        final = final.merge(d, on=unique_label, how='inner')
        print("{} counties are still matched".format(len(final)))

    
    return final
    
def entry():
    #setup metadata
    metadata = [
        gis_demo_data,
        group_covid_data,
        unemployment_data,
        education_data
    ]

    #load data
    raw_data = load_data(metadata)

    cleaned_data = clean_data(raw_data, metadata)

    pd_data = aggregate_counties_pandas(cleaned_data, metadata)

    print("Saving processed data to csv")
    pd_data.sort_values(by=['state','county'], inplace=True)
    pd_data.to_csv(data_fp("output.csv"))
    #data_np, labels = aggregate_counties(data, metadata)


if __name__ == "__main__":
    entry()