import pandas as pd

#Extract
def extractData(path):
    return pd.read_csv(path, delimiter=',', encoding='unicode_escape')

coffeeProduction = extractData("./Coffee_production.csv")
coffeeConsumtion = extractData("./Coffee_domestic_consumption.csv")

#Transform
def bagsToMTn(bags):
    # original unit is in thousand bags and each bag is of 60kg. 
    kgPerBag = 60
    #Convertion to thousand tones
    umTransformation = 1000000
    return (bags*kgPerBag)/umTransformation
def dataCleaning(dataFrame, UnitColumn, Country):
    # Delete rows with zero values
    cleanDataFrame = dataFrame[(dataFrame != 0).all(axis=1)]
    # Convert from bags units to thousand tones
    convertDataFrame = cleanDataFrame.copy()  # Explicit copy here
    convertDataFrame[UnitColumn] = convertDataFrame[UnitColumn].apply(bagsToMTn)
    # Select top 10 rows ordered by UnitColumn
    topTenDataFrame = convertDataFrame[[Country, UnitColumn]].sort_values(by=[UnitColumn], ascending=False).head(10)
    return topTenDataFrame

top_production = dataCleaning(coffeeProduction, 'Total_production', 'Country')
top_consumption = dataCleaning(coffeeConsumtion, 'Total_domestic_consumption', 'Country')
consumptionVSproduction = top_production.merge(top_consumption, on='Country')

#Load
load = pd.ExcelWriter('Coffee-Analysis-SB.xlsx') 
top_production.to_excel(load, sheet_name='Top-Coffee-Production')
top_consumption.to_excel(load, sheet_name='Top-Coffee-Consumption')
consumptionVSproduction.to_excel(load, sheet_name='Production-vs-Consumption')

load.close()