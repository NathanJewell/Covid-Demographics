import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_path = "../data/"
data_fp = lambda fn : "{}{}".format(data_path, fn)

def make_statistics(data):
    cases_percap = data['cases']/data['population']
    deaths_percap = data['deaths']/data['population']

    psqmi = data['pop_sqmi']
    rural = psqmi.between(psqmi.quantile(0), psqmi.quantile(.33))
    transition = psqmi.between(psqmi.quantile(.33), psqmi.quantile(.66))
    urban = psqmi.between(psqmi.quantile(.66), psqmi.quantile(1))
    classification = pd.Series([None] * len(psqmi)) 
    classification[rural] = "rural"
    classification[transition] = "transition"
    classification[urban] = "urban"

    fromusd = lambda usdstr : float(''.join(usdstr.split(',')))
    income_percap = data['median_household_income_2018'].apply(fromusd)

    income_over_deaths = income_percap / deaths_percap * 10000

    data.insert(len(data.columns)-1, "cases_percap", cases_percap)
    data.insert(len(data.columns)-1, "deaths_percap", deaths_percap)
    data.insert(len(data.columns)-1, "classification", classification)
    data.insert(len(data.columns)-1, "med_income_percap", income_percap)
    data.insert(len(data.columns)-1, "income_over_deaths", income_over_deaths)

    return data

def between(df, col, qlo, qhi):
    return df[df[col].between(df[col].quantile[qlo], df[col].quantile[qhi])]

linear = lambda x : x
def plot_cols(df, xcols, ycols, xlabel, ylabel, scale=[linear, linear]):
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
    plt.savefig("{}.png".format('-'.join(xcols+ycols)))
    plt.clf()

def plot_classwise(df, class_col, xcol, ycol, xlabel, ylabel, scale=[linear, linear]):
    classes = set(df[class_col])

    qlo = .05
    qhi = .95
    series_formats = [".r",".b",".g",".c","om","oy"]
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
    plt.title('{} vs {} by {}'.format(xcol, ycol, class_col))
    plt.legend()
    plt.savefig("{}-vs-{}-by-{}.png".format(xcol, ycol, class_col))
    plt.clf()

def entry():
    data = None
    with open(data_fp("best_output.csv"), "r") as datafile:
        data = pd.read_csv(datafile)

    aug_data = make_statistics(data)

    #fig = aug_data.plot(x='pop_sqmi', y="cases_percap")
    #plot_cols(aug_data, ['pop_sqmi', "pop_sqmi"], ['deaths_percap', 'cases_percap'], 'people/sqmi', 'prevalence percapita', [np.log, linear])
    #plot_classwise(aug_data, 'classification', 'pop_sqmi', 'deaths_percap', 'people/sqmi', 'deaths percap', [linear, linear])
    #xcols = ["med_income_percap"]
    #plot_cols(aug_data, xcols, ['deaths_percap'], 'med. hh income ($)', "prevalence percapita", [linear, linear])
    plot_classwise(aug_data, 'classification', 'med_income_percap', 'income_over_deaths', 'income_percap', 'income/deaths', [linear, linear])
    #plt.savefig(fig, )

if __name__ == "__main__":
    entry()