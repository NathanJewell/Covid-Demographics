
gis_demo_data = {
    "fn" : "gis-demo-counties.csv",
    "state_col" : "state_name",
    "county_col" : "name",
    "state_fmt" : "name",
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
    "state_fmt" : "name",
    "load_cols" : [
        "income", "incomepercap", "poverty"
    ]
}

covid_data = {
    "fn" : "covid-counties.csv",
    "state_col" : "county",
    "county_col" : "state",
    "state_fmt" : "name",
    "load_cols" : [
        "date", "fips", "cases", "deaths"
    ]
}

group_covid_data = {
    "fn" : "group-covid-counties.csv",
    "state_col" : "county",
    "county_col" : "state",
    "state_fmt" : "name",
    "load_cols" : [
        "date", "start_date", "fips", "cases", "deaths"
    ]

}

unemployment_data = {
    "fn" : "Unemployment.csv",
    "state_col" : "stabr",
    "county_col" : "area_name",
    "filter_col" : "rural_urban_continuum_code_2013", #needed to remove state meta-entries
    "state_fmt" : "abv",
    "load_cols" : [
        "median_household_income_2018",
        "unemployment_rate_2018"
        "rural_urban_continuum_code_2013",
        "urban_influence_code_2013"
    ]
}
#"Unemployment and median household income for the U.S., States, and counties, 2000-19",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#"Sources: Unemployment: U.S. Department of Labor, Bureau of Labor Statistics, Local Area Unemployment Statistics (LAUS); median household income: U.S. Department of Commerce, Bureau of the Census, Small Area Income and Poverty Estimates (SAIPE) Program.",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#"For definitions of rural classifications, see the USDA, Economic Research Service webpage ""Rural Classifications"" in the ""Rural Economy & Population"" topic. Variable descriptions (column names) are found in the second tab in this workbook.",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
#"This table was prepared by USDA, Economic Research Service. Data as of May 13, 2020. Contact: Kathleen Kassel.",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

education_data = {
    "fn" : "Education.csv",
    "state_col" : "state",
    "county_col" : "county",
    "state_fmt" : "abv",
    "filter_col" : "2003 rural-urban continuum code", #needed to remove state meta-entries
    "load_cols" : [
        "percent_bs_higher_2014-18",
        "percent_some_college_2014-18",
        "percent_adults_hs_only_2014-18",
        "percent_adults_lessthan_hs_2014-18"
    ]
}


#"Educational attainment for adults age 25 and older for the U.S., States, and counties, 1970-2018","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
#"Sources: U.S. Census Bureau, 1970, 1980, 1990, 2000 Censuses of Population, and the 2014-18 American Community Survey 5-yr average county-level estimates.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
#"For definitions of rural classifications, see the USDA, Economic Research Service webpage ""Rural Classifications"" in the ""Rural Economy & Population"" topic.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""
#"This table was prepared by USDA, Economic Research Service. Data as of February 5, 2020. Contact: Kathleen Kassel.","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""