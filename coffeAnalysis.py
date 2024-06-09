import pandas as pd

#Extract
coffeeProduction = pd.read_csv("./Coffee_production.csv", delimiter=',', encoding='unicode_escape')
coffeeConsumtion = pd.read_csv("./Coffee_domestic_consumption.csv", delimiter=',', encoding='unicode_escape')

#Transform
def bagsToMTn(x):
    # original unit is in thousand bags and each bag is of 60kg. Convertion to tones
    return (x*60)/1000000

cleanCoffeeProduction = coffeeProduction.copy()
cleanCoffeeProduction = cleanCoffeeProduction[(cleanCoffeeProduction != 0).all(axis=1)]
cleanCoffeeProduction['Total_production'] = cleanCoffeeProduction['Total_production'].apply(bagsToMTn)
top_production = cleanCoffeeProduction[['Country', 'Total_production']].sort_values(by=['Total_production'], ascending=False).head(10)

cleanCoffeeConsumption = coffeeConsumtion.copy()
cleanCoffeeConsumption = cleanCoffeeConsumption[(cleanCoffeeConsumption != 0).all(axis=1)]
cleanCoffeeConsumption['Total_domestic_consumption'] = cleanCoffeeConsumption['Total_domestic_consumption'].apply(bagsToMTn)
top_consumtion = cleanCoffeeConsumption[['Country', 'Total_domestic_consumption']].sort_values(by=['Total_domestic_consumption'], ascending=False).head(10)

print(top_production.head(10))
print(top_consumtion.head(10))

consumptionVSproduction = top_production.merge(top_consumtion, on='Country')
print(consumptionVSproduction)