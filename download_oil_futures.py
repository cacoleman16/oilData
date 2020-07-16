import numpy as np
import pandas as pd
import os
import quandl
import apiKey


# Variables
key = apiKey.QUANDL_API_KEY
number_of_futures = 38  # This determines how many contracts of cl to downloand. max is 38
file_name = "oilfutures.xlsx"  # sets the file name


# temporary program to download oil futures and save as xls file

# I plan on going back and making this more flexible for other data and other formats


def main():
    try:
        oilfutures = quandl.get("CHRIS/CME_CL1.6", authtoken=key)
        oilfutures = oilfutures.rename(columns={'Settle': 'CL1Settle'})
        for i in range(2, number_of_futures + 1):
            c = quandl.get("CHRIS/CME_CL" + str(i) + ".6", authtoken=key)
            c = c.rename(columns={'Settle': 'CL' + str(i) + 'Settle'})
            oilfutures = oilfutures.join(c)
        oilfutures.to_excel(
            apiKey.path + file_name, na_rep='NaN')

    except:
        print("There was a problem retreiving the data. Conact chasecoleman@uky.edu to update the code")


if __name__ == "__main__":
    main()
