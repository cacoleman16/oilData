import numpy as np
import pandas as pd
import os
from apiKey import FRED_API_KEY
from fredapi import Fred
#from apiKey import path  # you can remove this and change the path
key = FRED_API_KEY
file_name = "macro_data.xlsx"  # this can be changed to change the file name
fred = Fred(api_key=key)
quartertly = False
null_values = True


def main():
    try:
        if quartertly == True:
            df = {}
            df['Unemployment Rate'] = fred.get_series('UNRATE', frequency='q')
            df['Real GDP'] = fred.get_series('GDPC1')
            df['Industrial Production Index'] = fred.get_series(
                'INDPRO', frequency='q')
            df['Real Personal Expenditures'] = fred.get_series(
                'PCEC96', frequency='q')
            df['Savings Rate'] = fred.get_series('PSAVERT', frequency='q')
            df = pd.DataFrame(df)

            df.to_excel(path + file_name, na_rep='NaN')
        else:
            df = {}
            df['Unemployment Rate'] = fred.get_series('UNRATE')
            df['Industrial Production Index'] = fred.get_series('INDPRO')
            df['Real Personal Expenditures'] = fred.get_series('PCEC96')
            df['Savings Rate'] = fred.get_series('PSAVERT')
            df = pd.DataFrame(df)
            if null_values == False:
                df = df.dropna()
            df.to_excel(path + file_name, na_rep='NaN')

            df = {}
            df = pd.DataFrame(df)
            df['Real GDP'] = fred.get_series('GDPC1')
            df.to_excel(path + "GDP.xlsx", na_rep='NaN')
    except:
        print("An error occured getting the data. Contact chasecoleman@uky.edu to update the code")


if __name__ == "__main__":
    main()
