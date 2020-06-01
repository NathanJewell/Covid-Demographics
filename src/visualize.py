import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from functools import partial
from ast import literal_eval

data_path = "../data/"
data_fp = lambda fn : "{}{}".format(data_path, fn)

continuum_code_map = {
    1 : "Metro",
    2 : "Metro",
    3 : "Metro",
    4 : "Transition",
    5 : "Transition",
    6 : "Transition",
    7 : "Transition",
    8 : "Rural",
    9 : "Rural"
}

continuumAsClass = lambda c : continuum_code_map[c]

def make_statistics(data):
    cases_percap = data['cases']/data['population']
    deaths_percap = data['deaths']/data['population']
    deaths_sqmi = data['deaths']/data['sqmi']
    cases_sqmi = data['cases']/data['sqmi']

    psqmi = data['pop_sqmi']
    rural = psqmi.between(psqmi.quantile(0), psqmi.quantile(.33))
    transition = psqmi.between(psqmi.quantile(.33), psqmi.quantile(.66))
    urban = psqmi.between(psqmi.quantile(.66), psqmi.quantile(1))
    classification =  psqmi.copy()
    classification[rural] = "rural"
    classification[transition] = "transition"
    classification[urban] = "urban"

    continuum_classes = set(list(data['rural_urban_continuum_code_2013']))
    for cc in continuum_classes:
        if cc not in continuum_code_map:
            continuum_code_map[cc] = "Other"
    continuum_class = data['rural_urban_continuum_code_2013'].apply(continuumAsClass)

    race_cols = ["white", "black", "ameri_es", "asian", "hawn_pi", "hispanic", "other"]
    race_plurality = data[race_cols].idxmax(axis=1)

    fromusd = lambda usdstr : float(''.join(usdstr.split(',')))
    income_percap = data['median_household_income_2018'].apply(fromusd)

    income_over_deaths = income_percap / deaths_percap * 10000

    data.insert(len(data.columns)-1, "cases_percap", cases_percap)
    data.insert(len(data.columns)-1, "deaths_percap", deaths_percap)
    data.insert(len(data.columns)-1, "cases_sqmi", cases_sqmi)
    data.insert(len(data.columns)-1, "deaths_sqmi", deaths_sqmi)
    data.insert(len(data.columns)-1, "continuum_class", continuum_class)
    data.insert(len(data.columns)-1, "race_plurality", race_plurality)
    data.insert(len(data.columns)-1, "classification", classification)
    data.insert(len(data.columns)-1, "med_income_percap", income_percap)
    data.insert(len(data.columns)-1, "income_over_deaths", income_over_deaths)

    return data

def between(df, col, qlo, qhi):
    return df[df[col].between(df[col].quantile[qlo], df[col].quantile[qhi])]

linear = lambda x : x
def plot_cols(df, xcols, ycols, xlabel, ylabel, scale=[linear, linear], save=True):
    plt.clf()
    assert(len(xcols) == len(ycols), "mistmached label sizes")
    series_formats = [".r",".b",".g",".c","om","oy"]

    qhi = .95
    qlo = .05


    for xcol, ycol, fmt in zip(xcols, ycols, series_formats):
        x = df[xcol]
        y = df[ycol]
        keep = x.between(x.quantile(qlo), x.quantile(qhi))
        x = x[keep]
        y = y[keep]
        keep = y.between(y.quantile(qlo), y.quantile(qhi))
        x = scale[0](x[keep])
        y = scale[1](y[keep])
        plt.plot(x, y, fmt, label="{} vs {}".format(xcol, ycol), alpha=.25)
    plt.plot
    plt.xlabel("{}".format(xlabel))
    plt.ylabel("{}".format(ylabel))
    plt.title('{} vs {}'.format(' '.join(xcols), ' '.join(ycols)))
    plt.legend()
    if save:
        plt.savefig("{}.png".format('-'.join(xcols+ycols)))

def plot_classwise(df, class_col, xcol, ycol, xlabel, ylabel, scale=[linear, linear], save=True, filename=None):
    classes = set(df[class_col])
    this_date = df['date'].value_counts().idxmax()

    qlo = .05
    qhi = .95
    series_formats = [".r",".b",".g",".c",".m",".y"]
    for c, fmt in zip(classes, series_formats):
        where = df[df[class_col] == c]
        x = where[xcol]
        y = where[ycol]
        keep = x.between(x.quantile(qlo), x.quantile(qhi))
        x = x[keep]
        y = y[keep]
        keep = y.between(y.quantile(qlo), y.quantile(qhi))
        x = scale[0](x[keep])
        y = scale[1](y[keep])
        plt.plot(x, y, fmt, label="{}".format(c), alpha=.3)

    plt.plot
    plt.xlabel("{}".format(xlabel))
    plt.ylabel("{}".format(ylabel))
    plt.title('[{}] {} vs {} by {}'.format(this_date, xcol, ycol, class_col))
    plt.legend()
    if save:
        if not filename:
            filename = "output/{}-vs-{}-by-{}.png".format(xcol, ycol, class_col)
        plt.savefig(filename)
        plt.clf()

def entry():
    data = None
    with open(data_fp("output_grouped.csv"), "r") as datafile:
        data = pd.read_csv(datafile)

    data = data.drop(columns='fips')
    literal_eval_cols = ['deaths', 'cases', 'date']
    for col in literal_eval_cols:
        data[col] = data[col].apply(literal_eval)

    num_dates = max(data['start_date'])
    cases_datewise = []
    deaths_datewise = []
    dates_datewise = []
    print("ALIGNING covid data")
    for date_id in range(num_dates-1):
        def data_atdate(series_col, row):
            #import pdb
            #pdb.set_trace()
            offset = date_id - row['start_date']
            if offset >= 0:
                return row[series_col][offset]
            return None
        
        #import pdb
        #pdb.set_trace()
        deaths = data.apply(partial(data_atdate, 'deaths'), axis=1)
        cases = data.apply(partial(data_atdate, 'cases'), axis=1)
        dates = data.apply(partial(data_atdate, 'date'), axis=1)
        deaths_datewise.append(deaths)
        cases_datewise.append(cases)
        dates_datewise.append(dates)
        sys.stdout.write("\r{}%".format(int(date_id/num_dates * 100)))
        sys.stdout.flush()

    cases_datewise = np.asarray(cases_datewise)
    deaths_datewise = np.asarray(deaths_datewise)

    #aug_data = make_statistics(data)

    #fig = aug_data.plot(x='pop_sqmi', y="cases_percap")
    #plot_cols(aug_data, ['pop_sqmi', "pop_sqmi"], ['deaths_sqmi', 'cases_sqmi'], 'people/sqmi', 'prevalence percapita', [np.log, linear])
    #plot_classwise(aug_data, 'classification', 'pop_sqmi', 'deaths_sqmi', 'people/sqmi', 'deaths/sqmi', [linear, linear])
    #xcols = ["med_income_percap"]
    #plot_cols(aug_data, xcols, ['deaths_percap'], 'med. hh income ($)', "prevalence percapita", [linear, linear])
    #plot_classwise(aug_data, 'classification', 'med_income_percap', 'income_over_deaths', 'income_percap', 'income/deaths', [linear, linear])
    #plot_classwise(aug_data, 'continuum_class', 'pop_sqmi', 'deaths_sqmi', 'people/sqmi', 'deaths/sqmi', [linear, linear])
    #plot_cols(aug_data, ['med_age'], ['cases_percap'], 'med_age', "deaths percapita", [linear, linear])

    max_deaths_sqmi = 0.0
    max_cases_sqmi = 0.0
    max_med_income = 0.0 
    def covid_ondate(df, dateid):
        nonlocal max_deaths_sqmi
        nonlocal max_cases_sqmi
        nonlocal max_med_income
        date_deaths = deaths_datewise[dateid-1]
        date_cases = cases_datewise[dateid-1]
        date_dates = dates_datewise[dateid-1]
        ondate = df
        ondate['deaths'] = date_deaths
        ondate['cases'] = date_cases
        ondate['date'] = date_dates
        ondate = ondate[(pd.notnull(date_deaths)) & (pd.notnull(date_cases))]
        ondate = make_statistics(ondate)
        max_deaths_sqmi = np.max([max_deaths_sqmi, ondate['deaths_sqmi'].quantile(.95)])
        max_cases_sqmi = np.max([max_cases_sqmi, ondate['cases_sqmi'].quantile(.95)])
        max_med_income = np.max([max_med_income, ondate['med_income_percap'].quantile(.95)])

        return ondate

    deathbounds = (np.min(deaths_datewise), np.max(deaths_datewise))
    casebounds = (np.min(cases_datewise), np.max(cases_datewise))
    max_pop_sqmi = data['pop_sqmi'].quantile(.95)
    def graph_frame(dateid, date_data):
        xcol = 'pop_sqmi'
        deathcol = 'deaths_sqmi'
        casecol = 'cases_sqmi'
        incomecol = 'med_income_percap'
        xbounds = (0, np.log(max_pop_sqmi)) #constant for all graphs
        incomebounds = (0, max_med_income)
        deathbounds = (0, max_deaths_sqmi) #using max computed from aggregated deaths
        casebounds = (0, max_cases_sqmi) #using max computed from aggregated deaths
        
        #plt.xlim(xbounds)
        #plt.ylim(deathbounds)
        ##date_data = covid_ondate(dateid)
        #plot_classwise(date_data, 'continuum_class', xcol, deathcol, 'people/sqmi', 'deaths/sqmi', [np.log, linear], filename="output/deaths-{:03d}.png".format(dateid))
        #plt.ylim(casebounds)
        #plot_classwise(date_data, 'continuum_class', xcol, casecol, 'people/sqmi', 'cases/sqmi', [np.log, linear], filename="output/cases-{:03d}.png".format(dateid))
        plt.xlim(incomebounds)
        plt.ylim(casebounds)
        plot_classwise(date_data, 'race_plurality', incomecol, casecol, 'med income', 'cases/sqmi', [linear, linear], filename="output/race-income-{:03d}.png".format(dateid))



    data_ondates = []
    print("Generating datewise data")
    for date in range(num_dates):
        data_ondates.append(covid_ondate(data, date))
        sys.stdout.write("\r{}%".format(int(date/num_dates * 100)))
        sys.stdout.flush()

    print("Generating datewise animation frames")
    for dateid, date_data in enumerate(data_ondates):
        graph_frame(dateid, date_data)
        sys.stdout.write("\r{}%".format(int(date_id/num_dates * 100)))
        sys.stdout.flush()





if __name__ == "__main__":
    entry()