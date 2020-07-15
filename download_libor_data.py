import numpy as np
import pandas as pd
import os
from apiKey import FRED_API_KEY
from fredapi import Fred

key = FRED_API_KEY

fred = Fred(api_key=key)



def main():
    df = {}
    df['LIBOR1'] = fred.get_series('USD1MTD156N')
    df['LIBOR2'] = fred.get_series('USD2MTD156N')
    df['LIBOR3'] = fred.get_series('USD3MTD156N')
    df['LIBOR6'] = fred.get_series('USD6MTD156N')
    df['LIBOR12'] = fred.get_series('USD12MD156N')
    df = pd.DataFrame(df)

    df.to_excel(path + "LIBOR.xlsx", na_rep='NaN')


if __name__ == "__main__":
    main()
