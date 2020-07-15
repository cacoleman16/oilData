import numpy as np
import pandas as pd
import os
import quandl
import apiKey

key = apiKey.QUANDL_API_KEY

# temporary program to download oil futures and save as xls file

# I plan on going back and making this more flexible for other data and other formats


def main():
    oilfutures = quandl.get("CHRIS/CME_CL1.6", authtoken=key)
    oilfutures = oilfutures.rename(columns={'Settle': 'CL1Settle'})
    for i in range(2, 21):
        c = quandl.get("CHRIS/CME_CL" + str(i) + ".6", authtoken=key)
        c = c.rename(columns={'Settle': 'CL' + str(i) + 'Settle'})
        oilfutures = oilfutures.join(c)
    oilfutures.to_excel(path + "oilfutures.xlsx", na_rep='NaN')


if __name__ == "__main__":
    main()
