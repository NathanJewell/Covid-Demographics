
gis_demo_data = {
    "fn" : "gis-demo-counties.csv",
    "state_col" : "state_name",
    "county_col" : "name",
    "load_cols" : [
        "population", "pop_sqmi" , "sqmi",
        "white", "black", "ameri_es", "asian", "hawn_pi", "hispanic", "other", "multi_race",
        "med_age"
    ]
}


kaggle_demo_data = {
    "fn" : "kaggle-demo-counties.csv",
    "state_col" : "state",
    "county_col" : "county",
    "load_cols" : [
        "income", "incomepercap", "poverty"
    ]
}

covid_data = {
    "fn" : "covid-counties.csv",
    "state_col" : "county",
    "county_col" : "state",
    "load_cols" : [
        "date", "fips", "cases", "deaths"
    ]
}