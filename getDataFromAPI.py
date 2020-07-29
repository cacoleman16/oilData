import quandl
import apiKey
import numpy as np
import pandas as pd
import os
from fredapi import Fred


class getDataFromAPI():
    def __init__(self, key):
        self.key = key
        self.df = {}

    def toDF(self):
        self.df = pd.DataFrame(self.df)

    def toExcel(self, path, filename):
        self.df.to_excel(path + filename, na_rep='NaN')


class getQuandlData(getDataFromAPI):

    def __init__(self, apiKey):
        self.key = apiKey.QUANDL_API_KEY
        self.df = {}

    def getData(self, datapaths, datanames):

        try:
            if isinstance(datapaths, list):

                for datapath, dataname in zip(datapaths, datanames):
                    self.df[dataname] = quandl.get(
                        datapath, authtoken=self.key)
            elif isinstance(datapaths, str):
                self.df[datanames] = quandl.get(datapaths, authtoken=self.key)
            else:
                return 'Input must be string or list.'

        except:
            return "Series does not exist"


class getFredData(getDataFromAPI):
    def __init__(self):
        self.key = apiKey.FRED_API_KEY
        self.fred = Fred(api_key=self.key)
        self.df = {}

    def get_CPI_data(self):
        series = ['CPIAUCSL', 'INDPRO']
        titles = ['CPI', ' Industrial Production Index']
        self.get_data(series, titles,
                      observation_start='12/1/1988', units='pc1')

    def get_LIBOR_data(self):
        self.df['LIBOR1'] = self.fred.get_series('USD1MTD156N')
        self.df['LIBOR2'] = self.fred.get_series('USD2MTD156N')
        self.df['LIBOR3'] = self.fred.get_series('USD3MTD156N')
        self.df['LIBOR6'] = self.fred.get_series('USD6MTD156N')
        self.df['LIBOR12'] = self.fred.get_series('USD12MD156N')

    def get_macro_data(self):

        pass

    def get_data(self, series_names, title_names, observation_start=None, observation_end=None, **kwargs):
        if isinstance(series_names, list):
            try:
                for series_name, title_name in zip(series_names, title_names):
                    self.df[title_name] = self.fred.get_series(
                        series_id=str(series_name), observation_start=observation_start, observation_end=observation_end, **kwargs)
            except:
                return "Series does not exist"

        elif isinstance(series_names, str):
            try:
                self.df[title_names] = self.fred.get_series(
                    series_id=str(series_name), observation_start=observation_start, observation_end=observation_end, **kwargs)
            except:
                return "Series does not exist"

        else:
            return "Input must be a string or list of strings"

    def collect(self):
        pass


if __name__ == "__main__":
    pass
